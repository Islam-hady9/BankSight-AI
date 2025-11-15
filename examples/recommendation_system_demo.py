"""
Financial Recommendation System - Demo Examples

This script demonstrates the financial recommendation system features:
1. Financial health analysis
2. Savings plan recommendations
3. Loan eligibility checks
4. Personalized loan recommendations

Uses 7 different customer profiles with various financial situations.
"""
import requests
import json
from typing import List, Dict


# API Configuration
BASE_URL = "http://localhost:8000"

# Customer profiles to demonstrate
DEMO_CUSTOMERS = [
    {"id": "customer_001", "name": "Sarah Johnson", "scenario": "Young professional, ready for homeownership"},
    {"id": "customer_002", "name": "Michael Chen", "scenario": "Business owner, expansion plans"},
    {"id": "customer_003", "name": "Emily Rodriguez", "scenario": "Recent graduate, student debt"},
    {"id": "customer_004", "name": "David Thompson", "scenario": "Senior professional, near retirement"},
    {"id": "customer_005", "name": "Jessica Martinez", "scenario": "Working parent, multiple debts"},
    {"id": "customer_006", "name": "James Wilson", "scenario": "High debt load, needs consolidation"},
    {"id": "customer_007", "name": "Amanda Lee", "scenario": "Freelancer, variable income"},
]


