import pytest
from app.data.repository import JsonRepository
from app.logic.controller import FinanceController
from app.logic.models import Transaction

@pytest.fixture
def controller(tmp_path):
    repo_dir = tmp_path / "data"
    repo = JsonRepository(str(repo_dir))
    return FinanceController(repo)

def test_add_transaction(controller):
    t = controller.add_transaction("income", "T1", "D1", 100.0, "C1", "2024-01-01", "P1")
    assert t.title == "T1"
    
def test_add_transaction_invalid_amount(controller):
    with pytest.raises(ValueError):
        controller.add_transaction("income", "T1", "D1", -10.0, "C1", "2024-01-01", "P1")
        
def test_add_transaction_empty_title(controller):
    with pytest.raises(ValueError):
        controller.add_transaction("income", "   ", "D1", 10.0, "C1", "2024-01-01", "P1")

def test_update_transaction(controller):
    t = controller.add_transaction("income", "T1", "D1", 100.0, "C1", "2024-01-01", "P1")
    t.title = "T2"
    controller.update_transaction(t)
    transactions = controller.get_transactions("income")
    assert transactions[0].title == "T2"

def test_update_transaction_invalid(controller):
    t = controller.add_transaction("income", "T1", "D1", 100.0, "C1", "2024-01-01", "P1")
    t.amount = -5
    with pytest.raises(ValueError):
        controller.update_transaction(t)
    t.amount = 50
    t.title = ""
    with pytest.raises(ValueError):
        controller.update_transaction(t)

def test_delete_transaction(controller):
    t = controller.add_transaction("income", "T1", "D1", 100.0, "C1", "2024-01-01", "P1")
    controller.delete_transaction(t.id, "income")
    assert len(controller.get_transactions("income")) == 0

def test_get_transactions_search(controller):
    controller.add_transaction("income", "Salary", "monthly", 1000, "Job", "2024-01-01", "Bank")
    controller.add_transaction("income", "Bonus", "yearly", 500, "Job", "2024-01-01", "Bank")
    assert len(controller.get_transactions("income", "salary")) == 1
    assert len(controller.get_transactions("income", "yearly")) == 1
    assert len(controller.get_transactions("income", "Job")) == 2

def test_get_dashboard_summary(controller):
    controller.add_transaction("income", "I1", "D", 1000, "Job", "2024-01-01", "P")
    controller.add_transaction("expense", "E1", "D", 200, "Food", "2024-01-05", "P")
    controller.add_transaction("expense", "E2", "D", 100, "Food", "2024-02-05", "P")
    
    summary = controller.get_dashboard_summary()
    assert summary["total_income"] == 1000
    assert summary["total_expense"] == 300
    assert summary["balance"] == 700
    assert summary["expense_by_category"]["Food"] == 300
    assert summary["income_by_category"]["Job"] == 1000
    assert summary["monthly_summary"]["2024-01"]["income"] == 1000
    assert summary["monthly_summary"]["2024-01"]["expense"] == 200
    assert summary["monthly_summary"]["2024-02"]["expense"] == 100
