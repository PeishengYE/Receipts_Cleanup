import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QTextEdit, QLabel, QPushButton


class TextInputExample(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Single-line text input
        self.single_line_label = QLabel("Enter text (single line):")
        self.single_line_edit = QLineEdit()
        self.single_line_edit.setPlaceholderText("Type something...")
        layout.addWidget(self.single_line_label)
        layout.addWidget(self.single_line_edit)

        # Multi-line text input
        self.multi_line_label = QLabel("Enter text (multi-line):")
        self.multi_line_edit = QTextEdit()
        self.multi_line_edit.setPlaceholderText("Type multiple lines...")
        layout.addWidget(self.multi_line_label)
        layout.addWidget(self.multi_line_edit)

        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_text)
        layout.addWidget(self.submit_button)

        # Set layout
        self.setLayout(layout)
        self.setWindowTitle("PyQt Text Input Example")

    def submit_text(self):
        single_line_text = self.single_line_edit.text()
        multi_line_text = self.multi_line_edit.toPlainText()

        print(f"Single Line Text: {single_line_text}")
        print(f"Multi Line Text: {multi_line_text}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextInputExample()
    window.show()
    sys.exit(app.exec_())

