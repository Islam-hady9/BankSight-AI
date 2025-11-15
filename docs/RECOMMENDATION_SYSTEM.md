# Financial Recommendation System

AI-powered financial advisory system that analyzes customer financial data and provides personalized recommendations for savings plans and loans.

---

## Overview

The BankSight AI Financial Recommendation System uses advanced algorithms to:
- **Analyze** customer financial health with a comprehensive scoring system (0-100)
- **Recommend** personalized savings plans based on financial goals and situation
- **Assess** loan eligibility with strict safety criteria
- **Suggest** appropriate loan products with risk-aware decision making

---

## Features

### 1. Financial Health Analysis
- **Comprehensive scoring** across 5 dimensions:
  - Income stability (20 points)
  - Savings rate (25 points)
  - Debt-to-Income ratio (25 points)
  - Credit score (20 points)
  - Emergency fund adequacy (10 points)
- **Financial categories**: Excellent (80+), Good (65-79), Fair (50-64), Needs Improvement (35-49), Critical (<35)
- **Detailed assessments** with strengths and concerns
- **Key metrics**: DTI ratio, savings rate, net cashflow, emergency fund coverage

### 2. Savings Recommendations
- **Priority-based suggestions** (High/Medium/Low priority)
- **Product matching** based on:
  - Financial goals (emergency fund, retirement, home purchase, etc.)
  - Income level and stability
  - Current savings balance
  - Risk tolerance
- **Monthly contribution guidance** tailored to income and expenses
- **5 savings products**:
  - Basic Savings Account (0.5% APY, $100 min)
  - High-Yield Savings (4.5% APY, $5,000 min)
  - Goal Saver Account (3.0% APY, $500 min)
  - Retirement Savings Plan (5.0% APY, $1,000 min)
  - Youth Savings (2.0% APY, $25 min)

### 3. Loan Eligibility Assessment
- **Multi-criteria validation**:
  - Credit score requirements (varies by loan type)
  - Minimum income thresholds
  - Debt-to-Income ratio limits
  - Employment history verification
- **Conservative loan amount calculations** (max 30% of annual income)
- **6 loan types**:
  - Personal Loans (7.5-15% APR, $1K-$50K)
  - Auto Loans (4.5-9% APR, $5K-$75K)
  - Home Mortgages (3.5-7% APR, $50K-$1M)
  - Student Loans (4-8% APR, $1K-$100K)
  - Business Loans (6-12% APR, $10K-$500K)
  - Debt Consolidation (8-14% APR, $5K-$100K)

### 4. Risk-Based Recommendations
- **Safety-first approach**: Never recommend products that increase financial risk
- **Red flags** prevent loan recommendations for:
  - DTI ratio > 50%
  - Expenses exceeding income
  - Recent bankruptcies
  - Critical financial health scores
- **Warnings** for borderline cases
- **Responsible lending** compliance

---

## LangChain Agent Tools

The recommendation system provides 4 tools for the AI agent:

### 1. AnalyzeFinancialHealth
**Description**: Analyze customer's complete financial health

**Input**: `customer_id` (string)

**Output**:
```json
{
  "success": true,
  "customer_id": "customer_001",
  "financial_health": {
    "score": 72,
    "category": "Good",
    "income_analysis": {
      "monthly_income": 8500,
      "monthly_expenses": 5200,
      "net_cashflow": 3300,
      "savings_rate": 38.8
    },
    "debt_analysis": {
      "total_debt": 20500,
      "dti_ratio": 26.7,
      "monthly_debt_payments": 650
    },
    "strengths": [
      "Excellent savings rate of 38.8%",
      "Strong credit score of 750"
    ],
    "concerns": [
      "Student loan debt of $18,000"
    ]
  }
}
```

**Use when**:
- User asks about their financial situation
- Wants a financial checkup
- Needs overall assessment before making decisions

---

### 2. RecommendSavingsPlans
**Description**: Recommend personalized savings plans

**Input**: `customer_id` (string)

**Output**:
```json
{
  "success": true,
  "recommendations": [
    {
      "product_id": "savings_high_yield",
      "product_name": "High-Yield Savings Account",
      "priority": "high",
      "recommended_monthly_deposit": 1700,
      "interest_rate": 4.5,
      "reason": "Excellent for growing emergency fund with stable income",
      "goal": "Build 6-month emergency fund"
    }
  ]
}
```

**Use when**:
- User wants to start saving
- Needs savings advice
- Asks which savings account is best
- Wants to know how much to save monthly

---

