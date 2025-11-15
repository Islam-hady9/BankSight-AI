"""
Financial Recommendation Engine

Analyzes customer financial data and provides personalized recommendations
for savings plans, loans, and other banking products.
"""
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from ..utils.logger import logger


class RecommendationEngine:
    """Financial recommendation engine for banking products."""

    def __init__(self):
        """Initialize recommendation engine with product catalogs."""
        self.products_file = Path(__file__).parent.parent.parent / "data" / "financial_products.json"
        self.customers_file = Path(__file__).parent.parent.parent / "data" / "customer_profiles.json"

        self.products = self._load_products()
        self.customers = self._load_customers()

        logger.info("Recommendation engine initialized")

    def _load_products(self) -> Dict:
        """Load financial products catalog."""
        try:
            with open(self.products_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load products: {e}")
            return {"savings_plans": [], "loan_products": [], "credit_cards": []}

    def _load_customers(self) -> Dict:
        """Load customer profiles."""
        try:
            with open(self.customers_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load customers: {e}")
            return {"customers": []}

    def get_customer_profile(self, customer_id: str) -> Optional[Dict]:
        """Get customer profile by ID."""
        for customer in self.customers.get("customers", []):
            if customer["id"] == customer_id:
                return customer
        return None

    def calculate_financial_health_score(self, customer: Dict) -> Tuple[int, str]:
        """
        Calculate financial health score (0-100).

        Returns:
            Tuple of (score, category)
        """
        score = 0

        # Income stability (20 points)
        if customer["employment_status"] == "full_time":
            score += 15
            if customer["employment_months"] >= 24:
                score += 5
        elif customer["employment_status"] == "self_employed":
            score += 10
            if customer["employment_months"] >= 36:
                score += 5

        # Savings rate (25 points)
        income = customer["financial_data"]["monthly_income"]
        expenses = customer["financial_data"]["monthly_expenses"]
        savings_rate = ((income - expenses) / income * 100) if income > 0 else 0

        if savings_rate >= 20:
            score += 25
        elif savings_rate >= 10:
            score += 15
        elif savings_rate >= 5:
            score += 10
        elif savings_rate > 0:
            score += 5

        # Debt-to-Income ratio (25 points)
        total_debt_monthly = sum(customer.get("debts", {}).values()) / 12  # Rough monthly
        dti_ratio = (total_debt_monthly / income * 100) if income > 0 else 0

        if dti_ratio < 20:
            score += 25
        elif dti_ratio < 35:
            score += 20
        elif dti_ratio < 50:
            score += 10
        elif dti_ratio < 70:
            score += 5

        # Credit score (20 points)
        credit = customer.get("credit_score", 0)
        if credit >= 750:
            score += 20
        elif credit >= 700:
            score += 15
        elif credit >= 650:
            score += 10
        elif credit >= 600:
            score += 5

        # Emergency fund (10 points)
        savings = customer.get("accounts", {}).get("savings_balance", 0)
        emergency_fund_months = savings / expenses if expenses > 0 else 0

        if emergency_fund_months >= 6:
            score += 10
        elif emergency_fund_months >= 3:
            score += 7
        elif emergency_fund_months >= 1:
            score += 4

        # Categorize
        if score >= 80:
            category = "Excellent"
        elif score >= 65:
            category = "Good"
        elif score >= 50:
            category = "Fair"
        elif score >= 35:
            category = "Needs Improvement"
        else:
            category = "Critical"

        return score, category

    def analyze_financial_health(self, customer_id: str) -> Dict:
        """
        Comprehensive financial health analysis.

        Args:
            customer_id: Customer ID

        Returns:
            Dict with analysis results
        """
        customer = self.get_customer_profile(customer_id)
        if not customer:
            return {"success": False, "error": "Customer not found"}

        income = customer["financial_data"]["monthly_income"]
        expenses = customer["financial_data"]["monthly_expenses"]
        net_cashflow = income - expenses
        savings_rate = (net_cashflow / income * 100) if income > 0 else 0

        # Calculate totals
        checking = customer["accounts"].get("checking_balance", 0)
        savings = customer["accounts"].get("savings_balance", 0)
        investments = customer["accounts"].get("investment_balance", 0)
        total_assets = checking + savings + investments

        total_debt = sum(customer.get("debts", {}).values())

        # Calculate DTI
        monthly_debt = total_debt / 12  # Rough estimate
        dti_ratio = (monthly_debt / income * 100) if income > 0 else 0

        # Health score
        health_score, category = self.calculate_financial_health_score(customer)

        # Identify strengths
        strengths = []
        if savings_rate >= 15:
            strengths.append("Strong savings rate")
        if customer.get("credit_score", 0) >= 720:
            strengths.append("Excellent credit score")
        if dti_ratio < 30:
            strengths.append("Low debt burden")
        if savings >= expenses * 3:
            strengths.append("Adequate emergency fund")

        # Identify concerns
        concerns = []
        if savings_rate < 5:
            concerns.append("Low or negative savings rate")
        if customer.get("credit_score", 0) < 650:
            concerns.append("Credit score needs improvement")
        if dti_ratio > 40:
            concerns.append("High debt-to-income ratio")
        if savings < expenses * 3:
            concerns.append("Insufficient emergency fund")
        if net_cashflow < 0:
            concerns.append("⚠️ CRITICAL: Expenses exceed income")

        return {
            "success": True,
            "customer_name": customer["name"],
            "customer_id": customer_id,
            "monthly_income": income,
            "monthly_expenses": expenses,
            "net_cashflow": net_cashflow,
            "savings_rate": round(savings_rate, 1),
            "checking_balance": checking,
            "savings_balance": savings,
            "investments": investments,
            "total_assets": total_assets,
            "total_debt": total_debt,
            "dti_ratio": round(dti_ratio, 1),
            "credit_score": customer.get("credit_score", 0),
            "health_score": health_score,
            "category": category,
            "strengths": strengths,
            "concerns": concerns,
            "employment_status": customer["employment_status"],
            "employment_months": customer["employment_months"]
        }

    def recommend_savings_plans(self, customer_id: str) -> Dict:
        """
        Recommend appropriate savings plans for customer.

        Args:
            customer_id: Customer ID

        Returns:
            Dict with recommendations
        """
        customer = self.get_customer_profile(customer_id)
        if not customer:
            return {"success": False, "error": "Customer not found"}

        analysis = self.analyze_financial_health(customer_id)
        if not analysis.get("success"):
            return analysis

        recommendations = []

        income = analysis["monthly_income"]
        savings_rate = analysis["savings_rate"]
        net_cashflow = analysis["net_cashflow"]
        savings_balance = analysis["savings_balance"]

        # Recommend emergency fund if needed
        if savings_balance < income * 3:
            for plan in self.products["savings_plans"]:
                if "emergency_fund" in plan.get("recommended_for", []):
                    recommended_amount = min(net_cashflow * 0.3, 500)
                    recommendations.append({
                        "plan": plan,
                        "priority": "high",
                        "recommended_monthly": round(recommended_amount, 2),
                        "goal": "Build 3-6 month emergency fund",
                        "target_amount": income * 6,
                        "reasoning": "Emergency fund is essential financial safety net"
                    })
                    break

        # High-yield savings for stable income customers
        if net_cashflow > 1000 and savings_balance >= 5000:
            for plan in self.products["savings_plans"]:
                if plan["id"] == "savings_high_yield":
                    recommendations.append({
                        "plan": plan,
                        "priority": "medium",
                        "recommended_monthly": round(net_cashflow * 0.4, 2),
                        "goal": "Maximize savings growth",
                        "reasoning": "Your stable income and existing savings qualify you for higher returns"
                    })

        # Retirement savings for customers over 25
        if customer["age"] >= 25 and net_cashflow > 500:
            for plan in self.products["savings_plans"]:
                if plan["type"] == "retirement":
                    recommended_amount = max(net_cashflow * 0.15, income * 0.1)
                    recommendations.append({
                        "plan": plan,
                        "priority": "high" if customer["age"] > 40 else "medium",
                        "recommended_monthly": round(recommended_amount, 2),
                        "goal": "Retirement planning",
                        "reasoning": f"Start/increase retirement savings (target: 10-15% of income)"
                    })
                    break

        # Goal savings for specific needs
        if net_cashflow > 300 and "buy_home" in customer.get("financial_goals", []):
            for plan in self.products["savings_plans"]:
                if plan["id"] == "savings_goal":
                    recommendations.append({
                        "plan": plan,
                        "priority": "medium",
                        "recommended_monthly": round(net_cashflow * 0.25, 2),
                        "goal": "Home down payment",
                        "target_amount": 50000,
                        "reasoning": "Dedicated savings for your home purchase goal"
                    })
                    break

        return {
            "success": True,
            "customer_name": customer["name"],
            "recommendations": recommendations,
            "analysis_summary": {
                "monthly_income": income,
                "available_for_savings": net_cashflow,
                "current_savings": savings_balance,
                "savings_rate": savings_rate
            }
        }

    def check_loan_eligibility(self, customer_id: str, loan_type: str) -> Dict:
        """
        Check customer eligibility for a specific loan type.

        Args:
            customer_id: Customer ID
            loan_type: Type of loan (personal, auto, home, etc.)

        Returns:
            Dict with eligibility decision and reasoning
        """
        customer = self.get_customer_profile(customer_id)
        if not customer:
            return {"success": False, "error": "Customer not found"}

        analysis = self.analyze_financial_health(customer_id)

        # Find loan product
        loan_product = None
        for loan in self.products["loan_products"]:
            if loan["type"] == loan_type:
                loan_product = loan
                break

        if not loan_product:
            return {"success": False, "error": f"Loan type '{loan_type}' not found"}

        requirements = loan_product["requirements"]
        eligible = True
        reasons = []
        warnings = []

        # Check credit score
        if customer["credit_score"] < requirements.get("min_credit_score", 0):
            eligible = False
            reasons.append(f"Credit score ({customer['credit_score']}) below minimum ({requirements['min_credit_score']})")

        # Check income
        if analysis["monthly_income"] < requirements.get("min_monthly_income", 0):
            eligible = False
            reasons.append(f"Monthly income below minimum requirement")

        # Check DTI ratio
        if analysis["dti_ratio"] > requirements.get("max_dti_ratio", 100):
            eligible = False
            reasons.append(f"Debt-to-income ratio ({analysis['dti_ratio']}%) exceeds maximum ({requirements['max_dti_ratio']}%)")

        # Check employment
        if customer["employment_months"] < requirements.get("employment_months", 0):
            eligible = False
            reasons.append(f"Employment history too short")

        # Calculate max loan amount
        max_amount = loan_product["amount_max"]
        if eligible:
            # Conservative: 30% of annual income or product max, whichever is lower
            income_based_max = (analysis["monthly_income"] * 12) * 0.3
            max_amount = min(income_based_max, loan_product["amount_max"])

        # Add warnings even if eligible
        if analysis["dti_ratio"] > 35:
            warnings.append("⚠️ High debt level - consider debt consolidation first")
        if analysis["savings_rate"] < 10:
            warnings.append("⚠️ Low savings rate - ensure loan payments won't strain finances")
        if analysis["net_cashflow"] < 500:
            warnings.append("⚠️ Limited cashflow - carefully review payment obligations")

        return {
            "success": True,
            "customer_name": customer["name"],
            "loan_product": loan_product["name"],
            "loan_type": loan_type,
            "eligible": eligible,
            "max_amount": round(max_amount, 2) if eligible else 0,
            "interest_rate_range": f"{loan_product['interest_rate_min']}-{loan_product['interest_rate_max']}%",
            "term_range": f"{loan_product['term_months_min']}-{loan_product['term_months_max']} months",
            "reasons": reasons if not eligible else ["All eligibility criteria met"],
            "warnings": warnings,
            "requirements": requirements,
            "customer_metrics": {
                "credit_score": customer["credit_score"],
                "monthly_income": analysis["monthly_income"],
                "dti_ratio": analysis["dti_ratio"],
                "employment_months": customer["employment_months"]
            }
        }

    def recommend_loans(self, customer_id: str) -> Dict:
        """
        Recommend appropriate loan products for customer.

        Args:
            customer_id: Customer ID

        Returns:
            Dict with loan recommendations
        """
        customer = self.get_customer_profile(customer_id)
        if not customer:
            return {"success": False, "error": "Customer not found"}

        analysis = self.analyze_financial_health(customer_id)
        recommendations = []

        # Debt consolidation for high credit card debt
        cc_debt = customer["debts"].get("credit_card_debt", 0)
        if cc_debt > 5000 and analysis["dti_ratio"] < 45:
            eligibility = self.check_loan_eligibility(customer_id, "debt_consolidation")
            if eligibility["eligible"]:
                recommendations.append({
                    "loan": eligibility,
                    "priority": "high",
                    "purpose": "Consolidate high-interest credit card debt",
                    "benefit": f"Could save on interest and simplify payments",
                    "recommended_amount": min(cc_debt, eligibility["max_amount"])
                })

        # Personal loan for goals
        if "major_purchase" in customer.get("financial_goals", []) and analysis["dti_ratio"] < 35:
            eligibility = self.check_loan_eligibility(customer_id, "personal")
            if eligibility["eligible"]:
                recommendations.append({
                    "loan": eligibility,
                    "priority": "medium",
                    "purpose": "Finance major purchase",
                    "benefit": "Fixed rate and predictable payments"
                })

        # Home loan for qualified buyers
        if "buy_home" in customer.get("financial_goals", []):
            eligibility = self.check_loan_eligibility(customer_id, "mortgage")
            if eligibility["eligible"]:
                recommendations.append({
                    "loan": eligibility,
                    "priority": "high",
                    "purpose": "Home purchase",
                    "benefit": "Build equity and potential tax benefits",
                    "down_payment_needed": eligibility["max_amount"] * 0.2
                })
            else:
                # Explain why not qualified
                recommendations.append({
                    "loan": eligibility,
                    "priority": "future",
                    "purpose": "Home purchase (not currently eligible)",
                    "steps_to_qualify": eligibility["reasons"]
                })

        # Business loan for entrepreneurs
        if customer["employment_status"] == "self_employed":
            eligibility = self.check_loan_eligibility(customer_id, "business")
            if eligibility["eligible"]:
                recommendations.append({
                    "loan": eligibility,
                    "priority": "medium",
                    "purpose": "Business expansion",
                    "benefit": "Grow your business with working capital"
                })

        return {
            "success": True,
            "customer_name": customer["name"],
            "recommendations": recommendations,
            "general_advice": self._get_loan_advice(analysis)
        }

    def _get_loan_advice(self, analysis: Dict) -> List[str]:
        """Get general loan advice based on financial health."""
        advice = []

        if analysis["dti_ratio"] > 40:
            advice.append("⚠️ Focus on reducing existing debt before taking new loans")

        if analysis["savings_balance"] < analysis["monthly_expenses"] * 3:
            advice.append("💡 Build emergency fund before major loan commitments")

        if analysis["credit_score"] < 700:
            advice.append("📈 Improving credit score can get you better interest rates")

        if analysis["net_cashflow"] > analysis["monthly_income"] * 0.2:
            advice.append("✅ Strong cashflow - you're in good position for borrowing")

        return advice


# Global instance
recommendation_engine = RecommendationEngine()
