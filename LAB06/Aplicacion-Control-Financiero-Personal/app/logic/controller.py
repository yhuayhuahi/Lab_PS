from typing import List, Dict, Any
from collections import defaultdict
from app.logic.models import Transaction
from app.data.repository import JsonRepository

class FinanceController:
    def __init__(self, repository: JsonRepository):
        self.repository = repository

    def add_transaction(self, t_type: str, title: str, description: str, amount: float, category: str, date: str, payment_method: str) -> Transaction:
        if amount <= 0:
            raise ValueError("El monto debe ser mayor a cero")
        if not title.strip():
            raise ValueError("El título no puede estar vacío")
        
        t = Transaction.create(t_type, title, description, amount, category, date, payment_method)
        self.repository.add(t)
        return t

    def update_transaction(self, transaction: Transaction):
        if transaction.amount <= 0:
            raise ValueError("El monto debe ser mayor a cero")
        if not transaction.title.strip():
            raise ValueError("El título no puede estar vacío")
        self.repository.update(transaction)

    def delete_transaction(self, t_id: str, t_type: str):
        self.repository.delete(t_id, t_type)

    def get_transactions(self, t_type: str, search_term: str = "") -> List[Transaction]:
        transactions = self.repository.get_all(t_type)
        if search_term:
            term = search_term.lower()
            transactions = [
                t for t in transactions 
                if term in t.title.lower() or 
                   term in t.description.lower() or 
                   term in t.category.lower()
            ]
        return transactions

    def get_dashboard_summary(self) -> Dict[str, Any]:
        incomes = self.repository.get_all("income")
        expenses = self.repository.get_all("expense")
        
        total_income = sum(t.amount for t in incomes)
        total_expense = sum(t.amount for t in expenses)
        balance = total_income - total_expense
        
        expense_by_category = defaultdict(float)
        for e in expenses:
            expense_by_category[e.category] += e.amount
            
        income_by_category = defaultdict(float)
        for i in incomes:
            income_by_category[i.category] += i.amount
            
        # Resumen mensual simple (por mes, ej: YYYY-MM)
        monthly_summary = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
        for i in incomes:
            month = i.date[:7]
            monthly_summary[month]["income"] += i.amount
        for e in expenses:
            month = e.date[:7]
            monthly_summary[month]["expense"] += e.amount
            
        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
            "expense_by_category": dict(expense_by_category),
            "income_by_category": dict(income_by_category),
            "monthly_summary": dict(monthly_summary)
        }
