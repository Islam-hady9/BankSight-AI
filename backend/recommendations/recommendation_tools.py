"""
LangChain Tools for Financial Recommendations

These tools enable the AI agent to analyze customer financial data
and provide personalized recommendations for savings and loans.
"""
from typing import Optional
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool
from .recommendation_engine import recommendation_engine
from ..utils.logger import logger


# Pydantic schemas for tool inputs
class AnalyzeFinancialHealthInput(BaseModel):
    """Input schema for analyzing financial health."""
    customer_id: str = Field(
        description="Customer ID to analyze (e.g., 'customer_001')"
    )


class RecommendSavingsInput(BaseModel):
    """Input schema for savings recommendations."""
    customer_id: str = Field(
        description="Customer ID for savings recommendations"
    )


class CheckLoanEligibilityInput(BaseModel):
    """Input schema for loan eligibility check."""
    customer_id: str = Field(
        description="Customer ID to check"
    )
    loan_type: str = Field(
        description="Type of loan: 'personal', 'auto', 'mortgage', 'student', 'business', or 'debt_consolidation'"
    )


class RecommendLoansInput(BaseModel):
    """Input schema for loan recommendations."""
    customer_id: str = Field(
        description="Customer ID for loan recommendations"
    )


# Tool functions
def analyze_financial_health(customer_id: str) -> dict:
    """
    Analyze a customer's financial health and provide detailed assessment.

    This tool:
    - Calculates financial health score (0-100)
    - Analyzes income, expenses, savings, and debt
    - Identifies financial strengths and concerns
    - Provides debt-to-income ratio
    - Assesses emergency fund adequacy

    Args:
        customer_id: Customer ID (e.g., 'customer_001')

    Returns:
        Comprehensive financial health analysis
    """
    try:
        logger.info(f"Analyzing financial health for {customer_id}")
        result = recommendation_engine.analyze_financial_health(customer_id)
        return result
    except Exception as e:
        logger.error(f"Error analyzing financial health: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def recommend_savings_plans(customer_id: str) -> dict:
    """
    Recommend personalized savings plans based on customer's financial situation.

    This tool analyzes the customer and recommends:
    - Emergency fund plans (if needed)
    - High-yield savings accounts
    - Retirement savings plans
    - Goal-based savings (home, education, etc.)

    Each recommendation includes:
    - Recommended monthly contribution
    - Interest rate and features
    - Specific goals and reasoning

    Args:
        customer_id: Customer ID

    Returns:
        List of personalized savings recommendations with priorities
    """
    try:
        logger.info(f"Generating savings recommendations for {customer_id}")
        result = recommendation_engine.recommend_savings_plans(customer_id)
        return result
    except Exception as e:
        logger.error(f"Error recommending savings: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def check_loan_eligibility(customer_id: str, loan_type: str) -> dict:
    """
    Check if customer is eligible for a specific type of loan.

    This tool verifies:
    - Credit score requirements
    - Income requirements
    - Debt-to-income ratio
    - Employment history
    - Maximum loan amount qualification

    Loan types available:
    - 'personal': Personal loans
    - 'auto': Auto/car loans
    - 'mortgage': Home mortgages
    - 'student': Student loans
    - 'business': Small business loans
    - 'debt_consolidation': Debt consolidation loans

    Args:
        customer_id: Customer ID
        loan_type: Type of loan to check

    Returns:
        Eligibility decision with:
        - Eligible (yes/no)
        - Maximum loan amount (if eligible)
        - Interest rate range
        - Reasons for decision
        - Warnings and recommendations
    """
    try:
        logger.info(f"Checking loan eligibility for {customer_id}: {loan_type}")
        result = recommendation_engine.check_loan_eligibility(customer_id, loan_type)
        return result
    except Exception as e:
        logger.error(f"Error checking loan eligibility: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def recommend_loans(customer_id: str) -> dict:
    """
    Recommend appropriate loan products based on customer's financial goals and situation.

    This tool:
    - Analyzes customer's financial goals
    - Checks eligibility for relevant loans
    - Prioritizes recommendations (high/medium/low)
    - Provides specific use cases and benefits
    - Warns about risks and considerations

    Common recommendations:
    - Debt consolidation (for high credit card debt)
    - Home loans (for qualified buyers)
    - Personal loans (for major purchases)
    - Business loans (for entrepreneurs)

    Args:
        customer_id: Customer ID

    Returns:
        List of loan recommendations with:
        - Priority level
        - Eligibility status
        - Purpose and benefits
        - Amount recommendations
        - Required next steps
    """
    try:
        logger.info(f"Generating loan recommendations for {customer_id}")
        result = recommendation_engine.recommend_loans(customer_id)
        return result
    except Exception as e:
        logger.error(f"Error recommending loans: {e}")
        return {
            "success": False,
            "error": str(e)
        }


# Create LangChain tools
def create_recommendation_tools():
    """Create LangChain tools for financial recommendations."""

    tools = [
        StructuredTool.from_function(
            func=analyze_financial_health,
            name="AnalyzeFinancialHealth",
            description=(
                "Analyze a customer's complete financial health. "
                "Use this when the user asks about their financial situation, "
                "wants a financial checkup, or needs an overall assessment. "
                "Provides financial health score, income/expense analysis, debt assessment, "
                "savings evaluation, and identifies strengths and concerns."
            ),
            args_schema=AnalyzeFinancialHealthInput,
            return_direct=False
        ),

        StructuredTool.from_function(
            func=recommend_savings_plans,
            name="RecommendSavingsPlans",
            description=(
                "Recommend personalized savings plans for a customer. "
                "Use this when the user wants to start saving, needs savings advice, "
                "or wants to know which savings account is best for them. "
                "Recommends emergency funds, high-yield accounts, retirement plans, "
                "and goal-based savings with specific monthly contribution amounts."
            ),
            args_schema=RecommendSavingsInput,
            return_direct=False
        ),

        StructuredTool.from_function(
            func=check_loan_eligibility,
            name="CheckLoanEligibility",
            description=(
                "Check if a customer qualifies for a specific loan type. "
                "Use this when the user asks if they can get a loan, "
                "wants to know their maximum loan amount, or needs loan eligibility assessment. "
                "Checks credit score, income, debt-to-income ratio, and employment. "
                "Loan types: 'personal', 'auto', 'mortgage', 'student', 'business', 'debt_consolidation'."
            ),
            args_schema=CheckLoanEligibilityInput,
            return_direct=False
        ),

        StructuredTool.from_function(
            func=recommend_loans,
            name="RecommendLoans",
            description=(
                "Recommend appropriate loan products based on customer's financial goals. "
                "Use this when the user asks what loans they should consider, "
                "needs financing options, or wants personalized loan recommendations. "
                "Analyzes their situation and suggests suitable loans with priorities, "
                "benefits, and warnings."
            ),
            args_schema=RecommendLoansInput,
            return_direct=False
        ),
    ]

    return tools
