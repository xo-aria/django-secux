from functools import wraps
from django.http import HttpResponse
from django.utils.timezone import now
from .models import PageRequestLog
from django.conf import settings

DEFAULT_MESSAGES = {
    "blocked": "⛔ این صفحه موقتاً مسدود شده است. لطفاً بعداً تلاش کنید.",
    "rate_exceeded": "⚠️ تعداد درخواست‌ها بیش از حد مجاز است. صفحه به‌طور موقت مسدود شد.",
}

def get_secux_message(key):
    return getattr(settings, "SECUX_MESSAGES", {}).get(key, DEFAULT_MESSAGES.get(key))

_block_memory = {}

def _render_blocked_page(message):
    html = f"""
    <!DOCTYPE html>
    <html lang="fa">
    <head>
        <meta charset="UTF-8">
        <title>{message}</title>
        <style>
            body {{
                background: #fdfdfd;
                color: #222;
                font-family: sans-serif;
                text-align: center;
                padding: 50px;
                direction: rtl;
            }}
            .box {{
                border: 1px solid #ddd;
                display: inline-block;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                background: white;
            }}
            .emoji {{
                font-size: 40px;
                margin-bottom: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="box">
            <div class="emoji">🚫</div>
            <h2>{message}</h2>
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
                return _render_blocked_page(get_secux_message("rate_exceeded"))

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