### 3. CheckLoanEligibility
**Description**: Check if customer qualifies for a specific loan

**Input**:
- `customer_id` (string)
- `loan_type` (string): One of `personal`, `auto`, `mortgage`, `student`, `business`, `debt_consolidation`

**Output**:
```json
{
  "success": true,
  "eligible": true,
  "loan_type": "mortgage",
  "max_loan_amount": 255000,
  "interest_rate_range": "3.5% - 7.0%",
  "reasons": [
    "✓ Credit score 750 meets requirement (700+)",
    "✓ DTI ratio 26.7% is below 36% threshold",
    "✓ Stable employment for 48+ months"
  ],
  "warnings": [
    "Consider 20% down payment for better rates"
  ]
}
```

**Use when**:
- User asks if they can get a loan
- Wants to know maximum loan amount
- Needs loan eligibility assessment

---

### 4. RecommendLoans
**Description**: Recommend appropriate loan products based on goals

**Input**: `customer_id` (string)

**Output**:
```json
{
  "success": true,
  "recommendations": [
    {
      "product_id": "loan_mortgage",
      "loan_type": "mortgage",
      "priority": "high",
      "eligible": true,
      "max_amount": 255000,
      "purpose": "Home purchase aligns with your financial goals",
      "benefits": [
        "Build equity instead of renting",
        "Tax deductions on mortgage interest"
      ],
      "next_steps": [
        "Save for 20% down payment ($51,000)",
        "Get pre-approved to lock in rates"
      ]
    }
  ]
}
```

**Use when**:
- User asks what loans they should consider
- Needs financing options
- Wants personalized loan recommendations

---

## Customer Profile Structure

Customer profiles must include:

```json
{
  "id": "customer_001",
  "name": "Customer Name",
  "age": 28,
  "occupation": "Job Title",
  "employment_status": "full_time",
  "employment_months": 48,
  "credit_score": 750,
  "financial_data": {
    "monthly_income": 8500,
    "monthly_expenses": 5200,
    "rent_mortgage": 1800,
    "utilities": 200,
    "groceries": 500,
    "transportation": 400,
    "entertainment": 300,
    "insurance": 250,
    "other_expenses": 750
  },
  "accounts": {
    "checking_balance": 4500,
    "savings_balance": 15000,
    "investment_balance": 25000
  },
  "debts": {
    "credit_card_debt": 2500,
    "student_loans": 18000,
    "car_loan": 0,
    "personal_loans": 0
  },
  "financial_goals": [
    "buy_home",
    "retirement_savings",
    "emergency_fund"
  ],
  "risk_tolerance": "moderate"
}
```

---

## Usage Examples

### Example 1: Financial Health Check

**User Query**:
```
"Analyze my financial health for customer customer_001"
```

**Agent Response**:
```
I've analyzed your financial health. Here's your assessment:

📊 Financial Health Score: 72/100 (Good)

Income Analysis:
• Monthly Income: $8,500
• Monthly Expenses: $5,200
• Net Cashflow: +$3,300
• Savings Rate: 38.8% (Excellent!)

Debt Analysis:
• Total Debt: $20,500
• Debt-to-Income Ratio: 26.7% (Healthy)
• Monthly Debt Payments: $650

💪 Strengths:
• Excellent savings rate of 38.8%
• Strong credit score of 750
• Healthy debt-to-income ratio under 30%

⚠️ Areas to Monitor:
• Student loan debt of $18,000
• Credit card balance of $2,500

Overall, you're in a good financial position with room for improvement!
```

---

### Example 2: Savings Recommendations

**User Query**:
```
"What savings plans would you recommend for me? I want to know which accounts I should open."
```

**Agent Response**:
```
Based on your financial situation, here are my top savings recommendations:

🎯 HIGH PRIORITY:
1. High-Yield Savings Account (4.5% APY)
   - Recommended monthly deposit: $1,700
   - Goal: Build 6-month emergency fund ($31,200)
   - Why: Your stable income and existing savings make this ideal
   - Features: FDIC insured, competitive rates, easy access

📈 MEDIUM PRIORITY:
2. Retirement Savings Plan (5.0% APY)
   - Recommended monthly deposit: $850
   - Goal: Long-term retirement planning
   - Why: At age 28, compound interest will maximize growth
   - Features: Tax advantages, employer matching if available

💡 Action Plan:
Start with the High-Yield Savings for your emergency fund, then add retirement savings once you have 3-6 months of expenses saved.
```

---

### Example 3: Loan Eligibility

**User Query**:
```
"Can I qualify for a home loan? What's my maximum loan amount?"
```

