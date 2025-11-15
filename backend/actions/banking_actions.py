"""
Banking actions that can be performed on dummy data.
"""
from typing import Dict, List, Optional
from datetime import datetime
import uuid
from .banking_data import banking_data
from ..utils.logger import logger
from ..utils.exceptions import ActionExecutionError


def get_account_balance(account_type: str = "checking", user_id: str = None) -> Dict:
    """
    Get account balance.

    Args:
        account_type: Type of account (checking, savings, credit_card)
        user_id: User ID (optional)

    Returns:
        Dict with account details and balance
    """
    try:
        account = banking_data.get_account(account_type, user_id)

        if not account:
            return {
                "success": False,
                "error": f"No {account_type} account found"
            }

        return {
            "success": True,
            "account_type": account["type"],
            "balance": account["balance"],
            "account_number": account["account_number"],
            "status": account["status"]
        }

    except Exception as e:
        logger.error(f"Error getting balance: {e}")
        raise ActionExecutionError(f"Failed to get balance: {e}")


def get_transactions(account_type: str = "checking", limit: int = 5, user_id: str = None) -> Dict:
    """
    Get recent transactions.

    Args:
        account_type: Type of account
        limit: Number of transactions to return
        user_id: User ID (optional)

    Returns:
        Dict with transactions list
    """
    try:
        account = banking_data.get_account(account_type, user_id)

        if not account:
            return {
                "success": False,
                "error": f"No {account_type} account found"
            }

        transactions = banking_data.get_transactions(account["id"], limit)

        return {
            "success": True,
            "account_type": account_type,
            "transactions": transactions,
            "count": len(transactions)
        }

    except Exception as e:
        logger.error(f"Error getting transactions: {e}")
        raise ActionExecutionError(f"Failed to get transactions: {e}")


def transfer_funds(
    from_account: str = "checking",
    to_account: str = "savings",
    amount: float = 0.0,
    user_id: str = None
) -> Dict:
    """
    Transfer funds between accounts.

    Args:
        from_account: Source account type
        to_account: Destination account type
        amount: Amount to transfer
        user_id: User ID (optional)

    Returns:
        Dict with transfer result
    """
    try:
        # Get accounts
        source_acc = banking_data.get_account(from_account, user_id)
        dest_acc = banking_data.get_account(to_account, user_id)

        if not source_acc:
            return {"success": False, "error": f"Source account '{from_account}' not found"}

        if not dest_acc:
            return {"success": False, "error": f"Destination account '{to_account}' not found"}

        # Check balance
        if source_acc["balance"] < amount:
            return {
                "success": False,
                "error": "Insufficient funds",
                "available": source_acc["balance"],
                "requested": amount
            }

        # Update balances
        new_source_balance = source_acc["balance"] - amount
        new_dest_balance = dest_acc["balance"] + amount

        banking_data.update_account_balance(source_acc["id"], new_source_balance)
        banking_data.update_account_balance(dest_acc["id"], new_dest_balance)

        # Create transaction records
        txn_id = f"txn_{uuid.uuid4().hex[:8]}"
        date = datetime.now().strftime("%Y-%m-%d")

        # Debit transaction
        banking_data.add_transaction({
            "id": f"{txn_id}_debit",
            "account_id": source_acc["id"],
            "date": date,
            "amount": -amount,
            "merchant": f"Transfer to {to_account}",
            "category": "transfer",
            "description": f"Transfer to {to_account}",
            "status": "completed"
        })

        # Credit transaction
        banking_data.add_transaction({
            "id": f"{txn_id}_credit",
            "account_id": dest_acc["id"],
            "date": date,
            "amount": amount,
            "merchant": f"Transfer from {from_account}",
            "category": "transfer",
            "description": f"Transfer from {from_account}",
            "status": "completed"
        })

        logger.info(f"Transfer completed: ${amount} from {from_account} to {to_account}")

        return {
            "success": True,
            "from_account": from_account,
            "to_account": to_account,
            "amount": amount,
            "new_balance": new_source_balance,
            "transaction_id": txn_id
        }

    except Exception as e:
        logger.error(f"Error transferring funds: {e}")
        raise ActionExecutionError(f"Failed to transfer funds: {e}")


def search_transactions(
    keyword: str = None,
    category: str = None,
    min_amount: float = None,
    account_type: str = "checking",
    user_id: str = None
) -> Dict:
    """
    Search transactions by keyword or category.

    Args:
        keyword: Search in merchant/description
        category: Transaction category
        min_amount: Minimum amount
        account_type: Account type
        user_id: User ID

    Returns:
        Dict with matching transactions
    """
    try:
        account = banking_data.get_account(account_type, user_id)

        if not account:
            return {"success": False, "error": f"Account '{account_type}' not found"}

        # Get all transactions
        all_transactions = banking_data.get_transactions(account["id"], limit=100)

        # Filter
        results = []
        for txn in all_transactions:
            match = True

            if keyword:
                keyword_lower = keyword.lower()
                if keyword_lower not in txn.get("merchant", "").lower() and \
                   keyword_lower not in txn.get("description", "").lower():
                    match = False

            if category and txn.get("category") != category:
                match = False

            if min_amount is not None and abs(txn.get("amount", 0)) < min_amount:
                match = False

            if match:
                results.append(txn)

        return {
            "success": True,
            "transactions": results,
            "count": len(results),
            "filters": {
                "keyword": keyword,
                "category": category,
                "min_amount": min_amount
            }
        }

    except Exception as e:
        logger.error(f"Error searching transactions: {e}")
        raise ActionExecutionError(f"Failed to search transactions: {e}")


# Action registry
AVAILABLE_ACTIONS = {
    "get_balance": get_account_balance,
    "get_transactions": get_transactions,
    "transfer_funds": transfer_funds,
    "search_transactions": search_transactions,
}


def execute_action(action_name: str, parameters: Dict) -> Dict:
    """
    Execute a banking action.

    Args:
        action_name: Name of the action
        parameters: Action parameters

    Returns:
        Action result
    """
    if action_name not in AVAILABLE_ACTIONS:
        return {
            "success": False,
            "error": f"Unknown action: {action_name}",
            "available_actions": list(AVAILABLE_ACTIONS.keys())
        }

    action_func = AVAILABLE_ACTIONS[action_name]

    try:
        result = action_func(**parameters)
        return result
    except Exception as e:
        logger.error(f"Action execution failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }
