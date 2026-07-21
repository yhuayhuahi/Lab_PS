from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QStackedWidget, QMessageBox, QFileDialog
from app.logic.controller import FinanceController
from app.ui.dashboard_view import DashboardView
from app.ui.transaction_view import TransactionView
from app.utils.exports import export_to_csv, export_to_pdf
import os

class MainWindow(QMainWindow):
    def __init__(self, controller: FinanceController):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Aplicación de Control Financiero Personal")
        self.resize(1024, 768)
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(150)
        self.sidebar.addItems(["Dashboard", "Ingresos", "Gastos", "Exportar CSV", "Exportar PDF"])
        self.sidebar.currentRowChanged.connect(self.change_view)
        
        # Stacked Widget
        self.stacked_widget = QStackedWidget()
        
        self.dashboard_view = DashboardView(self.controller)
        self.incomes_view = TransactionView(self.controller, "income")
        self.expenses_view = TransactionView(self.controller, "expense")
        
        self.stacked_widget.addWidget(self.dashboard_view)
        self.stacked_widget.addWidget(self.incomes_view)
        self.stacked_widget.addWidget(self.expenses_view)
        
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stacked_widget)
        
        # CSS Styling for modern look
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f4f6f9;
            }
            QListWidget {
                background-color: #343a40;
                color: white;
                font-size: 16px;
                border: none;
                padding-top: 10px;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #007bff;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border-radius: 5px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
        """)

    def change_view(self, row):
        if row == 0:
            self.dashboard_view.refresh()
            self.stacked_widget.setCurrentIndex(0)
        elif row == 1:
            self.incomes_view.load_data()
            self.stacked_widget.setCurrentIndex(1)
        elif row == 2:
            self.expenses_view.load_data()
            self.stacked_widget.setCurrentIndex(2)
        elif row == 3:
            self.export_csv()
            self.sidebar.setCurrentRow(self.stacked_widget.currentIndex()) # Revert selection
        elif row == 4:
            self.export_pdf()
            self.sidebar.setCurrentRow(self.stacked_widget.currentIndex())

    def export_csv(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Exportar a CSV", "", "CSV Files (*.csv)")
        if filepath:
            try:
                incomes = self.controller.get_transactions("income")
                expenses = self.controller.get_transactions("expense")
                export_to_csv(filepath, incomes + expenses)
                QMessageBox.information(self, "Éxito", "Exportado a CSV correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al exportar: {e}")

    def export_pdf(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Exportar a PDF", "", "PDF Files (*.pdf)")
        if filepath:
            try:
                incomes = self.controller.get_transactions("income")
                expenses = self.controller.get_transactions("expense")
                summary = self.controller.get_dashboard_summary()
                export_to_pdf(filepath, incomes + expenses, summary)
                QMessageBox.information(self, "Éxito", "Exportado a PDF correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al exportar: {e}")
