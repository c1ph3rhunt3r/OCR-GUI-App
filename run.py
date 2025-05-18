#!/usr/bin/env python3

"""
OCR GUI Application Launcher
This script launches the OCR GUI application.
"""

import sys
import os
import subprocess
import platform

def check_tesseract():
    """Check if Tesseract is installed and provide installation instructions if not."""
    try:
        import pytesseract
        # Skip version check - we'll rely on the explicit path in ocr_app.py
        return True
    except Exception:
        print("Tesseract OCR is not installed or not properly configured.")
        system = platform.system()
        
        if system == "Windows":
            print("\nInstallation instructions for Windows:")
            print("1. Download Tesseract installer from: https://github.com/UB-Mannheim/tesseract/wiki")
            print("2. Run the installer and complete the installation")
            print("3. Ensure the Tesseract installation directory is in your PATH")
            print("\nAlternatively, you can edit ocr_app.py to set the correct path to tesseract.exe")
        elif system == "Darwin":  # macOS
            print("\nInstallation instructions for macOS:")
            print("1. Install Homebrew if not already installed: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
            print("2. Install Tesseract: brew install tesseract")
        elif system == "Linux":
            print("\nInstallation instructions for Linux (Ubuntu/Debian):")
            print("1. Install Tesseract: sudo apt install tesseract-ocr")
            print("\nFor other Linux distributions, please check your package manager.")
        
        return False

def check_dependencies():
    """Check if all required Python packages are installed."""
    try:
        # Try to import each package directly
        import PIL
        import pytesseract
        import PyQt5
        import pyperclip
        import mss
        return True
    except ImportError as e:
        print(f"Missing dependency: {str(e)}")
        print("\nYou can install all dependencies with:")
        print("pip install -r requirements.txt")
        return False

def main():
    """Main function to launch the OCR application."""
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check if Tesseract is installed
    if not check_tesseract():
        return
    
    # Launch the OCR application
    try:
        from ocr_app import OCRApp
        from PyQt5.QtWidgets import QApplication
        
        app = QApplication(sys.argv)
        window = OCRApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error launching the application: {str(e)}")

if __name__ == "__main__":
    main() 