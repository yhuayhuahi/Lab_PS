import sys
import os
import logging
from PySide6.QtWidgets import QApplication
from app.data.repository import JsonRepository
from app.logic.controller import FinanceController
from app.ui.main_window import MainWindow

def main():
    # Setup logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    
    app = QApplication(sys.argv)
    
    # Initialize data and logic
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    repository = JsonRepository(data_dir)
    controller = FinanceController(repository)
    
    # Initialize UI
    window = MainWindow(controller)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
