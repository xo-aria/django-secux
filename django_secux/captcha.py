import random
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

def generate_captcha_text():
    return str(random.randint(10000, 99999))
  
def generate_captcha_image(text):
    width, height = 120, 50
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    font = ImageFont.load_default()
    
    text_width, text_height = draw.textsize(text, font=font)
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    draw.text((x, y), text, font=font, fill=(0, 0, 0))
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode()

def is_captcha_valid(request):
    user_input = request.POST.get('captcha_input', '').strip()
    expected = request.session.get('captcha_answer', '')
    return user_input == expected
