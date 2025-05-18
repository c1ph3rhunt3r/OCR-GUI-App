import sys
import os
import pytesseract
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, 
                            QWidget, QFileDialog, QTextEdit, QLabel, QMessageBox, QGroupBox,
                            QCheckBox)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QRect, QTimer
from PIL import Image
import pyperclip
import mss
import mss.tools
from datetime import datetime
from alt_screenshot import ScreenCapture

# Set Tesseract executable path - adjust this path based on your installation location
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# If you installed it in a different location, update the path accordingly
# Examples:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
# pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'

class OCRApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("OCR Application")
        self.setGeometry(100, 100, 800, 600)
        
        self.image_path = None
        self.extracted_text = ""
        self.is_screenshot = False  # Flag to track if current image is a screenshot
        
        self.init_ui()
    
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        
        # Image group
        image_group = QGroupBox("Image")
        image_layout = QVBoxLayout()
        
        # Image preview
        self.image_label = QLabel("No image selected")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(200)
        self.image_label.setStyleSheet("border: 1px solid #cccccc;")
        image_layout.addWidget(self.image_label)
        
        # Image buttons
        btn_layout = QHBoxLayout()
        self.btn_load_image = QPushButton("Load Image")
        self.btn_load_image.clicked.connect(self.load_image)
        self.btn_screenshot = QPushButton("Take Screenshot")
        self.btn_screenshot.clicked.connect(self.take_screenshot)
        self.btn_recapture = QPushButton("Recapture")
        self.btn_recapture.clicked.connect(self.recapture_screenshot)
        self.btn_recapture.setEnabled(False)
        self.btn_remove_image = QPushButton("Remove Image")
        self.btn_remove_image.clicked.connect(self.remove_image)
        self.btn_remove_image.setEnabled(False)
        self.btn_extract = QPushButton("Extract Text")
        self.btn_extract.clicked.connect(self.extract_text)
        self.btn_extract.setEnabled(False)
        
        btn_layout.addWidget(self.btn_load_image)
        btn_layout.addWidget(self.btn_screenshot)
        btn_layout.addWidget(self.btn_recapture)
        btn_layout.addWidget(self.btn_remove_image)
        btn_layout.addWidget(self.btn_extract)
        
        image_layout.addLayout(btn_layout)
        
        # Auto-cleanup option 
        self.auto_cleanup_checkbox = QCheckBox("Auto-remove screenshots after text extraction")
        self.auto_cleanup_checkbox.setChecked(True)  # Default to checked
        self.auto_cleanup_checkbox.setToolTip(
            "When checked, screenshots taken with the app will be automatically deleted after text extraction.\n"
            "This does not affect images loaded from files."
        )
        image_layout.addWidget(self.auto_cleanup_checkbox)
        
        image_group.setLayout(image_layout)
        main_layout.addWidget(image_group)
        
        # Text group
        text_group = QGroupBox("Extracted Text")
        text_layout = QVBoxLayout()
        
        # Text display
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(False)
        self.text_display.setMinimumHeight(200)
        text_layout.addWidget(self.text_display)
        
        # Text buttons
        text_btn_layout = QHBoxLayout()
        self.btn_copy = QPushButton("Copy to Clipboard")
        self.btn_copy.clicked.connect(self.copy_to_clipboard)
        self.btn_copy.setEnabled(False)
        self.btn_save = QPushButton("Save to File")
        self.btn_save.clicked.connect(self.save_to_file)
        self.btn_save.setEnabled(False)
        
        text_btn_layout.addWidget(self.btn_copy)
        text_btn_layout.addWidget(self.btn_save)
        
        text_layout.addLayout(text_btn_layout)
        text_group.setLayout(text_layout)
        main_layout.addWidget(text_group)
        
        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
    def load_image(self):
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )
        
        if image_path:
            self.image_path = image_path
            self.is_screenshot = False  # Mark as not a screenshot
            self.display_image(image_path)
            self.btn_extract.setEnabled(True)
            self.btn_remove_image.setEnabled(True)
            self.btn_recapture.setEnabled(False)  # Disable recapture for loaded images
    
    def take_screenshot(self):
        # Minimize the window to avoid it being in the screenshot
        self.showMinimized()
        
        # Add a small delay to ensure the window is minimized
        QTimer.singleShot(500, self._take_screenshot)
    
    def recapture_screenshot(self):
        """Recapture a screenshot if the previous one was not satisfactory"""
        # First remove the current screenshot if it exists
        if self.is_screenshot and self.image_path and os.path.exists(self.image_path):
            try:
                os.remove(self.image_path)
            except Exception as e:
                print(f"Error deleting previous screenshot: {str(e)}")
        
        # Now take a new screenshot
        self.take_screenshot()
    
    def _take_screenshot(self):
        self.screen_capture = ScreenCapture()
        self.screen_capture.screenshot_taken.connect(self.process_screenshot)
        self.screen_capture.start()
    
    def process_screenshot(self, screenshot):
        if screenshot is not None:
            # Generate a temporary filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_path = f"screenshot_{timestamp}.png"
            
            # Save the screenshot
            screenshot.save(temp_path)
            self.image_path = temp_path
            self.is_screenshot = True  # Mark as a screenshot
            self.display_image(temp_path)
            self.btn_extract.setEnabled(True)
            self.btn_remove_image.setEnabled(True)
            self.btn_recapture.setEnabled(True)  # Enable recapture for screenshots
        
        # Restore window state
        self.showNormal()
        self.activateWindow()  # Bring window to front
    
    def remove_image(self):
        # Store screenshot path before clearing
        screenshot_to_delete = None
        if self.is_screenshot and self.image_path and os.path.exists(self.image_path):
            screenshot_to_delete = self.image_path
        
        # Clear the image
        self.image_path = None
        self.is_screenshot = False
        self.image_label.setText("No image selected")
        self.image_label.setPixmap(QPixmap())  # Clear the pixmap
        
        # Disable buttons that require an image
        self.btn_extract.setEnabled(False)
        self.btn_remove_image.setEnabled(False)
        self.btn_recapture.setEnabled(False)
        
        # Also clear text if there was any
        if self.text_display.toPlainText():
            if QMessageBox.question(self, "Clear Text", 
                                   "Do you want to clear the extracted text as well?",
                                   QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                self.text_display.clear()
                self.btn_copy.setEnabled(False)
                self.btn_save.setEnabled(False)
        
        # Delete the screenshot file if it exists
        if screenshot_to_delete:
            try:
                os.remove(screenshot_to_delete)
            except Exception as e:
                print(f"Error deleting screenshot file: {str(e)}")
    
    def display_image(self, image_path):
        pixmap = QPixmap(image_path)
        
        # Scale pixmap to fit the label while maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(
            self.image_label.width(), self.image_label.height(), 
            Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        )
        
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
    
    def extract_text(self):
        if not self.image_path:
            QMessageBox.warning(self, "Warning", "No image selected.")
            return
        
        try:
            # Perform OCR with improved image processing
            image = Image.open(self.image_path)
            
            # Improve image for better OCR results
            # Convert to grayscale for better text recognition
            # pytesseract works better with grayscale images
            image = image.convert('L')
            
            # Use psm mode 6 (assuming a single uniform block of text)
            # and oem mode 3 (default, based on what's available)
            config = '--psm 6 --oem 3'
            self.extracted_text = pytesseract.image_to_string(image, config=config)
            
            # Update text display
            self.text_display.setText(self.extracted_text)
            
            # Enable buttons
            self.btn_copy.setEnabled(True)
            self.btn_save.setEnabled(True)
            
            # Auto cleanup screenshot if enabled and it's a screenshot
            if self.auto_cleanup_checkbox.isChecked() and self.is_screenshot:
                screenshot_path = self.image_path
                self.image_path = None
                self.is_screenshot = False
                self.image_label.setText("No image selected")
                self.image_label.setPixmap(QPixmap())  # Clear the pixmap
                self.btn_extract.setEnabled(False)
                self.btn_remove_image.setEnabled(False)
                self.btn_recapture.setEnabled(False)
                
                # Delete the screenshot file
                try:
                    os.remove(screenshot_path)
                except Exception as e:
                    print(f"Error deleting screenshot file: {str(e)}")
            
            QMessageBox.information(self, "Success", "Text extracted successfully!")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to extract text: {str(e)}")
    
    def copy_to_clipboard(self):
        if self.text_display.toPlainText():
            pyperclip.copy(self.text_display.toPlainText())
            QMessageBox.information(self, "Success", "Text copied to clipboard!")
    
    def save_to_file(self):
        if not self.text_display.toPlainText():
            QMessageBox.warning(self, "Warning", "No text to save.")
            return
        
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self, "Save Text", "", "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.text_display.toPlainText())
                QMessageBox.information(self, "Success", f"Text saved to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OCRApp()
    window.show()
    sys.exit(app.exec_()) 