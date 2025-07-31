from django import template
from django_secux import captcha

register = template.Library()

@register.simple_tag(takes_context=True)
def captcha_src(context):
    request = context['request']
    text = captcha.generate_captcha_text()
    request.session['captcha_answer'] = text
    image_data = captcha.generate_captcha_image(text)
    return f'data:image/png;base64,{image_data}'
