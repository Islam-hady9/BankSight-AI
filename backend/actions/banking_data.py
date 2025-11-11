"""
Load and manage dummy banking data.
"""
import json
from pathlib import Path
from typing import Dict, List, Optional
from ..config import config
from ..utils.logger import logger


class BankingDataManager:
    """Manage dummy banking data from JSON file."""

    def __init__(self):
        self.data_file = config.banking_data_file
        self.data = None
        logger.info(f"Banking data file: {self.data_file}")

    def load_data(self) -> Dict:
        """Load banking data from JSON file."""
        if self.data is not None:
            return self.data

        try:
            with open(self.data_file, "r") as f:
                self.data = json.load(f)
            logger.info("Banking data loaded successfully")
            return self.data
        except Exception as e:
            logger.error(f"Failed to load banking data: {e}")
            # Return empty data structure
            self.data = {
                "users": [],
                "accounts": [],
                "transactions": [],
                "payees": []
            }
            return self.data

    def save_data(self):
        """Save data back to JSON file."""
        try:
            with open(self.data_file, "w") as f:
                json.dump(self.data, f, indent=2)
            logger.info("Banking data saved")
        except Exception as e:
            logger.error(f"Failed to save banking data: {e}")

    def get_user(self, user_id: str = None) -> Optional[Dict]:
        """Get user by ID."""
        if self.data is None:
            self.load_data()

        user_id = user_id or config.banking_default_user

        for user in self.data.get("users", []):
            if user["id"] == user_id:
                return user
        return None

    def get_accounts(self, user_id: str = None) -> List[Dict]:
        """Get all accounts for a user."""
        if self.data is None:
            self.load_data()

        user_id = user_id or config.banking_default_user

        return [
            acc for acc in self.data.get("accounts", [])
            if acc["user_id"] == user_id
        ]

    def get_account(self, account_type: str = "checking", user_id: str = None) -> Optional[Dict]:
        """Get specific account by type."""
        accounts = self.get_accounts(user_id)

        for acc in accounts:
            if acc["type"] == account_type:
                return acc
        return None

    def get_transactions(self, account_id: str, limit: int = 10) -> List[Dict]:
        """Get transactions for an account."""
        if self.data is None:
            self.load_data()

        transactions = [
            txn for txn in self.data.get("transactions", [])
            if txn["account_id"] == account_id
        ]

        # Sort by date (newest first)
        transactions.sort(key=lambda x: x["date"], reverse=True)

        return transactions[:limit]

    def add_transaction(self, transaction: Dict):
        """Add a new transaction."""
        if self.data is None:
            self.load_data()

        self.data["transactions"].append(transaction)
        self.save_data()

    def update_account_balance(self, account_id: str, new_balance: float):
        """Update account balance."""
        if self.data is None:
            self.load_data()

        for acc in self.data.get("accounts", []):
            if acc["id"] == account_id:
                acc["balance"] = new_balance
                break

        self.save_data()


# Global data manager
banking_data = BankingDataManager()
