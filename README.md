# OCR GUI Application

A simple GUI application for Optical Character Recognition (OCR) that allows users to:

- Select an image from their computer
- Take a screenshot of a screen region
- Recapture a screenshot if needed
- Extract text from the image
- Copy text to clipboard
- Save text to a file
- Remove images and reset the application
- Automatically clean up screenshots after text extraction

## Requirements

- Python 3.8+
- Tesseract OCR engine

## Installation

1. Install Tesseract OCR:
   - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
   - macOS: `brew install tesseract`
   - Linux: `sudo apt install tesseract-ocr`

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application with:
```
python run.py
```

## Features

- **Load Image**: Select an image file containing text for OCR processing
- **Take Screenshot**: Capture a specific region of your screen for OCR processing
- **Recapture**: Take a new screenshot if you captured the wrong area
- **Remove Image**: Clear the current image if you want to select a different one
- **Extract Text**: Use OCR to extract text from the loaded image
- **Copy to Clipboard**: Copy the extracted text to your clipboard
- **Save to File**: Save the extracted text to a text file
- **Auto-cleanup**: Automatically remove screenshot files after text extraction to avoid clutter (only affects screenshots taken through the app, not loaded images) 