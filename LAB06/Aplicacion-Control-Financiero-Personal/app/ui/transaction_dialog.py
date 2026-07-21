from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QDoubleSpinBox, QComboBox, QDateEdit, QPushButton, QHBoxLayout, QMessageBox
from PySide6.QtCore import QDate
from app.logic.models import Transaction

class TransactionDialog(QDialog):
    def __init__(self, parent=None, transaction_type="income", transaction: Transaction = None):
        super().__init__(parent)
        self.transaction_type = transaction_type
        self.transaction = transaction
        self.setWindowTitle(f"{'Editar' if transaction else 'Nuevo'} {'Ingreso' if transaction_type == 'income' else 'Gasto'}")
        self.resize(400, 300)
        self.setup_ui()
        if transaction:
            self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.title_input = QLineEdit()
        self.description_input = QLineEdit()
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setMaximum(999999999.99)
        self.amount_input.setDecimals(2)
        
        self.category_input = QComboBox()
        if self.transaction_type == "income":
            self.category_input.addItems(["Salario", "Negocio", "Inversión", "Otros"])
        else:
            self.category_input.addItems(["Alimentación", "Transporte", "Vivienda", "Salud", "Ocio", "Otros"])

        self.date_input = QDateEdit(QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        self.payment_method_input = QComboBox()
        self.payment_method_input.addItems(["Efectivo", "Tarjeta de Crédito", "Tarjeta de Débito", "Transferencia"])

        form_layout.addRow("Título:", self.title_input)
        form_layout.addRow("Descripción:", self.description_input)
        form_layout.addRow("Monto:", self.amount_input)
        form_layout.addRow("Categoría:", self.category_input)
        form_layout.addRow("Fecha:", self.date_input)
        form_layout.addRow("Método de Pago:", self.payment_method_input)

        layout.addLayout(form_layout)

        buttons_layout = QHBoxLayout()
        self.save_btn = QPushButton("Guardar")
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.clicked.connect(self.reject)

        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.cancel_btn)

        layout.addLayout(buttons_layout)

    def load_data(self):
        self.title_input.setText(self.transaction.title)
        self.description_input.setText(self.transaction.description)
        self.amount_input.setValue(self.transaction.amount)
        self.category_input.setCurrentText(self.transaction.category)
        date = QDate.fromString(self.transaction.date, "yyyy-MM-dd")
        self.date_input.setDate(date)
        self.payment_method_input.setCurrentText(self.transaction.payment_method)

    def save(self):
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Error", "El título es obligatorio.")
            return
        if self.amount_input.value() <= 0:
            QMessageBox.warning(self, "Error", "El monto debe ser mayor a cero.")
            return

        self.accept()

    def get_data(self) -> dict:
        return {
            "title": self.title_input.text().strip(),
            "description": self.description_input.text().strip(),
            "amount": self.amount_input.value(),
            "category": self.category_input.currentText(),
            "date": self.date_input.date().toString("yyyy-MM-dd"),
            "payment_method": self.payment_method_input.currentText()
        }
