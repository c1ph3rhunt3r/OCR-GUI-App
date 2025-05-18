import sys
import mss
import mss.tools
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                            QLabel, QMainWindow, QComboBox)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint, QRect, pyqtSignal, QTimer, QObject

class ScreenCapture(QObject):
    screenshot_taken = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        self.screen_selector = ScreenSelector()
        self.screen_selector.region_selected.connect(self.capture_region)
    
    def start(self):
        # Start the screen selection process
        self.screen_selector.showFullScreen()
    
    def capture_region(self, region):
        """Capture the selected region of the screen"""
        if region is None:
            self.screenshot_taken.emit(None)
            return
            
        try:
            x, y, width, height = region
            
            # Ensure dimensions are valid
            if width < 1 or height < 1:
                self.screenshot_taken.emit(None)
                return
                
            # Use native QScreen method for better quality
            screen = QApplication.primaryScreen()
            if screen:
                # Capture the screenshot using QScreen for better quality
                screenshot = screen.grabWindow(0, x, y, width, height)
                
                # Emit the captured screenshot
                self.screenshot_taken.emit(screenshot)
                return
                
            # Fallback to mss if QScreen fails
            with mss.mss() as sct:
                # Define the region to capture
                monitor = {"top": y, "left": x, "width": width, "height": height}
                
                # Capture the specified region
                sct_img = sct.grab(monitor)
                
                # Convert to QPixmap for Qt compatibility
                # Use RGB format (without alpha channel)
                img_array = np.array(sct_img)
                height, width, _ = img_array.shape
                bytes_per_line = 4 * width
                
                img = QImage(sct_img.rgb, width, height, bytes_per_line, QImage.Format_RGBA8888)
                pixmap = QPixmap.fromImage(img)
                
                # Emit the captured screenshot
                self.screenshot_taken.emit(pixmap)
                
        except Exception as e:
            print(f"Screenshot error: {str(e)}")
            self.screenshot_taken.emit(None)


class ScreenSelector(QWidget):
    region_selected = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        
        # Make fullscreen widget with translucent background
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 30);")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(Qt.CrossCursor)
        
        # Initialize selection variables
        self.begin = QPoint()
        self.end = QPoint()
        self.is_selecting = False
        
        # Add text instructions
        self.help_label = QLabel("Click and drag to select an area. Press Esc to cancel.", self)
        self.help_label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 150); padding: 5px;")
        self.help_label.move(10, 10)
        self.help_label.setFixedWidth(400)
        self.help_label.adjustSize()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Main background
        painter.fillRect(self.rect(), QColor(0, 0, 0, 30))
        
        # If we're selecting, draw the selection rectangle
        if self.is_selecting:
            # Get the selection rectangle
            selected_rect = QRect(self.begin, self.end)
            
            # Clear the area inside the selection
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.fillRect(selected_rect, Qt.transparent)
            
            # Reset composition and draw border
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            painter.setPen(QPen(QColor(255, 255, 255), 2))
            painter.drawRect(selected_rect)
            
            # Draw dimensions text
            width = abs(self.end.x() - self.begin.x())
            height = abs(self.end.y() - self.begin.y())
            dim_text = f"{width} x {height}"
            
            # Position the text near the selection
            text_x = min(self.begin.x(), self.end.x())
            text_y = min(self.begin.y(), self.end.y()) - 20
            if text_y < 10:
                text_y = min(self.begin.y(), self.end.y()) + height + 20
                
            # Draw the text with background
            text_rect = QRect(text_x, text_y, 100, 20)
            painter.fillRect(text_rect, QColor(0, 0, 0, 150))
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(text_rect, Qt.AlignCenter, dim_text)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.begin = event.pos()
            self.end = event.pos()
            self.is_selecting = True
            self.update()
    
    def mouseMoveEvent(self, event):
        if self.is_selecting:
            self.end = event.pos()
            self.update()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_selecting:
            self.end = event.pos()
            self.is_selecting = False
            
            # Calculate selection coordinates
            x1 = min(self.begin.x(), self.end.x())
            y1 = min(self.begin.y(), self.end.y())
            width = abs(self.end.x() - self.begin.x())
            height = abs(self.end.y() - self.begin.y())
            
            # Validate selection size
            if width >= 10 and height >= 10:
                # Hide this window before capturing to avoid it being in the screenshot
                self.hide()
                QApplication.processEvents()
                
                # Emit the selected region
                self.region_selected.emit((x1, y1, width, height))
                self.close()
            else:
                # Selection too small, cancel
                self.region_selected.emit(None)
                self.close()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.region_selected.emit(None)
            self.close()