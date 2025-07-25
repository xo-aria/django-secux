import os
import io
from PIL import Image
from datetime import datetime, timedelta
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils.http import http_date

@csrf_exempt
def cdn_serve(request, file_path):
    if request.method != 'GET':
        return _svg_error()

    file_path = file_path.strip()
    if '..' in file_path or file_path.startswith('/'):
        return _svg_error()

    abs_requested_path = os.path.abspath(os.path.join(settings.BASE_DIR, file_path))
    print(abs_requested_path)

    allowed = False
    for base in getattr(settings, 'SECUX_STATIC', []):
        base_path = os.path.abspath(base)
        try:
            if os.path.commonpath([abs_requested_path, base_path]) == base_path:
                allowed = True
                break
        except ValueError:
            continue 

    if not allowed or not os.path.isfile(abs_requested_path):
        return _svg_error()

    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext in ['.png', '.jpg', '.jpeg', '.webp', '.gif']:
            return _serve_resized_image(request, abs_requested_path, ext)
        elif ext in ['.css', '.js']:
            return _serve_minified_file(request, abs_requested_path, ext)
        else:
            return _serve_raw_file(abs_requested_path, ext)
    except:
        print(f"Error processing file {abs_requested_path}: {str(e)}")
        return _svg_error()


def _svg_error():
    return HttpResponse(
        'Not found',
        content_type='text/plain',
        status=404,
        headers={
            'Cache-Control': 'no-cache, no-store',
        }
    )

def _serve_resized_image(request, full_path, ext):
    size = request.GET.get('size', '').strip()
    size = int(size) if size else None
    img = Image.open(full_path)
    if img.mode not in ['RGB', 'RGBA']:
        img = img.convert('RGBA' if img.format in ['PNG', 'WEBP'] else 'RGB')
    if size:
        img.thumbnail((size, size), Image.LANCZOS)

    output = io.BytesIO()
    fmt = img.format or ext.replace('.', '').upper()
    img.save(output, format=fmt)
    output.seek(0)

    expires = datetime.utcnow() + timedelta(days=1)
    return HttpResponse(
        output.read(),
        content_type=f'image/{fmt.lower()}',
        headers={
            'Cache-Control': 'public, max-age=86400',
            'Expires': http_date(expires.timestamp()),
        }
    )

def _serve_minified_file(request, full_path, ext):
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if ext == '.css':
        content = _minify_css(content)
        content_type = 'text/css'
    else:
        content = _minify_js(content)
        content_type = 'application/javascript'

    expires = datetime.utcnow() + timedelta(minutes=60)
    return HttpResponse(
        content,
        content_type=content_type,
        headers={
            'Cache-Control': 'public, max-age=3600',
            'Expires': http_date(expires.timestamp()),
        }
    )

def _serve_raw_file(full_path, ext):
    content_type = {
        '.svg': 'image/svg+xml',
        '.woff2': 'font/woff2',
        '.woff': 'font/woff',
        '.ttf': 'font/ttf',
        '.eot': 'application/vnd.ms-fontobject',
    }.get(ext, 'application/octet-stream')

    with open(full_path, 'rb') as f:
        content = f.read()

    expires = datetime.utcnow() + timedelta(minutes=60)
    return HttpResponse(
        content,
        content_type=content_type,
        headers={
            'Cache-Control': 'public, max-age=3600',
            'Expires': http_date(expires.timestamp()),
        }
    )

def _minify_css(css):
    return ''.join(line.strip() for line in css.splitlines() if line.strip() and not line.strip().startswith('/*'))

def _minify_js(js):
    return ''.join(line.strip() for line in js.splitlines() if line.strip() and not line.strip().startswith('//'))
