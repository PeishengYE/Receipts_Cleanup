import sys
import csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QFrame, QGroupBox
)
from PyQt5.QtCore import QDate

GST_RATE = 0.05
QST_RATE = 0.09975

class TaxCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tax Calculator and Report Generator")

        self.layout = QVBoxLayout()

        # Frame for Inputs
        self.input_group = QGroupBox("Input Area")
        self.input_layout = QVBoxLayout()

        # Date Input
        self.date_label = QLabel("Date (YYYY-MM-DD):")
        self.date_input = QLineEdit(QDate.currentDate().toString("yyyy-MM-dd"))
        self.input_layout.addWidget(self.date_label)
        self.input_layout.addWidget(self.date_input)

        # Description Input
        self.desc_label = QLabel("Description:")
        self.desc_input = QLineEdit()
        self.input_layout.addWidget(self.desc_label)
        self.input_layout.addWidget(self.desc_input)

        # Amount Input
        self.amount_label = QLabel("Final Amount (including GST and QST):")
        self.amount_input = QLineEdit()
        self.input_layout.addWidget(self.amount_label)
        self.input_layout.addWidget(self.amount_input)

        # GST/QST Display
        self.gst_label = QLabel("GST:")
        self.gst_output = QLineEdit()
        self.gst_output.setReadOnly(True)
        self.input_layout.addWidget(self.gst_label)
        self.input_layout.addWidget(self.gst_output)

        self.qst_label = QLabel("QST:")
        self.qst_output = QLineEdit()
        self.qst_output.setReadOnly(True)
        self.input_layout.addWidget(self.qst_label)
        self.input_layout.addWidget(self.qst_output)

        self.input_group.setLayout(self.input_layout)
        self.layout.addWidget(self.input_group)

        # Buttons
        self.button_layout = QHBoxLayout()

        self.calc_button = QPushButton("Calculate Taxes")
        self.calc_button.clicked.connect(self.calculate_taxes)
        self.button_layout.addWidget(self.calc_button)

        self.report_button = QPushButton("Generate Report")
        self.report_button.clicked.connect(self.generate_report)
        self.button_layout.addWidget(self.report_button)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

    def calculate_taxes(self):
        try:
            total_amount = float(self.amount_input.text())
            gst = round(total_amount * GST_RATE / (1 + GST_RATE + QST_RATE), 2)
            qst = round(total_amount * QST_RATE / (1 + GST_RATE + QST_RATE), 2)

            self.gst_output.setText(f"{gst:.2f}")
            self.qst_output.setText(f"{qst:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid final amount.")

    def generate_report(self):
        date = self.date_input.text()
        description = self.desc_input.text()
        try:
            total_amount = float(self.amount_input.text())
            gst = round(total_amount * GST_RATE / (1 + GST_RATE + QST_RATE), 2)
            qst = round(total_amount * QST_RATE / (1 + GST_RATE + QST_RATE), 2)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid final amount before generating the report.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Report", "", "CSV Files (*.csv)")

        if file_path:
            try:
                with open(file_path, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([date, description, total_amount, gst, qst])

                QMessageBox.information(self, "Success", "Report generated successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save report: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaxCalculator()
    window.show()
    sys.exit(app.exec_())

