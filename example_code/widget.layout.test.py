import sys
from PyQt5.QtWidgets import \
    QApplication, QMainWindow, QWidget, QStatusBar, QMenuBar, QMenu, \
    QAction, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication


class UISimple(QMainWindow):
    def __init__(self, title="stretch 4 parts to 1"):
        super().__init__()

        self.showMaximized()
        self.setWindowTitle(title)

        # FIXME: is that necessary?
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.hlayout = QHBoxLayout(self.centralwidget)

        # Widget as a container for further views
        self.rename_input = QLineEdit()
        self.rename_input.setPlaceholderText("Enter new name for current image")
        self.rename_button = QPushButton("OK")

        edit_buttons_layout = QHBoxLayout()
        edit_buttons_layout.addWidget(self.rename_input)
        edit_buttons_layout.addWidget(self.rename_button)

        self.widget_container = QWidget(self.centralwidget)
        self.widget_container.setLayout(edit_buttons_layout)
        #self.widget_container.addWidget(edit_buttons_layout)



        self.hlayout.addWidget(self.widget_container, stretch=4)    # +
        #self.hlayout.addWidget(edit_buttons_layout, stretch=4)    # +

        # label for show some help
        self.label_help = QLabel(self.centralwidget)
        self.label_help.setStyleSheet("background-color: #B9E9BE")
        self.label_help.setWordWrap(True)                           # +
        self.hlayout.addWidget(self.label_help, stretch=1)          # +      

       
        # FIXME: label 1 and widget 4 parts of the window.
#        self.hlayout.setStretch(4, 1)
# ?        self.setLayout(self.hlayout)

    def setup(self):
        self._setup_main_window()

    def write_help(self, helptext):
        self.label_help.setText(helptext)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = UISimple()
    window.write_help("You need some help - so i'm in trouble!")
    sys.exit(app.exec_())
