import json
import os
from typing import List
from app.logic.models import Transaction

class JsonRepository:
    def __init__(self, directory: str):
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)
        self.incomes_file = os.path.join(self.directory, "incomes.json")
        self.expenses_file = os.path.join(self.directory, "expenses.json")
        self._ensure_files()

    def _ensure_files(self):
        for file_path in [self.incomes_file, self.expenses_file]:
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump([], f)

    def _get_file_path(self, transaction_type: str) -> str:
        if transaction_type == "income":
            return self.incomes_file
        elif transaction_type == "expense":
            return self.expenses_file
        raise ValueError(f"Invalid transaction type: {transaction_type}")

    def get_all(self, transaction_type: str) -> List[Transaction]:
        file_path = self._get_file_path(transaction_type)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Transaction(**item) for item in data]

    def _save_all(self, transaction_type: str, transactions: List[Transaction]):
        file_path = self._get_file_path(transaction_type)
        with open(file_path, "w", encoding="utf-8") as f:
            data = [t.__dict__ for t in transactions]
            json.dump(data, f, indent=4, ensure_ascii=False)

    def add(self, transaction: Transaction):
        transactions = self.get_all(transaction.type)
        transactions.append(transaction)
        self._save_all(transaction.type, transactions)

    def update(self, transaction: Transaction):
        transactions = self.get_all(transaction.type)
        for i, t in enumerate(transactions):
            if t.id == transaction.id:
                transactions[i] = transaction
                self._save_all(transaction.type, transactions)
                return True
        raise ValueError(f"Transaction with id {transaction.id} not found")

    def delete(self, transaction_id: str, transaction_type: str):
        transactions = self.get_all(transaction_type)
        filtered = [t for t in transactions if t.id != transaction_id]
        if len(filtered) == len(transactions):
            raise ValueError(f"Transaction with id {transaction_id} not found")
        self._save_all(transaction_type, filtered)
