from functools import wraps
from django.http import HttpResponse
from django.utils.timezone import now
from datetime import timedelta
from .models import PageRequestLog
from django.db.models import Avg, StdDev
from django.conf import settings

DEFAULT_MESSAGES = {
    "blocked": "⛔ This page is temporarily blocked. Please try again later.",
    "rate_exceeded": "⚠️ Rate limit exceeded. This page is blocked temporarily.",
}

def get_secux_message(key):
    return getattr(settings, "SECUX_MESSAGES", {}).get(key, DEFAULT_MESSAGES.get(key))

_block_memory = {}

def ai_ratelimit(day_limit=7, std_multiplier=2, block_time=300):
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

            start_day = today - timedelta(days=day_limit)
            qs = PageRequestLog.objects.filter(path=path, date__gte=start_day, date__lt=today)
            if qs.count() < day_limit:
                return view_func(request, *args, **kwargs)

            agg = qs.aggregate(avg=Avg('count'), std=StdDev('count'))
            avg = agg['avg'] or 0
            std = agg['std'] or 0
            threshold = avg + std_multiplier * std

            if obj.count > threshold:
                _block_memory[path] = now_time.timestamp() + block_time
                return HttpResponse(get_secux_message("rate_exceeded"), status=429)

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
