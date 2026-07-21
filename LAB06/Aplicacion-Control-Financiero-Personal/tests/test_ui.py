import pytest
from unittest.mock import MagicMock
from PySide6.QtWidgets import QMessageBox, QDialog
from PySide6.QtCore import QDate
from app.ui.transaction_dialog import TransactionDialog
from app.ui.transaction_view import TransactionView
from app.ui.dashboard_view import DashboardView
from app.ui.main_window import MainWindow
from app.logic.controller import FinanceController
from app.data.repository import JsonRepository
from app.logic.models import Transaction

@pytest.fixture
def controller(tmp_path):
    repo_dir = tmp_path / "data"
    repo = JsonRepository(str(repo_dir))
    return FinanceController(repo)

def test_transaction_dialog(qtbot):
    dialog = TransactionDialog(transaction_type="income")
    qtbot.addWidget(dialog)
    
    dialog.title_input.setText("Test Title")
    dialog.description_input.setText("Test Desc")
    dialog.amount_input.setValue(150.0)
    dialog.category_input.setCurrentText("Salario")
    dialog.date_input.setDate(QDate(2024, 1, 1))
    dialog.payment_method_input.setCurrentText("Efectivo")
    
    data = dialog.get_data()
    assert data["title"] == "Test Title"
    assert data["amount"] == 150.0
    
def test_transaction_dialog_load_data(qtbot):
    t = Transaction.create("income", "Loaded", "D", 50, "Salario", "2024-01-01", "Efectivo")
    dialog = TransactionDialog(transaction_type="income", transaction=t)
    qtbot.addWidget(dialog)
    assert dialog.title_input.text() == "Loaded"
    assert dialog.amount_input.value() == 50.0

def test_transaction_dialog_empty_title(qtbot, monkeypatch):
    dialog = TransactionDialog(transaction_type="income")
    qtbot.addWidget(dialog)
    dialog.title_input.setText("")
    
    mock_warning = MagicMock()
    monkeypatch.setattr(QMessageBox, "warning", mock_warning)
    
    dialog.save()
    mock_warning.assert_called_once()
    
def test_transaction_dialog_zero_amount(qtbot, monkeypatch):
    dialog = TransactionDialog(transaction_type="income")
    qtbot.addWidget(dialog)
    dialog.title_input.setText("Title")
    dialog.amount_input.setValue(0.0)
    
    mock_warning = MagicMock()
    monkeypatch.setattr(QMessageBox, "warning", mock_warning)
    
    dialog.save()
    mock_warning.assert_called_once()

def test_transaction_view(qtbot, controller):
    view = TransactionView(controller, "income")
    qtbot.addWidget(view)
    
    controller.add_transaction("income", "T1", "D1", 100, "Salario", "2024-01-01", "Efectivo")
    view.load_data()
    
    assert view.table.rowCount() == 1
    assert view.table.item(0, 2).text() == "T1"
    
def test_transaction_view_add_dialog(qtbot, controller, monkeypatch):
    view = TransactionView(controller, "income")
    qtbot.addWidget(view)
    
    class MockDialog:
        def __init__(self, *args, **kwargs): pass
        def exec(self): return QDialog.Accepted
        def get_data(self):
            return {"title": "T1", "description": "D1", "amount": 100, "category": "Salario", "date": "2024-01-01", "payment_method": "Efectivo"}
    
    monkeypatch.setattr("app.ui.transaction_view.TransactionDialog", MockDialog)
    view.add_transaction()
    assert view.table.rowCount() == 1

def test_transaction_view_delete(qtbot, controller, monkeypatch):
    view = TransactionView(controller, "income")
    qtbot.addWidget(view)
    controller.add_transaction("income", "T1", "D1", 100, "Salario", "2024-01-01", "Efectivo")
    view.load_data()
    
    view.table.selectRow(0)
    monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.Yes)
    view.delete_transaction()
    assert view.table.rowCount() == 0

def test_dashboard_view(qtbot, controller):
    controller.add_transaction("income", "I1", "D1", 1000, "Salario", "2024-01-01", "Efectivo")
    controller.add_transaction("expense", "E1", "D2", 200, "Ocio", "2024-01-05", "Efectivo")
    
    dashboard = DashboardView(controller)
    qtbot.addWidget(dashboard)
    
    assert dashboard.kpi_income.value_label.text() == "$1,000.00"
    assert dashboard.kpi_expense.value_label.text() == "$200.00"
    assert dashboard.kpi_balance.value_label.text() == "$800.00"

def test_main_window_routing(qtbot, controller):
    window = MainWindow(controller)
    qtbot.addWidget(window)
    
    window.sidebar.setCurrentRow(1)
    assert window.stacked_widget.currentIndex() == 1
    
    window.sidebar.setCurrentRow(2)
    assert window.stacked_widget.currentIndex() == 2

def test_transaction_view_edit(qtbot, controller, monkeypatch):
    view = TransactionView(controller, "income")
    qtbot.addWidget(view)
    controller.add_transaction("income", "T1", "D1", 100, "Salario", "2024-01-01", "Efectivo")
    view.load_data()
    
    view.table.selectRow(0)
    
    class MockDialog:
        def __init__(self, *args, **kwargs): pass
        def exec(self): return QDialog.Accepted
        def get_data(self):
            return {"title": "T1_mod", "description": "D1", "amount": 200, "category": "Salario", "date": "2024-01-01", "payment_method": "Efectivo"}
            
    monkeypatch.setattr("app.ui.transaction_view.TransactionDialog", MockDialog)
    view.edit_transaction()
    assert view.table.item(0, 2).text() == "T1_mod"