**Agent Response**:
```
Great news! You're eligible for a home mortgage. Here's your assessment:

✅ ELIGIBLE for Home Mortgage

Maximum Loan Amount: $255,000
Interest Rate Range: 3.5% - 7.0% (based on credit)

Why You Qualify:
✓ Credit score 750 exceeds requirement (700+)
✓ DTI ratio 26.7% is well below 36% threshold
✓ Stable full-time employment for 48+ months
✓ Sufficient income for monthly payments

⚠️ Important Considerations:
• Aim for 20% down payment ($51,000) to avoid PMI
• Keep DTI below 28% after mortgage for comfort
• Pre-approval will lock in your rate

Next Steps:
1. Save for down payment (you have $15K, need $36K more)
2. Get pre-approved with 2-3 lenders to compare
3. Budget for closing costs (2-5% of loan amount)

Would you like help creating a savings plan for your down payment?
```

---

### Example 4: Multi-Turn Conversation

**Turn 1**: "I need help with my finances"
```
I'm here to help! Let me analyze your financial situation first.

[Agent uses AnalyzeFinancialHealth tool]

Your financial health score is 72/100 - you're in good shape! You have a strong savings rate and healthy debt levels. What specific area would you like to focus on?
```

**Turn 2**: "What should I prioritize - paying off debt or saving more?"
```
Based on your situation, here's my recommendation:

Your student loan has a moderate interest rate and your DTI is healthy at 26.7%. I'd suggest a balanced approach:

1. Continue minimum payments on student loan
2. Pay off $2,500 credit card debt first (likely higher interest)
3. Build 6-month emergency fund in High-Yield Savings
4. Then accelerate student loan payments

You have $3,300/month net cashflow, so you can do both! Allocate:
• $1,700/month → Emergency fund
• $500/month → Extra credit card payment
• $1,100/month → Flexible (fun, extra savings, etc.)

This approach protects you with emergency savings while eliminating high-interest debt.
```

---

## Testing with Demo Script

Run the comprehensive demo:

```bash
# Make sure backend is running
python -m uvicorn backend.main:app --reload

# In another terminal, run demo
python examples/recommendation_system_demo.py
```

**Demo includes 7 examples**:
1. Financial health analysis (3 customer profiles)
2. Savings plan recommendations (3 scenarios)
3. Loan eligibility checks (3 loan types)
4. Comprehensive recommendations (2 customers)
5. Specific financial scenarios (3 situations)
6. Multi-turn conversation (4-turn dialogue)
7. Comparative analysis (3 customers)

---

## Financial Health Scoring Methodology

### Scoring Breakdown (100 points total):

**Income Stability (20 points)**:
- Full-time employment: 15 points
- 24+ months tenure: +5 points
- Part-time/contract: 10 points
- Unemployed: 0 points

**Savings Rate (25 points)**:
- ≥20% of income: 25 points
- 10-19%: 15 points
- 5-9%: 10 points
- 1-4%: 5 points
- <1%: 0 points

**Debt-to-Income Ratio (25 points)**:
- <20%: 25 points
- 20-35%: 20 points
- 36-43%: 15 points
- 44-50%: 5 points
- >50%: 0 points

**Credit Score (20 points)**:
- 750+: 20 points
- 700-749: 15 points
- 650-699: 10 points
- 600-649: 5 points
- <600: 0 points

**Emergency Fund (10 points)**:
- ≥6 months expenses: 10 points
- 3-6 months: 7 points
- 1-3 months: 4 points
- <1 month: 0 points

### Score Categories:

- **80-100 (Excellent)**: Strong financial health, eligible for best rates
- **65-79 (Good)**: Solid financial position, some room for improvement
- **50-64 (Fair)**: Moderate financial health, should focus on improvements
- **35-49 (Needs Improvement)**: Financial vulnerabilities, urgent action needed
- **0-34 (Critical)**: Severe financial stress, immediate intervention required

---

## Safety Guidelines

### When NOT to Recommend Loans:

❌ **Automatic Disqualification**:
- Debt-to-Income ratio > 50%
- Monthly expenses exceed income
- Credit score < minimum for loan type
- No emergency fund AND requesting non-essential loan
- Recent bankruptcy or foreclosure

⚠️ **Warning Flags (recommend with caution)**:
- DTI ratio 40-50%
- Variable/irregular income
- Poor credit history (600-650)
- Multiple existing loans
- High credit utilization

✅ **Safe to Recommend**:
- DTI < 40%
- Stable employment 12+ months
- Emergency fund exists
- Credit score meets requirements
- Loan serves clear financial goal

