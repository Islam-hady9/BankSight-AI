"""
Query routing based on intent.
"""
from typing import Dict
from .intent_classifier import Intent
from ..rag.retriever import retrieve_and_generate
from ..actions.banking_actions import execute_action
from ..llm.huggingface_client import llm_client
from ..llm.prompts import CHITCHAT_PROMPT, ACTION_EXTRACTION_PROMPT
from ..utils.logger import logger
import re


async def route_query(query: str, intent: Intent) -> Dict:
    """
    Route query to appropriate handler based on intent.

    Args:
        query: User query
        intent: Classified intent

    Returns:
        Dict with response and metadata
    """
    if intent == Intent.QUESTION:
        logger.info("Routing to RAG system")
        result = await retrieve_and_generate(query)
        return {
            "response": result["answer"],
            "intent": "question",
            "sources": result.get("sources", [])
        }

    elif intent == Intent.ACTION:
        logger.info("Routing to action handler")
        result = await handle_action(query)
        return {
            "response": result["response"],
            "intent": "action",
            "action_result": result.get("action_result", {}),
            "sources": []
        }

    else:  # CHITCHAT
        logger.info("Routing to chitchat handler")
        result = await handle_chitchat(query)
        return {
            "response": result,
            "intent": "chitchat",
            "sources": []
        }


async def handle_action(query: str) -> Dict:
    """Handle banking action queries."""
    # Extract action and parameters
    action_info = extract_action_parameters(query)

    if not action_info["action"]:
        return {
            "response": "I understand you want to perform an action, but I'm not sure which one. Try asking about balance, transactions, or transfers.",
            "action_result": {}
        }

    # Execute action
    result = execute_action(action_info["action"], action_info["parameters"])

    # Format response
    if result.get("success"):
        response = format_action_response(action_info["action"], result)
    else:
        response = f"Sorry, I couldn't complete that action: {result.get('error', 'Unknown error')}"

    return {
        "response": response,
        "action_result": result
    }


async def handle_chitchat(query: str) -> str:
    """Handle casual conversation."""
    prompt = CHITCHAT_PROMPT.format(query=query)
    response = llm_client.generate(prompt, max_new_tokens=100)
    return response


def extract_action_parameters(query: str) -> Dict:
    """
    Extract action and parameters from query using keywords.

    Args:
        query: User query

    Returns:
        Dict with 'action' and 'parameters'
    """
    query_lower = query.lower()

    # Balance check
    if "balance" in query_lower:
        account_type = "checking"
        if "savings" in query_lower:
            account_type = "savings"
        elif "credit" in query_lower:
            account_type = "credit_card"

        return {
            "action": "get_balance",
            "parameters": {"account_type": account_type}
        }

    # Transactions
    if "transaction" in query_lower or "history" in query_lower or "show" in query_lower:
        # Extract limit
        limit = 5
        numbers = re.findall(r'\d+', query)
        if numbers:
            limit = int(numbers[0])

        account_type = "checking"
        if "savings" in query_lower:
            account_type = "savings"

        return {
            "action": "get_transactions",
            "parameters": {"account_type": account_type, "limit": min(limit, 20)}
        }

    # Transfer
    if "transfer" in query_lower or "send" in query_lower or "move" in query_lower:
        # Extract amount
        amounts = re.findall(r'\$?(\d+(?:\.\d{2})?)', query)
        amount = float(amounts[0]) if amounts else 0.0

        # Determine accounts
        from_account = "checking"
        to_account = "savings"

        if "savings" in query_lower and "checking" in query_lower:
            if query_lower.index("savings") < query_lower.index("checking"):
                from_account, to_account = "savings", "checking"

        return {
            "action": "transfer_funds",
            "parameters": {
                "from_account": from_account,
                "to_account": to_account,
                "amount": amount
            }
        }

    # Search
    if "search" in query_lower or "find" in query_lower:
        # Extract keyword (simple approach)
        keywords = query_lower.replace("search", "").replace("find", "").replace("transactions", "").strip()

        return {
            "action": "search_transactions",
            "parameters": {"keyword": keywords if keywords else None}
        }

    return {"action": None, "parameters": {}}


def format_action_response(action: str, result: Dict) -> str:
    """Format action result into natural language response."""
    if action == "get_balance":
        return f"Your {result['account_type']} account ({result['account_number']}) has a balance of ${result['balance']:,.2f}."

    elif action == "get_transactions":
        transactions = result.get("transactions", [])
        if not transactions:
            return "No transactions found."

        response = f"Here are your last {len(transactions)} transactions:\n\n"
        for txn in transactions:
            amount_str = f"${abs(txn['amount']):,.2f}"
            sign = "+" if txn['amount'] > 0 else "-"
            response += f"{sign}{amount_str} - {txn['merchant']} ({txn['date']})\n"

        return response

    elif action == "transfer_funds":
        return f"✅ Transfer completed!\n${result['amount']:,.2f} transferred from {result['from_account']} to {result['to_account']}.\nNew {result['from_account']} balance: ${result['new_balance']:,.2f}"

    elif action == "search_transactions":
        count = result.get("count", 0)
        if count == 0:
            return "No transactions found matching your criteria."

        response = f"Found {count} matching transactions:\n\n"
        for txn in result["transactions"][:10]:  # Limit to 10
            amount_str = f"${abs(txn['amount']):,.2f}"
            sign = "+" if txn['amount'] > 0 else "-"
            response += f"{sign}{amount_str} - {txn['merchant']} ({txn['date']})\n"

        return response

    return str(result)
