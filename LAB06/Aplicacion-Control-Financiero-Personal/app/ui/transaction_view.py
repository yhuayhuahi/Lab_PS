from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QMessageBox, QDialog
from PySide6.QtCore import Qt
from app.logic.controller import FinanceController
from app.ui.transaction_dialog import TransactionDialog
from app.logic.models import Transaction

class TransactionView(QWidget):
    def __init__(self, controller: FinanceController, transaction_type: str, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.transaction_type = transaction_type
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por título, descripción o categoría...")
        self.search_input.textChanged.connect(self.load_data)
        
        self.btn_add = QPushButton("Nuevo")
        self.btn_add.clicked.connect(self.add_transaction)
        
        self.btn_edit = QPushButton("Editar")
        self.btn_edit.clicked.connect(self.edit_transaction)
        
        self.btn_delete = QPushButton("Eliminar")
        self.btn_delete.clicked.connect(self.delete_transaction)
        
        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addWidget(self.btn_add)
        toolbar_layout.addWidget(self.btn_edit)
        toolbar_layout.addWidget(self.btn_delete)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Fecha", "Título", "Descripción", "Monto", "Categoría", "Método de Pago"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.hideColumn(0) # Hide ID column
        
        layout.addLayout(toolbar_layout)
        layout.addWidget(self.table)

    def load_data(self):
        search_term = self.search_input.text()
        transactions = self.controller.get_transactions(self.transaction_type, search_term)
        self.table.setRowCount(0)
        for t in transactions:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(t.id))
            self.table.setItem(row, 1, QTableWidgetItem(t.date))
            self.table.setItem(row, 2, QTableWidgetItem(t.title))
            self.table.setItem(row, 3, QTableWidgetItem(t.description))
            self.table.setItem(row, 4, QTableWidgetItem(f"${t.amount:.2f}"))
            self.table.setItem(row, 5, QTableWidgetItem(t.category))
            self.table.setItem(row, 6, QTableWidgetItem(t.payment_method))

    def add_transaction(self):
        dialog = TransactionDialog(self, self.transaction_type)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            try:
                self.controller.add_transaction(
                    self.transaction_type, data["title"], data["description"], 
                    data["amount"], data["category"], data["date"], data["payment_method"]
                )
                self.load_data()
            except ValueError as e:
                QMessageBox.critical(self, "Error", str(e))

    def edit_transaction(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Advertencia", "Seleccione una transacción para editar.")
            return
        
        row = selected[0].row()
        t_id = self.table.item(row, 0).text()
        
        # Encuentra la transacción
        transactions = self.controller.get_transactions(self.transaction_type)
        transaction = next((t for t in transactions if t.id == t_id), None)
        
        if transaction:
            dialog = TransactionDialog(self, self.transaction_type, transaction)
            if dialog.exec() == QDialog.Accepted:
                data = dialog.get_data()
                transaction.title = data["title"]
                transaction.description = data["description"]
                transaction.amount = data["amount"]
                transaction.category = data["category"]
                transaction.date = data["date"]
                transaction.payment_method = data["payment_method"]
                
                try:
                    self.controller.update_transaction(transaction)
                    self.load_data()
                except ValueError as e:
                    QMessageBox.critical(self, "Error", str(e))

    def delete_transaction(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Advertencia", "Seleccione una transacción para eliminar.")
            return
        
        reply = QMessageBox.question(self, "Confirmar", "¿Está seguro de eliminar esta transacción?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            row = selected[0].row()
            t_id = self.table.item(row, 0).text()
            self.controller.delete_transaction(t_id, self.transaction_type)
            self.load_data()
