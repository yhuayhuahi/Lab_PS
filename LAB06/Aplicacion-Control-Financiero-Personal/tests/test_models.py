from app.logic.models import Transaction

def test_transaction_create():
    t = Transaction.create(
        type="income",
        title="Test Income",
        description="Test Desc",
        amount=100.0,
        category="Salario",
        date="2024-01-01",
        payment_method="Efectivo"
    )
    assert t.type == "income"
    assert t.title == "Test Income"
    assert t.description == "Test Desc"
    assert t.amount == 100.0
    assert t.category == "Salario"
    assert t.date == "2024-01-01"
    assert t.payment_method == "Efectivo"
    assert t.id is not None
