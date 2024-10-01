from PIL import Image, ImageDraw, ImageFont
import requests
import os
import time
import logging
import re
import textwrap
from io import BytesIO

def get_temp_image_path():
    temp_dir = os.path.join(os.path.dirname(__file__), "tmp")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return os.path.join(temp_dir, "temp_image.jpg")

def get_random_image():
    url = "https://t.mwm.moe/mp"
    response = requests.get(url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        return image
    else:
        raise Exception("Failed to fetch random image")

def resize_image_proportionally(image, base_width):
    width_ratio = base_width / image.width
    new_height = int(image.height * width_ratio)
    return image.resize((base_width, new_height), Image.Resampling.LANCZOS)

def create_image(text, background_url=None):
    font_path = 'G:\\桌面\\BOT\\library\\font\\Fort_1.ttf'
    font_size = 20
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        logging.error(f"Font file not found or cannot be opened. Please check the font path: {font_path}")
        return None
    image_width = 600
    padding = 50
    line_spacing = 10
    processed_text = re.sub(r'(\d+)\.', r'\1.\n', text)
    wrapped_lines = textwrap.wrap(processed_text, width=25)
    text_height = len(wrapped_lines) * (font_size + line_spacing) - line_spacing + 2 * padding
    if background_url:
        background_image = Image.open(background_url)
        if background_image.mode != 'RGBA':
            background_image = background_image.convert('RGBA')
    else:
        background_image = get_random_image()
        background_image = resize_image_proportionally(background_image, image_width)
        if background_image.mode != 'RGBA':
            background_image = background_image.convert('RGBA')
    text_image = Image.new("RGBA", background_image.size, (255, 255, 255, 98))
    draw = ImageDraw.Draw(text_image)
    current_height = padding
    for line in wrapped_lines:
        draw.text((padding, current_height), line, font=font, fill=(0, 0, 0))
        current_height += font_size + line_spacing
    combined_image = Image.alpha_composite(background_image, text_image)
    timestamp = time.strftime("%Y-%m-%d-%H.%M.%S")
    filename = f"G:\\桌面\\BOT\\tmp\\{timestamp}.png"
    combined_image.save(filename)
    print(f"Image saved to {filename}")
    return filename