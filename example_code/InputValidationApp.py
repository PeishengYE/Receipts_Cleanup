from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QFormLayout, QVBoxLayout, QWidget, QMessageBox, QRadioButton, QButtonGroup, QHBoxLayout


class InputValidationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Input Validation with Options")
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.year_input = QLineEdit()
        self.date_input = QLineEdit()
        self.index_input = QLineEdit()

        # Create a form layout for the label and line edit
        topLayout = QFormLayout()
        topLayout.addRow("YEAR:", self.year_input)
        topLayout.addRow("DATE:", self.date_input)
        topLayout.addRow("INDEX:", self.index_input)

        # Option group with radio buttons
        self.option_group = QButtonGroup(self)

        self.radio_swimming = QRadioButton("Swimming")
        self.radio_gas = QRadioButton("Gas")
        self.radio_costco = QRadioButton("Costco")
        self.radio_hotel = QRadioButton("Hotel")

        self.option_group.addButton(self.radio_swimming)
        self.option_group.addButton(self.radio_gas)
        self.option_group.addButton(self.radio_costco)
        self.option_group.addButton(self.radio_hotel)

        self.radio_gas.setChecked(True)  # Set a default selection

        optionLayout = QHBoxLayout()
        optionLayout.addWidget(self.radio_swimming)
        optionLayout.addWidget(self.radio_gas)
        optionLayout.addWidget(self.radio_costco)
        optionLayout.addWidget(self.radio_hotel)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.validate_and_process_input)

        layout = QVBoxLayout()
        layout.addLayout(topLayout)
        layout.addLayout(optionLayout)
        layout.addWidget(self.ok_button)

        self.central_widget.setLayout(layout)

    def validate_and_process_input(self):
        year = self.year_input.text().strip()
        date = self.date_input.text().strip()

        if not self.is_valid_year(year):
            self.show_warning("YEAR must be 2024 or 2025.")
            return

        if not self.is_valid_date(date):
            self.show_warning("DATE must be in MMDD format (e.g., 1122 for November 22).")
            return

        # Get selected option
        selected_option = self.get_selected_option()
        if not selected_option:
            self.show_warning("Please select an option.")
            return

        filename = f"{year}_{date}_{selected_option.upper()}.jpeg"

        # Show confirmation dialog
        confirmed = self.show_confirmation_dialog(filename)
        if confirmed:
            print("Great! Let's rename it")
        else:
            print("No change")

    def get_selected_option(self):
        if self.radio_swimming.isChecked():
            return "Swimming"
        elif self.radio_gas.isChecked():
            return "Gas"
        elif self.radio_costco.isChecked():
            return "Costco"
        elif self.radio_hotel.isChecked():
            return "Hotel"
        return None

    @staticmethod
    def is_valid_year(year):
        return year in {"2024", "2025"}

    @staticmethod
    def is_valid_date(date):
        if len(date) != 4 or not date.isdigit():
            return False

        month, day = int(date[:2]), int(date[2:])
        return 1 <= month <= 12 and 1 <= day <= 31

    def show_warning(self, message):
        QMessageBox.warning(self, "Invalid Input", message)

    def show_confirmation_dialog(self, filename):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Confirm")
        msg_box.setText(f"Are you sure you want to process this file?\n{filename}")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        response = msg_box.exec_()
        return response == QMessageBox.Yes


if __name__ == "__main__":
    app = QApplication([])
    window = InputValidationApp()
    window.show()
    app.exec_()

