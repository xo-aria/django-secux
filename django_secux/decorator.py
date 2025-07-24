from functools import wraps
from django.http import HttpResponse
from django.utils.timezone import now
from datetime import timedelta
from .models import PageRequestLog
from django.db.models import Avg
from django.conf import settings

DEFAULT_MESSAGES = {
    "blocked": "⛔ This page is temporarily blocked. Please try again later.",
    "rate_exceeded": "⚠️ Rate limit exceeded. This page is blocked temporarily.",
}

def get_secux_message(key):
    return getattr(settings, "SECUX_MESSAGES", {}).get(key, DEFAULT_MESSAGES.get(key))

_block_memory = {}

def ai_ratelimit(day_limit=7, extra_threshold=10, block_time=300):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            path = request.path
            today = now().date()

            # Check block memory
            if path in _block_memory and _block_memory[path] > now().timestamp():
                return HttpResponse(get_secux_message("blocked"), status=429)

            # Log today's request
            obj, _ = PageRequestLog.objects.get_or_create(path=path, date=today)
            obj.count += 1
            obj.save()

            # Calculate average from previous days
            start_day = today - timedelta(days=day_limit)
            avg = (
                PageRequestLog.objects
                .filter(path=path, date__gte=start_day, date__lt=today)
                .aggregate(average=Avg('count'))['average'] or 0
            )

            if obj.count > avg + extra_threshold:
                _block_memory[path] = now().timestamp() + block_time
                return HttpResponse(get_secux_message("rate_exceeded"), status=429)

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
