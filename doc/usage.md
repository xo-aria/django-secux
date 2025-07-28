# Usage Guide
- [Rate Limiting](#rate-limiting)
- [Fake CDN System](#fake-cdn-system)
- [Static File Optimization](#static-file-optimization)
- [User Session Management](#user-session-management)
- [Utility Tools](#utility-tools)

---

## Rate Limiting
Protect your views from excessive requests with AI-powered rate limiting.

```python
from django_secux.decorator import ai_ratelimit

@ai_ratelimit()
def protected_view(request):
    return HttpResponse("Protected content")
```

---

## Fake CDN System
Simulate a CDN for static files with optimization features.

### Setup
1. Add to `urls.py`:
```python
from django_secux.views import cdn_serve

urlpatterns = [
    path('cdn/<path:file_path>', cdn_serve, name='cdn'),
]
```

2. Collect static files:
```bash
python manage.py collectstatic
```

### Usage in Templates
```html
<!-- Basic usage -->
<img src="/cdn[STATIC]">

<!-- With resizing -->
<img src="/cdn[STATIC]?size=250">
```

---

## Static File Optimization
Automatic optimizations include:
- HTML/CSS/JS minification
- Font optimization
- Image compression (via Fake CDN)

---

## User Session Management
```python
import django_secux.user as dsu
```

### Session Operations
| Function | Description | Returns |
|----------|-------------|---------|
| `create_session(user, session_key, ip=None, user_agent=None)` | Create new session | - |
| `check_user_session(user, session_key)` | Check session exists | Boolean |
| `get_user_sessions(user)` | Get user's sessions | QuerySet |
| `get_all_sessions()` | Get all sessions | List |
| `terminate_session(user, session_key)` | End session | Deleted count |
| `is_session_active(session_key)` | Check session active | Boolean |

---

## Utility Tools
```python
import django_secux.tools as dst
```

### Client Information
| Function | Returns |
|----------|---------|
| `get_user_ip(request)` | Client IP |
| `get_user_agent(request)` | User agent |
| `get_referer_url(request, default)` | Referer URL |
| `is_request_secure(request)` | HTTPS status |
| `get_user_meta(request)` | User metadata |
| `get_request_headers(request, prefix)` | Request headers |
| `get_client_timezone(request, default)` | Timezone |
| `is_mobile_device(request)` | Mobile check |
| `get_client_fingerprint(request)` | Device fingerprint |

---

[Previous](installation.md) | [Menu](index.md) | [Next](configuration.md)
