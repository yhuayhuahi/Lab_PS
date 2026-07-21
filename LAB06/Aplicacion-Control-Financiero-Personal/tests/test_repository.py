import pytest
import os
from app.data.repository import JsonRepository
from app.logic.models import Transaction

@pytest.fixture
def repo(tmp_path):
    repo_dir = tmp_path / "data"
    return JsonRepository(str(repo_dir))

def test_repo_initialization(repo):
    assert os.path.exists(repo.incomes_file)
    assert os.path.exists(repo.expenses_file)

def test_repo_add_and_get(repo):
    t = Transaction.create("income", "T1", "D1", 100, "C1", "2024-01-01", "P1")
    repo.add(t)
    incomes = repo.get_all("income")
    assert len(incomes) == 1
    assert incomes[0].id == t.id

def test_repo_invalid_type(repo):
    with pytest.raises(ValueError):
        repo.get_all("invalid")

def test_repo_update(repo):
    t = Transaction.create("expense", "T1", "D1", 100, "C1", "2024-01-01", "P1")
    repo.add(t)
    t.amount = 200
    assert repo.update(t) is True
    expenses = repo.get_all("expense")
    assert expenses[0].amount == 200

def test_repo_update_not_found(repo):
    t = Transaction.create("expense", "T1", "D1", 100, "C1", "2024-01-01", "P1")
    with pytest.raises(ValueError):
        repo.update(t)

def test_repo_delete(repo):
    t = Transaction.create("income", "T1", "D1", 100, "C1", "2024-01-01", "P1")
    repo.add(t)
    repo.delete(t.id, "income")
    assert len(repo.get_all("income")) == 0

def test_repo_delete_not_found(repo):
    with pytest.raises(ValueError):
        repo.delete("invalid-id", "income")
