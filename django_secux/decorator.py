from functools import wraps
from django.http import HttpResponse
from django.utils.timezone import now
from datetime import timedelta
from .models import PageRequestLog
from django.conf import settings

DEFAULT_MESSAGES = {
    "blocked": "⛔ This page is temporarily blocked. Please try again later.",
    "rate_exceeded": "⚠️ Rate limit exceeded. This page is blocked temporarily.",
}

def get_secux_message(key):
    return getattr(settings, "SECUX_MESSAGES", {}).get(key, DEFAULT_MESSAGES.get(key))

_block_memory = {}

def ai_ratelimit(alpha=0.3, warmup_days=7, growth_factor=2.0, block_time=300):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            path = request.path
            now_time = now()
            today = now_time.date()

            if path in _block_memory and _block_memory[path] > now_time.timestamp():
                return HttpResponse(get_secux_message("blocked"), status=429)

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
                return HttpResponse(get_secux_message("rate_exceeded"), status=429)

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
