import os
import pytest
from app.utils.exports import export_to_csv, export_to_pdf
from app.logic.models import Transaction

def test_export_csv(tmp_path):
    t = Transaction.create("income", "T1", "D1", 100.0, "C1", "2024-01-01", "P1")
    file_path = tmp_path / "test.csv"
    export_to_csv(str(file_path), [t])
    assert os.path.exists(str(file_path))
    with open(str(file_path), "r", encoding="utf-8") as f:
        content = f.read()
        assert "ID,Tipo,Título,Descripción,Monto,Categoría,Fecha,Método de Pago" in content
        assert "T1" in content

def test_export_pdf(tmp_path):
    t = Transaction.create("income", "T1", "D1", 100.0, "C1", "2024-01-01", "P1")
    # Forzar salto de página creando múltiples transacciones (más de 30-40)
    transactions = [t] * 60 
    summary = {"total_income": 100, "total_expense": 0, "balance": 100}
    file_path = tmp_path / "test.pdf"
    export_to_pdf(str(file_path), transactions, summary)
    assert os.path.exists(str(file_path))