def test_main_window_export_csv(qtbot, controller, monkeypatch):
    window = MainWindow(controller)
    qtbot.addWidget(window)
    monkeypatch.setattr("PySide6.QtWidgets.QFileDialog.getSaveFileName", lambda *args: ("test.csv", ""))
    monkeypatch.setattr("app.ui.main_window.export_to_csv", lambda *args: None)
    monkeypatch.setattr("PySide6.QtWidgets.QMessageBox.information", lambda *args: None)
    window.export_csv()
    
def test_main_window_export_pdf(qtbot, controller, monkeypatch):
    window = MainWindow(controller)
    qtbot.addWidget(window)
    monkeypatch.setattr("PySide6.QtWidgets.QFileDialog.getSaveFileName", lambda *args: ("test.pdf", ""))
    monkeypatch.setattr("app.ui.main_window.export_to_pdf", lambda *args: None)
    monkeypatch.setattr("PySide6.QtWidgets.QMessageBox.information", lambda *args: None)
    window.export_pdf()

def test_main_window_routing_all(qtbot, controller, monkeypatch):
    window = MainWindow(controller)
    qtbot.addWidget(window)
    monkeypatch.setattr(window, "export_csv", lambda: None)
    monkeypatch.setattr(window, "export_pdf", lambda: None)
    window.sidebar.setCurrentRow(0)
    assert window.stacked_widget.currentIndex() == 0
    window.sidebar.setCurrentRow(3)
    window.sidebar.setCurrentRow(4)

def test_main_window_export_csv_error(qtbot, controller, monkeypatch):
    window = MainWindow(controller)
    qtbot.addWidget(window)
    monkeypatch.setattr("PySide6.QtWidgets.QFileDialog.getSaveFileName", lambda *args: ("test.csv", ""))
    def mock_export(*args): raise Exception("Export failed")
    monkeypatch.setattr("app.ui.main_window.export_to_csv", mock_export)
    mock_critical = MagicMock()
    monkeypatch.setattr(QMessageBox, "critical", mock_critical)
    window.export_csv()
    mock_critical.assert_called_once()

def test_main_window_export_pdf_error(qtbot, controller, monkeypatch):
    window = MainWindow(controller)
    qtbot.addWidget(window)
    monkeypatch.setattr("PySide6.QtWidgets.QFileDialog.getSaveFileName", lambda *args: ("test.pdf", ""))
    def mock_export(*args): raise Exception("Export failed")
    monkeypatch.setattr("app.ui.main_window.export_to_pdf", mock_export)
    mock_critical = MagicMock()
    monkeypatch.setattr(QMessageBox, "critical", mock_critical)
    window.export_pdf()
    mock_critical.assert_called_once()

def test_transaction_dialog_expense_and_save(qtbot, monkeypatch):
    dialog = TransactionDialog(transaction_type="expense")
    qtbot.addWidget(dialog)
    dialog.title_input.setText("Expense")
    dialog.amount_input.setValue(10.0)
    mock_accept = MagicMock()
    monkeypatch.setattr(dialog, "accept", mock_accept)
    dialog.save()
    mock_accept.assert_called_once()

def test_transaction_view_add_error(qtbot, controller, monkeypatch):
    view = TransactionView(controller, "income")
    qtbot.addWidget(view)
    class MockDialog:
        def __init__(self, *args, **kwargs): pass
        def exec(self): return QDialog.Accepted
        def get_data(self):
            return {"title": "T1", "description": "D1", "amount": 100, "category": "Salario", "date": "2024-01-01", "payment_method": "Efectivo"}
    monkeypatch.setattr("app.ui.transaction_view.TransactionDialog", MockDialog)
    def mock_add(*args): raise ValueError("Add error")
    monkeypatch.setattr(controller, "add_transaction", mock_add)
    mock_critical = MagicMock()
    monkeypatch.setattr(QMessageBox, "critical", mock_critical)
    view.add_transaction()
    mock_critical.assert_called_once()

def test_transaction_view_edit_no_selection(qtbot, controller, monkeypatch):
    view = TransactionView(controller, "income")
    qtbot.addWidget(view)
    mock_warning = MagicMock()
    monkeypatch.setattr(QMessageBox, "warning", mock_warning)
    view.edit_transaction()
    mock_warning.assert_called_once()

def test_transaction_view_edit_error(qtbot, controller, monkeypatch):
    view = TransactionView(controller, "income")
    qtbot.addWidget(view)
    controller.add_transaction("income", "T1", "D1", 100, "Salario", "2024-01-01", "Efectivo")
    view.load_data()
    view.table.selectRow(0)
    class MockDialog:
        def __init__(self, *args, **kwargs): pass
        def exec(self): return QDialog.Accepted
        def get_data(self):
            return {"title": "T1", "description": "D1", "amount": 100, "category": "Salario", "date": "2024-01-01", "payment_method": "Efectivo"}
    monkeypatch.setattr("app.ui.transaction_view.TransactionDialog", MockDialog)
    def mock_update(*args): raise ValueError("Update error")
    monkeypatch.setattr(controller, "update_transaction", mock_update)
    mock_critical = MagicMock()
    monkeypatch.setattr(QMessageBox, "critical", mock_critical)
    view.edit_transaction()
    mock_critical.assert_called_once()

def test_transaction_view_delete_no_selection(qtbot, controller, monkeypatch):
    view = TransactionView(controller, "income")
    qtbot.addWidget(view)
    mock_warning = MagicMock()
    monkeypatch.setattr(QMessageBox, "warning", mock_warning)
    view.delete_transaction()
    mock_warning.assert_called_once()
