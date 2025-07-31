import random
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

def generate_captcha_text():
    return str(random.randint(10000, 99999))

def generate_captcha_image(text):
    width, height = 120, 40
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    for _ in range(5):
        draw.line(
            [(random.randint(0, width), random.randint(0, height)), 
             (random.randint(0, width), random.randint(0, height))],
            fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 
            width=1
        )
    
    for _ in range(100):
        draw.point(
            (random.randint(0, width), random.randint(0, height)), 
            fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        )

    draw.text((x, y), text, font=font, fill=(0, 0, 0))
    
    img = img.filter(ImageFilter.SMOOTH)

    buffer = BytesIO()
    img.save(buffer, format='PNG', quality=95)
    return base64.b64encode(buffer.getvalue()).decode()

def is_captcha_valid(request):
    user_input = request.POST.get('secux_captcha_input', '').strip()
    expected = request.session.get('captcha_answer', '')
    return user_input == expected
