import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QMenuBar
)
from PyQt5.QtGui import QPixmap, QImageReader, QMouseEvent
from PyQt5.QtCore import Qt, QPoint

default_folder = "/mnt/largeDisk1/work/tax_receipts_cleanup/20240801_receipts/"

class ReceiptViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Receipt Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.current_index = 0
        self.image_files = []
        self.zoom_factor = 1.0
        self.max_zoom_factor = 0.4
        self.min_zoom_factor = 0.2
        self.prev_next_button_pressed = False

        self.pan_offset = QPoint(0, 0)
        self.last_mouse_pos = None
        self.last_image_label_height = 0

        self.init_ui()
        self.showFullScreen()

        self.load_folder(default_folder)


        
    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.filename_label = QLabel("", self)
        self.filename_label.setAlignment(Qt.AlignCenter)
        self.filename_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.image_label = QLabel("No Image Loaded", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black;")

        self.prev_button = QPushButton("Prev")
        self.next_button = QPushButton("Next")
        self.exit_button = QPushButton("Exit")
        self.prev_button.clicked.connect(self.show_prev_image)
        self.next_button.clicked.connect(self.show_next_image)
        self.exit_button.clicked.connect(self.close_application)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.exit_button)

        layout = QVBoxLayout()
        layout.addWidget(self.filename_label)
        layout.addWidget(self.image_label, stretch=1)
        layout.addLayout(button_layout)

        self.central_widget.setLayout(layout)

        self.menu_bar = self.menuBar()
        self.menubar = self.menu_bar.addMenu("Recipt Folder")

        open_folder_action = self.menubar.addAction("Open Folder")
        open_folder_action.triggered.connect(self.open_folder)

        fullscreen_action = self.menubar.addAction("Toggle Fullscreen")
        fullscreen_action.triggered.connect(self.toggle_fullscreen)

        
    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder with Receipts")

        if folder_path:
            self.load_folder(folder_path)

    def load_folder(self, folder_path):
        if folder_path:
            self.image_files = [
                os.path.join(folder_path, f)
                for f in os.listdir(folder_path)
                if f.lower().endswith((".jpg", ".jpeg", ".png"))
            ]
            self.image_files.sort()
            self.current_index = 0
            self.show_image(True)




    def show_image(self, just_load):
        if not self.image_files:
            self.image_label.setText("No Images Found")
            return

        image_path = self.image_files[self.current_index]
        self.filename_label.setText(os.path.basename(image_path))

        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            self.image_label.setText("Failed to load image")
        else:
            if just_load:
                self.zoom_factor = self.calculate_fit_zoom(pixmap)
                self.max_zoom_factor = self.zoom_factor
            self.update_image_display(pixmap)

    def calculate_fit_zoom(self, pixmap):
        # Calculate the zoom factor to fit the image within the QLabel
        label_width = self.image_label.width()
        label_height = self.image_label.height()
        print(f"Image label width: {label_width}")

        print(f"Image label height: {label_height}")
        print(f"Prev Image label height : {self.last_image_label_height}")

        height_diff =  label_height - self.last_image_label_height 
        print(f"Image label height changed with different: {height_diff}")

        if height_diff > 0 and height_diff < 3:
            print(f"Image label height changed, keep it to the previous value")
            label_height = self.last_image_label_height

        self.last_image_label_height = label_height

        pixmap_width = pixmap.width()
        pixmap_height = pixmap.height()

        width_ratio = label_width / pixmap_width
        height_ratio = label_height / pixmap_height

        zoom_factor_calculated = min(width_ratio, height_ratio)

        return zoom_factor_calculated
        


    def update_image_display(self, pixmap):
        scaled_pixmap = pixmap.scaled(
            pixmap.size() * self.zoom_factor,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        scaled_pixmap_width = scaled_pixmap.width()
        scaled_pixmap_height = scaled_pixmap.height()

        print(f"update_image_display()>> Scaled_Pixmap zoom_factor: {self.zoom_factor}")
        print(f"update_image_display()>> Scaled_Pixmap width: {scaled_pixmap_width}")
        print(f"update_image_display()>> Scaled_Pixmap height: {scaled_pixmap_height}")

        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.move(self.pan_offset)

    def show_prev_image(self):
        if self.image_files:
            self.current_index = (self.current_index - 1) % len(self.image_files)
            self.reset_zoom_and_pan()
            self.show_image(True)

    def show_next_image(self):
        if self.image_files:
            self.current_index = (self.current_index + 1) % len(self.image_files)
            self.reset_zoom_and_pan()
            self.show_image(True)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def reset_zoom_and_pan(self):
        self.zoom_factor = 1.0
        self.pan_offset = QPoint(0, 0)

    def close_application(self):
        QApplication.quit()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.zoom_factor *= 1.1
        else:
            self.zoom_factor /= 1.1

        if self.zoom_factor > self.max_zoom_factor:
           self.zoom_factor = self.max_zoom_factor

        if self.zoom_factor < self.min_zoom_factor: 
           self.zoom_factor = self.min_zoom_factor

        self.show_image(False)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.last_mouse_pos is not None and event.buttons() == Qt.LeftButton:
            delta = event.pos() - self.last_mouse_pos
            self.pan_offset += delta
            self.last_mouse_pos = event.pos()
            self.show_image(False)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ReceiptViewer()
    viewer.show()
    sys.exit(app.exec_())

