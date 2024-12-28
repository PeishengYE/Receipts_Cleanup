import sys
import os
import csv
import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QFileDialog, QMenuBar, QCheckBox,
 QFormLayout, QMessageBox, QRadioButton, QButtonGroup,QGroupBox 
)
from PyQt5.QtGui import QPixmap, QImageReader, QMouseEvent
from PyQt5.QtCore import Qt, QPoint

default_folder = "/mnt/largeDisk1/work/tax_receipts_cleanup/20240801_receipts/"
GST_RATE = 0.05
QST_RATE = 0.09975


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
        self.filename_label.setWordWrap(True)

        self.image_label = QLabel("No Image Loaded", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black;")

        self.prev_button = QPushButton("Prev")
        self.next_button = QPushButton("Next")
        self.exit_button = QPushButton("Exit")
        self.prev_button.clicked.connect(self.show_prev_image)
        self.next_button.clicked.connect(self.show_next_image)
        self.exit_button.clicked.connect(self.close_application)

        ############################################################
        self.rename_input = QLineEdit()
        self.rename_input.setPlaceholderText("Enter description")
        self.rename_button = QPushButton("OK")
        self.rename_button.clicked.connect(self.rename_and_next)

        self.control_buttons_widget_container = QWidget(self)

        ############################################################
        # Create a form layout for the label and line edit

        self.year_input = QLineEdit()
        self.year_input.setText("2024") 
        self.date_input = QLineEdit()
        self.amount = QLineEdit()
        self.tax_GST = QLineEdit()
        self.tax_QST = QLineEdit()
        self.description_input = QLineEdit("EX. Restaurant")



        topLayout = QFormLayout()
        topLayout.addRow("YEAR:", self.year_input)
        topLayout.addRow("DATE:", self.date_input)
        topLayout.addRow("Amount after GSTQST:", self.amount)
        topLayout.addRow("TVP/GST:", self.tax_GST)
        topLayout.addRow("TVQ/QST:", self.tax_QST)
        topLayout.addRow("DESC (NO SPACE): ", self.description_input)

        #############################################
        # Description Option group with radio buttons
        self.desc_option_group = QButtonGroup(self)

        self.radio_swimming = QRadioButton("Swimming")
        self.radio_walmart = QRadioButton("Walmart")
        self.radio_gas = QRadioButton("Gas")
        self.radio_costco = QRadioButton("Costco")
        self.radio_hotel = QRadioButton("Hotel")
        self.radio_unknown = QRadioButton("Unknown")
        self.radio_from_input = QRadioButton("From recepit description")

        self.desc_option_group.addButton(self.radio_swimming)
        self.desc_option_group.addButton(self.radio_gas)
        self.desc_option_group.addButton(self.radio_costco)
        self.desc_option_group.addButton(self.radio_hotel)
        self.desc_option_group.addButton(self.radio_walmart)
        self.desc_option_group.addButton(self.radio_from_input)
        self.desc_option_group.addButton(self.radio_unknown)

        self.radio_unknown.setChecked(True)  # Set a default selection

        optionDescLayout = QVBoxLayout()
        optionDescLayout.addWidget(self.radio_swimming)
        optionDescLayout.addWidget(self.radio_gas)
        optionDescLayout.addWidget(self.radio_costco)
        optionDescLayout.addWidget(self.radio_hotel)
        optionDescLayout.addWidget(self.radio_walmart)
        optionDescLayout.addWidget(self.radio_from_input)
        optionDescLayout.addWidget(self.radio_unknown)

        #############################################
        ############   CATEGORY OPTION ##############
        #############################################
        self.category_option_group = QButtonGroup(self)
        self.radio_computer = QRadioButton("Computer expenses")
        self.radio_professional = QRadioButton("Professional fee")
        self.radio_tele = QRadioButton("Tele communication")
        self.radio_adver = QRadioButton("advertising & promotion")
        self.radio_membership = QRadioButton("membership")
        self.radio_registration = QRadioButton("registration fee")
        self.radio_incorporation = QRadioButton("Incorporation cost")
        self.radio_parking = QRadioButton("Parking")
        self.radio_travel = QRadioButton("Business travel")
        self.radio_office = QRadioButton("Office supplies")
        self.radio_training = QRadioButton("Training")
        self.radio_meals = QRadioButton("Meals & entertainment")
        self.radio_soft = QRadioButton("Software")

        self.csv_report_group = QGroupBox("CSV Report")
        optionCategoryLayout = QVBoxLayout()
        optionCategoryLayout.addWidget(self.radio_computer)
        optionCategoryLayout.addWidget(self.radio_professional)
        optionCategoryLayout.addWidget(self.radio_tele)
        optionCategoryLayout.addWidget(self.radio_adver)
        optionCategoryLayout.addWidget(self.radio_membership)
        optionCategoryLayout.addWidget(self.radio_registration)
        optionCategoryLayout.addWidget(self.radio_incorporation)
        optionCategoryLayout.addWidget(self.radio_parking)
        optionCategoryLayout.addWidget(self.radio_travel)
        optionCategoryLayout.addWidget(self.radio_office)
        optionCategoryLayout.addWidget(self.radio_training)
        optionCategoryLayout.addWidget(self.radio_meals)
        optionCategoryLayout.addWidget(self.radio_soft)



        #############################################
        ############   CATEGORY OPTION ##############
        #############################################


        self.rename_file_button = QPushButton("Rename File")
        self.rename_file_button.clicked.connect(self.validate_and_process_input)

        outerLayout = QVBoxLayout()
        outerLayout.addLayout(topLayout)
        outerLayout.addLayout(optionDescLayout)

        outerLayout.addWidget(self.rename_file_button)

        #self.category_label = QLabel("CSV Report Category")
        #outerLayout.addWidget(self.category_label)
        self.button_layout = QHBoxLayout()
        self.calc_button = QPushButton("Calculate Taxes")
        self.calc_button.clicked.connect(self.calculate_taxes)
        self.button_layout.addWidget(self.calc_button)

        self.report_button = QPushButton("Generate Report")
        self.report_button.clicked.connect(self.generate_report)
        self.button_layout.addWidget(self.report_button)

        optionCategoryLayout.addLayout(self.button_layout)


        self.csv_report_group.setLayout(optionCategoryLayout)
        outerLayout.addWidget(self.csv_report_group)



        self.control_buttons_widget_container.setLayout(outerLayout)





        ############################################################




        center_layout = QHBoxLayout()
        center_layout.addWidget(self.image_label, stretch=1)
        center_layout.addWidget(self.control_buttons_widget_container, stretch=0)

        self.center_horizental_widget_container = QWidget(self)
        self.center_horizental_widget_container.setLayout(center_layout)


        next_prev_layout = QHBoxLayout()
        next_prev_layout.addWidget(self.prev_button)
        next_prev_layout.addWidget(self.next_button)
        next_prev_layout.addWidget(self.exit_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.filename_label, stretch=0)
        main_layout.addWidget(self.center_horizental_widget_container, stretch = 4)
        main_layout.addLayout(next_prev_layout, stretch = 1)

        self.central_widget.setLayout(main_layout)

        self.menu_bar = self.menuBar()
        self.menubar = self.menu_bar.addMenu("Recipt Folder")

        open_folder_action = self.menubar.addAction("Open Folder")
        open_folder_action.triggered.connect(self.open_folder)

        fullscreen_action = self.menubar.addAction("Toggle Fullscreen")
        fullscreen_action.triggered.connect(self.toggle_fullscreen)

    def calculate_taxes(self):
        try:
            total_amount = float(self.amount.text())
            gst = round(total_amount * GST_RATE / (1 + GST_RATE + QST_RATE), 2)
            qst = round(total_amount * QST_RATE / (1 + GST_RATE + QST_RATE), 2)

            self.tax_GST.setText(f"{gst:.2f}")
            self.tax_QST.setText(f"{qst:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid final amount.")

    def is_valid_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def generate_report(self):
        date = self.date_input.text()
        year = self.year_input.text()
        description =  self.get_selected_desc_option()
        try:
            total_amount = float(self.amount.text())
            gst_text = self.tax_GST.text().strip()
            qst_text = self.tax_QST.text().strip()
            gst = float(gst_text)
            qst = float(qst_text)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid amount,GST,QST before generating the report.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Report", "", "CSV Files (*.csv)")

        if file_path:
            try:
                with open(file_path, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([year, date, description, total_amount, gst, qst])

                QMessageBox.information(self, "Success", "Report generated successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save report: {str(e)}")


    def get_incremented_file_path(self, file_path):
        """
        Check the input file path and return an incremented file path if the file already exists.

        :param file_path: Original file path to check.
        :return: A new file path with an incremented number if the file exists.
        """

        print(f"Input file_path:  {file_path}")
        if not os.path.exists(file_path):
               print(f"Input file_path not exist, return immediatly")
               return file_path
        else:
               print(f"Input file_path exist")

        directory, filename = os.path.split(file_path)
        name, ext = os.path.splitext(filename)

        # Regex to find an existing number at the end of the filename
        pattern = r"^(.*?)(_\d{2})?$"
        match = re.match(pattern, name)

        if match:
            base_name = match.group(1)  # The main part of the filename
            number = match.group(2)    # The existing number (if any)

            # Start incrementing from 1 if no number exists
            if number is None:
                increment = 1
            else:
                increment = int(number[1:]) + 1

            # Generate a new filename with the incremented number
            while True:
                new_name = f"{base_name}_{increment:02}{ext}"
                new_file_path = os.path.join(directory, new_name)
                if not os.path.exists(new_file_path):
                    return new_file_path
                increment += 1

        # If no match, return the original file path
        return file_path

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
        selected_desc_option = self.get_selected_desc_option()
        if not selected_desc_option:
            self.show_warning("Please select an option.")
            return

        image_path = self.image_files[self.current_index]
        _no_use, imagename = os.path.split(image_path)
        directory_name, image_ext = os.path.splitext(imagename)

        base_dir = os.path.dirname(image_path)

        filename = f"{year}_{date}_{selected_desc_option.upper()}{image_ext}"

        file_path = os.path.join(base_dir , filename)
        print(f"validate_and_process_input()>> :: file_path of required filename:  {file_path}")

        filename = os.path.basename(self.get_incremented_file_path(file_path))
        print(f"validate_and_process_input()>> :: after verifying available filename: required filename:  {filename}")


         # Show confirmation dialog
        confirmed = self.show_confirmation_dialog(filename)
        if confirmed:
            print("Great! Let's rename it")
            self.rename_and_next(filename)
        else:
            print("No change")

    def show_confirmation_dialog(self, filename):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Confirm")
        msg_box.setText(f"Rename the current file to \n{filename}")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        response = msg_box.exec_()
        return response == QMessageBox.Yes


    def get_selected_desc_option(self):
        if self.radio_swimming.isChecked():
            return "Swimming"
        elif self.radio_gas.isChecked():
            return "Gas"
        elif self.radio_costco.isChecked():
            return "Costco"
        elif self.radio_hotel.isChecked():
            return "Hotel"
        elif self.radio_walmart.isChecked():
            return "Walmart"
        elif self.radio_from_input.isChecked():
            desc_input = self.description_input.text().strip()
            return desc_input
        elif self.radio_unknown.isChecked():
            return "Unknown"
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


    def rename_and_next(self, new_filename):

        current_path = self.image_files[self.current_index]
        print(f"current_filename {current_path}")
        print(f"new_filename {new_filename}")

        folder = os.path.dirname(current_path)
        new_path = os.path.join(folder, new_filename)
        if not new_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            new_path += os.path.splitext(current_path)[1]  # Preserve original extension

        try:
            os.rename(current_path, new_path)
            self.image_files[self.current_index] = new_path

            # clear inputs
            self.year_input.setText("2024") 
            self.date_input.clear()
            self.amount_input.clear()
            self.radio_unknown.setChecked(True)  # Set a default selection

            self.show_next_image()
        except Exception as e:
            print(f"Error renaming file: {e}")


    def rename_and_next_2(self):
        new_name = self.rename_input.text().strip()
        if new_name:
            current_path = self.image_files[self.current_index]
            folder = os.path.dirname(current_path)
            new_path = os.path.join(folder, new_name)
            if not new_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                new_path += os.path.splitext(current_path)[1]  # Preserve original extension

            try:
                os.rename(current_path, new_path)
                self.image_files[self.current_index] = new_path
                self.rename_input.clear()
                self.show_next_image()
            except Exception as e:
                print(f"Error renaming file: {e}")


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