### Conservative Calculations:

- **Maximum loan amount**: 30% of annual income (not standard 43% DTI)
- **Home loans**: Require 36% DTI (stricter than standard 43%)
- **Debt consolidation**: Only if reduces total payments by 20%+
- **Business loans**: Extra scrutiny for self-employed

---

## API Integration

### Using with LangChain Agent:

```python
from backend.agent.langchain_agent import BankSightAgent

agent = BankSightAgent()

# The agent automatically has access to recommendation tools
response = agent.chat(
    "Analyze customer customer_001's financial health and recommend savings plans",
    session_id="advisor_session"
)

print(response)
```

### Direct Engine Usage:

```python
from backend.recommendations.recommendation_engine import recommendation_engine

# Financial health analysis
health = recommendation_engine.analyze_financial_health("customer_001")
print(f"Score: {health['financial_health']['score']}")

# Savings recommendations
savings = recommendation_engine.recommend_savings_plans("customer_001")
for rec in savings['recommendations']:
    print(f"{rec['product_name']}: ${rec['recommended_monthly_deposit']}/month")

# Loan eligibility
eligibility = recommendation_engine.check_loan_eligibility("customer_001", "mortgage")
print(f"Eligible: {eligibility['eligible']}")
print(f"Max amount: ${eligibility['max_loan_amount']}")

# Loan recommendations
loans = recommendation_engine.recommend_loans("customer_001")
for rec in loans['recommendations']:
    print(f"{rec['loan_type']}: {rec['priority']} priority")
```

---

## File Structure

```
backend/recommendations/
├── __init__.py                    # Module initialization
├── prompts.py                     # System prompts and templates
├── recommendation_engine.py       # Core recommendation logic
└── recommendation_tools.py        # LangChain tool definitions

data/
├── customer_profiles.json         # 7 test customer profiles
└── financial_products.json        # Savings/loan product catalog

examples/
└── recommendation_system_demo.py  # Comprehensive demo script
```

---

## Customization

### Adding New Products:

Edit `data/financial_products.json`:

```json
{
  "savings_plans": [
    {
      "id": "savings_custom",
      "name": "Custom Savings Plan",
      "interest_rate": 5.0,
      "min_balance": 1000,
      "monthly_fee": 0,
      "features": ["Feature 1", "Feature 2"],
      "recommended_for": ["goal1", "goal2"]
    }
  ]
}
```

### Adding New Customers:

Edit `data/customer_profiles.json` following the customer profile structure above.

### Modifying Scoring:

Edit `backend/recommendations/recommendation_engine.py`:

```python
def calculate_financial_health_score(self, customer: Dict) -> Tuple[int, str]:
    # Modify scoring weights here
    score = 0

    # Adjust weights (must total 100)
    income_weight = 20
    savings_weight = 25
    dti_weight = 25
    credit_weight = 20
    emergency_weight = 10

    # ... scoring logic
```

---

## Troubleshooting

### Issue: "Customer not found"

**Solution**: Ensure customer ID exists in `data/customer_profiles.json`

### Issue: "No eligible products"

**Solution**: Customer may not meet requirements. Check:
- Credit score
- Income level
- Debt-to-Income ratio

### Issue: "All recommendations have low priority"

**Solution**: This is intentional for high-risk customers. Review financial health score and address concerns first.

### Issue: Tools not available in agent

**Solution**: Check that recommendation tools are imported in `backend/agent/langchain_tools.py`:

```python
from ..recommendations.recommendation_tools import create_recommendation_tools
```

---

## Future Enhancements

Potential improvements:
- Machine learning-based recommendations
- Investment product recommendations
- Insurance policy suggestions
- Tax optimization advice
- Retirement planning calculator
- Real-time product rate updates
- Credit score improvement plans
- Debt payoff optimization
- Budget creation tools
- Financial goal tracking

---

## References

- **Debt-to-Income Ratio**: https://www.consumerfinance.gov/ask-cfpb/what-is-a-debt-to-income-ratio-why-is-the-43-debt-to-income-ratio-important-en-1791/
- **Credit Score Ranges**: https://www.experian.com/blogs/ask-experian/credit-education/score-basics/what-is-a-good-credit-score/
- **Emergency Fund Guidelines**: https://www.consumerfinance.gov/ask-cfpb/how-much-should-i-save-in-my-emergency-fund-en-1464/

---

**Last Updated**: November 15, 2025
**Version**: 1.0.0
**Author**: BankSight AI Development Team
