from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from app.logic.controller import FinanceController

class KPIWidget(QFrame):
    def __init__(self, title, value, color):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"background-color: {color}; border-radius: 10px; padding: 10px; color: white;")
        layout = QVBoxLayout(self)
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.value_label = QLabel(value)
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)
        layout.addWidget(self.value_label)

    def set_value(self, value):
        self.value_label.setText(value)

class DashboardView(QWidget):
    def __init__(self, controller: FinanceController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # KPIs Layout
        kpi_layout = QHBoxLayout()
        self.kpi_income = KPIWidget("Total Ingresos", "$0.00", "#28a745")
        self.kpi_expense = KPIWidget("Total Gastos", "$0.00", "#dc3545")
        self.kpi_balance = KPIWidget("Balance Total", "$0.00", "#007bff")
        kpi_layout.addWidget(self.kpi_income)
        kpi_layout.addWidget(self.kpi_expense)
        kpi_layout.addWidget(self.kpi_balance)
        
        layout.addLayout(kpi_layout)
        
        # Charts Layout
        charts_layout = QHBoxLayout()
        
        # Figure for categories pie chart
        self.fig_pie = Figure()
        self.canvas_pie = FigureCanvas(self.fig_pie)
        self.ax_pie = self.fig_pie.add_subplot(111)
        charts_layout.addWidget(self.canvas_pie)
        
        # Figure for monthly bar chart
        self.fig_bar = Figure()
        self.canvas_bar = FigureCanvas(self.fig_bar)
        self.ax_bar = self.fig_bar.add_subplot(111)
        charts_layout.addWidget(self.canvas_bar)
        
        layout.addLayout(charts_layout)

    def refresh(self):
        summary = self.controller.get_dashboard_summary()
        
        self.kpi_income.set_value(f"${summary['total_income']:,.2f}")
        self.kpi_expense.set_value(f"${summary['total_expense']:,.2f}")
        self.kpi_balance.set_value(f"${summary['balance']:,.2f}")
        
        # Draw Pie Chart
        self.ax_pie.clear()
        expenses = summary['expense_by_category']
        if expenses:
            labels = list(expenses.keys())
            sizes = list(expenses.values())
            self.ax_pie.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
            self.ax_pie.set_title("Gastos por Categoría")
        else:
            self.ax_pie.text(0.5, 0.5, "Sin datos de gastos", horizontalalignment='center', verticalalignment='center')
        self.canvas_pie.draw()
        
        # Draw Bar Chart
        self.ax_bar.clear()
        monthly = summary['monthly_summary']
        if monthly:
            months = sorted(list(monthly.keys()))
            incomes = [monthly[m]['income'] for m in months]
            expenses_list = [monthly[m]['expense'] for m in months]
            x = range(len(months))
            width = 0.35
            
            self.ax_bar.bar([i - width/2 for i in x], incomes, width, label='Ingresos', color='#28a745')
            self.ax_bar.bar([i + width/2 for i in x], expenses_list, width, label='Gastos', color='#dc3545')
            
            self.ax_bar.set_xticks(x)
            self.ax_bar.set_xticklabels(months)
            self.ax_bar.legend()
            self.ax_bar.set_title("Ingresos vs Gastos por Mes")
        else:
            self.ax_bar.text(0.5, 0.5, "Sin datos mensuales", horizontalalignment='center', verticalalignment='center')
        self.canvas_bar.draw()
