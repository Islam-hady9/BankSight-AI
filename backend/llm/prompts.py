"""
Prompt templates for different tasks.
"""

# System prompts
BANKING_ASSISTANT_SYSTEM = """You are a helpful banking assistant. You help users with their banking questions and tasks.

Guidelines:
- Be concise and clear
- If you don't know something, say so
- For questions, use the provided context
- For actions, extract the relevant parameters
- Be professional and friendly
"""

# Intent classification
INTENT_CLASSIFICATION_PROMPT = """Classify the user's intent into one of these categories:
- question: User is asking a question (needs RAG)
- action: User wants to perform a banking action
- chitchat: General conversation

User query: {query}

Respond with ONLY the intent category (question, action, or chitchat)."""

# RAG prompts
RAG_ANSWER_PROMPT = """Answer the user's question based on the following context.

Context:
{context}

Question: {question}

Instructions:
- Answer only using information from the context
- If the context doesn't contain the answer, say "I don't have that information in my documents."
- Be concise and specific
- Cite the source document if relevant

Answer:"""

# Action extraction
ACTION_EXTRACTION_PROMPT = """Extract the banking action and parameters from this query.

User query: {query}

Available actions:
- get_balance: Check account balance (params: account_type)
- get_transactions: View transactions (params: account_type, limit)
- transfer_funds: Transfer money (params: from_account, to_account, amount)
- search_transactions: Search transactions (params: keyword, category)

Extract:
1. action_name: The action to perform
2. parameters: Dictionary of parameters

Respond in this format:
action: <action_name>
parameters: <parameter_dict>

For example:
action: get_balance
parameters: {{"account_type": "checking"}}

Your extraction:"""

# Chitchat
CHITCHAT_PROMPT = """You are a friendly banking assistant. Respond to this casual message in a helpful way.

User: {query}

Keep your response brief and conversational. If they're greeting you, greet them back. If they're thanking you, acknowledge it.

Response:"""
