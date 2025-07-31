from functools import wraps
from django.http import HttpResponse
from django.utils.timezone import now
from .models import PageRequestLog
from django.conf import settings
from .signals import attack_detected

DEFAULT_MESSAGES = {
    "blocked": "This page is temporarily blocked. Please try again later.",
    "rate_exceeded": "Rate limit exceeded. This page is blocked temporarily.",
}

def js_challenge(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.COOKIES.get('js_verified') == 'true':
            return view_func(request, *args, **kwargs)

        if 'js_verified=true' in request.META.get('HTTP_COOKIE', ''):
            return view_func(request, *args, **kwargs)

        js_code = f"""
        <script>
            document.cookie = "js_verified=true; path=/";
            window.location.href = "{request.get_full_path()}";
        </script>
        <noscript>
            <h3>JavaScript is required to access this content.</h3>
        </noscript>
        """
        return HttpResponse(js_code, content_type="text/html")

    return _wrapped_view

def get_secux_message(key):
    return getattr(settings, "SECUX_MESSAGES", {}).get(key, DEFAULT_MESSAGES.get(key))

_block_memory = {}

def _render_blocked_page(message):
    html = f"""
    <!DOCTYPE html>
    <html lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{message}</title>
        <style>
            body {{
                background: #fdfdfd;
                color: #222;
                font-family: sans-serif;
                width: 100%;
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0;
            }}
            .box {{
                display: inline-block;
                padding: 30px;
                background: white;
                border: 1px solid #eee;
                text-align: center;
            }}
            .box h2 {{
                color: red;
                font-weight: bold;
                line-height: 2;
            }}
            .box img {{
                width: 100px;
                height: 100px;
            }}
            .box p {{
                font-size: 12px;
                opacity: 0.6;
            }}
        </style>
    </head>
    <body>
        <div class="box">
            <img src="https://raw.githubusercontent.com/xo-aria/django-secux/refs/heads/main/restricted.png" draggable="false">
            <h2>{message}</h2>
            <p>Protected By Secux</p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html, content_type="text/html", status=429)

def ai_ratelimit(alpha=0.3, warmup_days=7, growth_factor=2.0, block_time=300):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            path = request.path
            now_time = now()
            today = now_time.date()

            if path in _block_memory and _block_memory[path] > now_time.timestamp():
                attack_detected.send(
                    sender=view_func,
                    request=request,
                    path=path,
                    reason="previously_blocked"
                )
                return _render_blocked_page(get_secux_message("blocked"))

            obj, _ = PageRequestLog.objects.get_or_create(path=path, date=today)
            obj.count += 1
            obj.save()

            prev_days = PageRequestLog.objects.filter(path=path, date__lt=today).order_by('-date')[:30]
            if prev_days.count() < warmup_days:
                return view_func(request, *args, **kwargs)

            ewma = prev_days[0].count
            for log in prev_days[1:]:
                ewma = alpha * log.count + (1 - alpha) * ewma

            if obj.count > ewma * growth_factor:
                _block_memory[path] = now_time.timestamp() + block_time
                attack_detected.send(
                    sender=view_func,
                    request=request,
                    path=path,
                    count=obj.count,
                    reason="rate_exceeded"
                )
                return _render_blocked_page(get_secux_message("rate_exceeded"))

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
