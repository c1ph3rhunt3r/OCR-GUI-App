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

## Building an Executable (Windows)

If you want to build a standalone executable (EXE) for Windows:

1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```

2. Icon options:
   - Generate a basic icon with `python generate_icon.py`
   - Use your own icon - simply place your .ico file in the project directory
   - Convert an existing image (.png, .jpg) to .ico using a converter tool or online service

3. Build the executable using the provided spec file:
   ```
   pyinstaller ocr_app.spec --clean
   ```
   If using your own icon, modify the `ocr_app.spec` file and change the `icon='icon.ico'` line to point to your icon file.

4. Find the executable in the `dist/OCR App` folder. You can run `OCR App.exe` without needing Python installed.

### Custom Icon

#### Using an existing image as icon
If you already have an image you want to use as icon:

1. Convert your image to .ico format using an online converter or a tool like:
   ```python
   from PIL import Image
   
   # Replace with your image path
   img = Image.open('your_image.png')
   img.save('custom_icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
   ```

2. Edit the spec file to point to your icon:
   ```python
   # Find this line in ocr_app.spec
   icon='icon.ico',
   # Change it to
   icon='custom_icon.ico',
   ```

#### Creating a custom icon with the script
The application uses a blue square icon with "OCR" text by default. If you want to create your own icon:

1. Edit the `generate_icon.py` script to customize the appearance (color, text, etc.)
2. Run `python generate_icon.py` to generate a new icon

### Troubleshooting the Build

- If you see a "No module named X" error, ensure all dependencies are in requirements.txt
- For issues with Tesseract, make sure to set the correct path in `ocr_app.py`
- If the executable doesn't run, try enabling the console with `console=True` in the spec file for debugging

## Customization

You can customize the OCR process by modifying the configuration in `ocr_app.py`. The current configuration uses:

- Grayscale conversion for better text recognition
- PSM mode 6 (assumes a single block of text)
- OEM mode 3 (default mode based on what's available) 