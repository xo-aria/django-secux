from django.conf import settings
import html

# ======================== Request Utilities ========================
def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip or 'unknown'

def get_user_agent(request):
    agent = request.META.get('HTTP_USER_AGENT', 'unknown')
    return html.escape(agent[:500])

def get_referer_url(request, default='direct'):
    referer = request.META.get('HTTP_REFERER')
    return html.escape(referer) if referer else default

# ======================== Security Utilities ========================
def is_request_secure(request):
    if getattr(settings, 'SECURE_PROXY_SSL_HEADER', None):
        return request.is_secure()
    return request.scheme == 'https'

# ======================== User Utilities ========================
def get_user_meta(request):
    return {
        'ip': get_user_ip(request),
        'agent': get_user_agent(request),
        'language': request.META.get('HTTP_ACCEPT_LANGUAGE', 'unknown'),
        'timezone': request.META.get('HTTP_CLIENT_TIMEZONE', 'UTC'),
        'secure': is_request_secure(request),
    }

# ======================== Debugging Utilities ========================
def get_request_headers(request, prefix='HTTP_'):
    return {
        key[len(prefix):]: sanitize_input(value)
        for key, value in request.META.items()
        if key.startswith(prefix)
    }

# ======================== Time Utilities ========================
def get_client_timezone(request, default='UTC'):
    tz = request.session.get('timezone')
    return tz if tz else request.META.get('HTTP_CLIENT_TIMEZONE', default)

# ======================== Device Detection ========================
def is_mobile_device(request):
    agent = get_user_agent(request).lower()
    mobile_keywords = ['mobile', 'android', 'iphone', 'ipad', 'windows phone']
    return any(kw in agent for kw in mobile_keywords)

# ======================== Rate Limiting Helpers ========================
def get_client_fingerprint(request):
    user_part = str(request.user.pk) if request.user.is_authenticated else 'anon'
    return f"{get_user_ip(request)}:{user_part}:{hash(get_user_agent(request))}"
