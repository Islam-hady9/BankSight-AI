"""
LangChain tool definitions for banking actions.
"""
from typing import Optional
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool
from ..actions.banking_actions import (
    get_account_balance,
    get_transactions,
    transfer_funds,
    search_transactions
)


# Pydantic schemas for tool parameters
class GetBalanceInput(BaseModel):
    """Input schema for getting account balance."""
    account_type: str = Field(
        default="checking",
        description="Type of account: 'checking', 'savings', or 'credit_card'"
    )
    user_id: Optional[str] = Field(
        default=None,
        description="User ID (optional, defaults to demo user)"
    )


class GetTransactionsInput(BaseModel):
    """Input schema for getting transactions."""
    account_type: str = Field(
        default="checking",
        description="Type of account: 'checking', 'savings', or 'credit_card'"
    )
    limit: int = Field(
        default=5,
        description="Number of recent transactions to retrieve (1-20)"
    )
    user_id: Optional[str] = Field(
        default=None,
        description="User ID (optional, defaults to demo user)"
    )


class TransferFundsInput(BaseModel):
    """Input schema for transferring funds."""
    from_account: str = Field(
        description="Source account type: 'checking', 'savings', or 'credit_card'"
    )
    to_account: str = Field(
        description="Destination account type: 'checking', 'savings', or 'credit_card'"
    )
    amount: float = Field(
        description="Amount to transfer (must be positive)"
    )
    user_id: Optional[str] = Field(
        default=None,
        description="User ID (optional, defaults to demo user)"
    )


class SearchTransactionsInput(BaseModel):
    """Input schema for searching transactions."""
    keyword: Optional[str] = Field(
        default=None,
        description="Search keyword for merchant or description"
    )
    category: Optional[str] = Field(
        default=None,
        description="Transaction category (e.g., 'groceries', 'dining', 'transfer')"
    )
    min_amount: Optional[float] = Field(
        default=None,
        description="Minimum transaction amount"
    )
    account_type: str = Field(
        default="checking",
        description="Account type to search in"
    )
    user_id: Optional[str] = Field(
        default=None,
        description="User ID (optional, defaults to demo user)"
    )


# Create LangChain tools
def create_banking_tools():
    """Create LangChain tools for banking actions."""

    tools = [
        StructuredTool.from_function(
            func=get_account_balance,
            name="GetAccountBalance",
            description=(
                "Get the current balance of a bank account. "
                "Use this when the user asks about their balance, how much money they have, "
                "or wants to check their account. "
                "Supports checking, savings, and credit card accounts."
            ),
            args_schema=GetBalanceInput,
            return_direct=False
        ),

        StructuredTool.from_function(
            func=get_transactions,
            name="GetTransactions",
            description=(
                "Get recent transactions for an account. "
                "Use this when the user asks to see their transaction history, "
                "recent purchases, or wants to review their spending. "
                "Returns the most recent transactions up to the specified limit."
            ),
            args_schema=GetTransactionsInput,
            return_direct=False
        ),

        StructuredTool.from_function(
            func=transfer_funds,
            name="TransferFunds",
            description=(
                "Transfer money between accounts. "
                "Use this when the user wants to move money from one account to another, "
                "such as from checking to savings or vice versa. "
                "Validates sufficient balance before transferring."
            ),
            args_schema=TransferFundsInput,
            return_direct=False
        ),

        StructuredTool.from_function(
            func=search_transactions,
            name="SearchTransactions",
            description=(
                "Search for specific transactions by keyword, category, or amount. "
                "Use this when the user wants to find transactions matching certain criteria, "
                "such as 'grocery purchases', 'transactions over $100', or spending at a specific merchant."
            ),
            args_schema=SearchTransactionsInput,
            return_direct=False
        ),
    ]

    # Add recommendation tools if available
    try:
        from ..recommendations.recommendation_tools import create_recommendation_tools
        recommendation_tools = create_recommendation_tools()
        tools.extend(recommendation_tools)
    except ImportError:
        pass  # Recommendation tools not available

    return tools