def chat(message: str, session_id: str = "demo") -> Dict:
    """Send message to AI agent."""
    url = f"{BASE_URL}/api/chat"
    payload = {
        "message": message,
        "session_id": session_id
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


def print_header(title: str):
    """Print formatted header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_subheader(title: str):
    """Print formatted subheader."""
    print("\n" + "-" * 80)
    print(f"  {title}")
    print("-" * 80)


def print_response(response: Dict):
    """Pretty print agent response."""
    print(f"\n📊 Response:")
    print(f"  {response['response']}")

    if response.get('tools_used'):
        print(f"\n🔧 Tools Used:")
        for tool in response['tools_used']:
            print(f"  - {tool['tool']}")


def example_1_financial_health_analysis():
    """Example 1: Comprehensive financial health analysis."""
    print_header("Example 1: Financial Health Analysis")

    # Analyze different customer profiles
    customers_to_analyze = [
        ("customer_001", "Young Professional - Sarah"),
        ("customer_003", "Recent Graduate - Emily"),
        ("customer_006", "High Debt - James")
    ]

    for customer_id, description in customers_to_analyze:
        print_subheader(description)
        print(f"\n💬 Request: Analyze financial health for {customer_id}")

        response = chat(
            f"Please analyze the financial health for customer {customer_id}. "
            f"Give me a comprehensive assessment including their financial health score, "
            f"strengths, concerns, and overall financial situation.",
            session_id=f"health_{customer_id}"
        )

        print_response(response)


def example_2_savings_recommendations():
    """Example 2: Personalized savings recommendations."""
    print_header("Example 2: Savings Plan Recommendations")

    # Get recommendations for different scenarios
    scenarios = [
        ("customer_003", "Recent graduate needs emergency fund"),
        ("customer_001", "Professional saving for home down payment"),
        ("customer_004", "Senior planning for retirement")
    ]

    for customer_id, description in scenarios:
        print_subheader(description)
        print(f"\n💬 Request: Recommend savings plans for {customer_id}")

        response = chat(
            f"What savings plans would you recommend for customer {customer_id}? "
            f"I want to know which accounts I should open and how much I should save monthly.",
            session_id=f"savings_{customer_id}"
        )

        print_response(response)


def example_3_loan_eligibility():
    """Example 3: Loan eligibility checks."""
    print_header("Example 3: Loan Eligibility Assessment")

    # Check different loan types for different customers
    scenarios = [
        ("customer_001", "mortgage", "Can I qualify for a home loan?"),
        ("customer_006", "debt_consolidation", "Am I eligible for debt consolidation?"),
        ("customer_002", "business", "Can I get a business loan for expansion?")
    ]

    for customer_id, loan_type, question in scenarios:
        print_subheader(f"{question} - Customer {customer_id}")
        print(f"\n💬 Request: Check {loan_type} loan eligibility")

        response = chat(
            f"Customer {customer_id} wants to know: {question} "
            f"Please check if they're eligible for a {loan_type} loan and explain why or why not.",
            session_id=f"loan_{customer_id}_{loan_type}"
        )

        print_response(response)


def example_4_comprehensive_recommendations():
    """Example 4: Complete financial recommendations."""
    print_header("Example 4: Comprehensive Financial Recommendations")

    # Get full recommendations for customers in different situations
    customers = [
        ("customer_005", "Working parent with multiple debts"),
        ("customer_007", "Freelancer with variable income")
    ]

    for customer_id, description in customers:
        print_subheader(description)
        print(f"\n💬 Request: Complete financial advice")

        response = chat(
            f"I'm customer {customer_id}. Please analyze my financial situation "
            f"and recommend both savings plans and loan products that would be appropriate for me. "
            f"Tell me what I should prioritize and why.",
            session_id=f"complete_{customer_id}"
        )

        print_response(response)


def example_5_specific_scenarios():
    """Example 5: Specific financial scenarios."""
    print_header("Example 5: Specific Financial Scenarios")

    scenarios = [
        {
            "customer_id": "customer_003",
            "question": "I just graduated and have $45,000 in student loans. Should I focus on paying off debt or start saving?",
            "description": "Debt vs Savings Priority"
        },
        {
            "customer_id": "customer_001",
            "question": "I want to buy a house. How much should I save for a down payment and can I qualify for a mortgage?",
            "description": "Home Buying Guidance"
        },
        {
            "customer_id": "customer_006",
            "question": "I'm struggling with $15,000 credit card debt and multiple loans. What should I do?",
            "description": "Debt Crisis Help"
        }
    ]

    for scenario in scenarios:
        print_subheader(scenario["description"])
        print(f"\n💬 Question: {scenario['question']}")

        response = chat(
            f"Customer ID: {scenario['customer_id']}. Question: {scenario['question']}",
            session_id=f"scenario_{scenario['customer_id']}"
        )

        print_response(response)


def example_6_multi_turn_conversation():
    """Example 6: Multi-turn conversation with recommendations."""
    print_header("Example 6: Multi-Turn Financial Advisory Conversation")

    customer_id = "customer_005"
    session_id = "multi_turn_demo"

    print_subheader("Turn 1: Initial Assessment")
    print(f"\n💬 User: I need help with my finances")
    response = chat(
        f"Hi, I'm customer {customer_id}. I need help understanding my financial situation "
        f"and what I should do to improve it.",
        session_id=session_id
    )
    print_response(response)

    print_subheader("Turn 2: Follow-up on Recommendations")
    print(f"\n💬 User: Tell me more about savings options")
    response = chat(
        "Based on my situation, what specific savings plans would you recommend and how much should I save?",
        session_id=session_id
    )
    print_response(response)

    print_subheader("Turn 3: Loan Inquiry")
    print(f"\n💬 User: What about debt consolidation?")
    response = chat(
        "I'm interested in consolidating my debt. Am I eligible and would it help my situation?",
        session_id=session_id
    )
    print_response(response)

    print_subheader("Turn 4: Action Plan")
    print(f"\n💬 User: Give me a concrete action plan")
    response = chat(
        "Give me a step-by-step action plan for the next 6 months to improve my financial health.",
        session_id=session_id
    )
    print_response(response)


def example_7_comparison():
    """Example 7: Compare recommendations across customers."""
    print_header("Example 7: Comparative Analysis")

    print("\nComparing recommendations for 3 different customer profiles:\n")

    customers = ["customer_001", "customer_003", "customer_006"]

    for customer_id in customers:
        print_subheader(f"Customer {customer_id}")

        response = chat(
            f"Give me a brief summary of customer {customer_id}'s financial health "
            f"and top 2 recommendations.",
            session_id=f"compare_{customer_id}"
        )

        print_response(response)


def main():
    """Run all examples."""
    print("\n" + "=" * 80)
    print("  BANKSIGHT AI - FINANCIAL RECOMMENDATION SYSTEM DEMO")
    print("=" * 80)
    print("\nThis demo showcases personalized financial recommendations based on")
    print("customer analysis including:")
    print("  • Financial health scoring")
    print("  • Savings plan recommendations")
    print("  • Loan eligibility assessment")
    print("  • Debt management advice")
    print("\n7 customer profiles with different financial situations are demonstrated.")

    try:
        # Check if backend is running
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            raise Exception("Backend not healthy")

        print("\n✅ Backend connection successful")
        print("\nAvailable customer profiles:")
        for customer in DEMO_CUSTOMERS:
            print(f"  • {customer['id']}: {customer['name']} - {customer['scenario']}")

        # Run examples
        input("\n\nPress Enter to start examples...")

        example_1_financial_health_analysis()
        input("\n\nPress Enter for next example...")

        example_2_savings_recommendations()
        input("\n\nPress Enter for next example...")

        example_3_loan_eligibility()
        input("\n\nPress Enter for next example...")

        example_4_comprehensive_recommendations()
        input("\n\nPress Enter for next example...")

        example_5_specific_scenarios()
        input("\n\nPress Enter for next example...")

        example_6_multi_turn_conversation()
        input("\n\nPress Enter for final example...")

        example_7_comparison()

        print("\n" + "=" * 80)
        print("  ✅ All examples completed successfully!")
        print("=" * 80)

    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to backend.")
        print("Make sure the backend is running:")
        print("  python -m uvicorn backend.main:app --reload")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
