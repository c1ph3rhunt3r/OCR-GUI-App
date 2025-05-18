import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def generate_ocr_icon():
    # Create a 256x256 image with a transparent background
    icon_size = 256
    icon = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    
    # Draw a rounded rectangle as background
    bg_color = (52, 152, 219)  # Blue
    border_radius = 30
    rect_size = icon_size - 40
    rect_pos = 20
    
    # Draw the rounded rectangle
    draw.rounded_rectangle(
        [(rect_pos, rect_pos), (rect_pos + rect_size, rect_pos + rect_size)],
        fill=bg_color,
        radius=border_radius
    )
    
    # Add text "OCR" in white
    try:
        # Try to use a built-in font
        font = ImageFont.truetype("arial.ttf", 120)
    except IOError:
        # Fallback to default font
        font = ImageFont.load_default().font_variant(size=120)
    
    draw.text((icon_size // 2, icon_size // 2), "OCR", fill="white", font=font, anchor="mm")
    
    # Save as .ico file
    icon.save("icon.ico", format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print("Icon created successfully.")

if __name__ == "__main__":
    generate_ocr_icon() 