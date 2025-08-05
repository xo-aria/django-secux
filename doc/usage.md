# Usage

* [Rate Limiting](#rate-limiting-)
* [Fake CDN System](#fake-cdn-system-)
* [Smart minify](#smart-minify)
* [User Session Management](#user-session-management-)
* [Utility Tools](#utility-tools-)
* [Optimize ImageField](#optimize-imagefield-)
* [Captcha](#captcha-)
* [JS Challenge](#js-challenge-)
* [Honeypot](#honeypot-)

---

## Rate Limiting [(+)](https://github.com/xo-aria/django-secux/blob/main/django_secux/decorator.py)

```python
from django_secux.decorator import ai_ratelimit

@ai_ratelimit()
def protected_view(request):
    return HttpResponse("Protected content")
```

and a receiver for when blocked:

```python
from django.dispatch import receiver
from django_secux.signals import attack_detected

@receiver(attack_detected)
def log_attack(sender, **kwargs):
    request = kwargs.get("request")
    path = kwargs.get("path")
    reason = kwargs.get("reason")
    ip = request.META.get("REMOTE_ADDR") if request else "unknown"
    user_agent = request.META.get("HTTP_USER_AGENT", "unknown") if request else "unknown"
    count = kwargs.get("count")

    log_message = "[SECUX] Attack detected:\n"
    log_message += f"  View: {sender.__name__ if sender else 'unknown'}\n"
    log_message += f"  Path: {path}\n"
    log_message += f"  IP: {ip}\n"
    log_message += f"  Reason: {reason}\n"
    log_message += f"  User-Agent: {user_agent}\n"

    print(log_message)
```
> [!Tip]
> You can use it for `EMAIL` and `Webhook` and `Log`.
---

## Fake CDN System [(+)](https://github.com/xo-aria/django-secux/blob/main/django_secux/views.py)

1. Add to your `urls.py`:

```python
from django_secux.views import cdn_serve

urlpatterns = [
    ...
    path('cdn/<path:file_path>', cdn_serve, name='cdn'),
]
```

2. Run collectstatic:

```
python manage.py collectstatic
```

3. Use in templates:

```html
<!-- Basic usage -->
<img src="/cdn[ STATIC ]">

<!-- With resizing -->
<img src="/cdn[ STATIC ]?size=250">
```

---

## Smart Minify

### Minification of HTML/CSS/JS [(+)](https://github.com/xo-aria/django-secux/blob/main/django_secux/middleware.py#L114)
```python
MIDDLEWARE = [
    ...
    'django_secux.middleware.Minify'
]
```

# Use for css/js
{% raw %}
```html
<link rel="stylesheet" href="/cdn{% static 'style.css' %}" />

...

<script src="/cdn{% static 'script.js' %}"></script>
```
{% endraw %}

---

## User Session Management [(+)](https://github.com/xo-aria/django-secux/blob/main/django_secux/user.py)

```python
import django_secux.user as dsu
```

### Create New Session

```python
dsu.create_session(user, session_key, ip=None, user_agent=None)
```

* Registers a new session for the user.
* Optional arguments: `ip`, `user_agent`.

### Check If Session Exists

```python
dsu.check_user_session(user, session_key)
```

* Checks if a session exists for the user and session key.
* Returns `True` if found, otherwise `False`.

### Get User Sessions

```python
dsu.get_user_sessions(user)
```

* Retrieves all sessions belonging to the given user.

### Get All Sessions

```python
dsu.get_all_sessions()
```

* Returns a list of all stored sessions.

### Terminate a Session

```python
dsu.terminate_session(user, session_key)
```

* Deletes the specified session from both custom model and Django's built-in Session table.
* Returns number of deleted sessions.

### Check If Session is Active

```python
dsu.is_session_active(session_key)
```

* Checks if the session is still valid (not expired).
* Returns `True` or `False`.

---

## Utility Tools [(+)](https://github.com/xo-aria/django-secux/blob/main/django_secux/tools.py)

```python
import django_secux.tools as dst
```

### Get user ip

```python
dst.get_user_ip(request)
```

### Get user agent

```python
dst.get_user_agent(request)
```

### Get referer url

```python
dst.get_referer_url(request, default)
```

### Is request secure

```python
dst.is_request_secure(request)
```

### Get user meta

```python
dst.get_user_meta(request)
```

### Get request headers

```python
dst.get_request_headers(request, prefix)
```

### Get client timezone

```python
dst.get_client_timezone(request, default)
```

### Is mobile device

```python
dst.is_mobile_device(request)
```

### Get client fingerprint

```python
dst.get_client_fingerprint(request)
```

---

## Optimize ImageField [(+)](https://github.com/xo-aria/django-secux/blob/175aa18b8860dc442f0fbcfc50abb3246a1abda5/django_secux/models.py#L37)

### Import
```python
from django_secux.models import OptimizeImageField
```

### Usage in models
```python
image = OptimizeImageField(upload_to='image/', name=f'image.jpg', size=(300, 300))
```

### Example
```python
from django.db import models
from django_secux.models import OptimizeImageField

class Test(models.Model):
    avatar = OptimizeImageField(upload_to='test/', name=f'test.jpg', size=(300, 300))
```

---

## Captcha [(+)](https://github.com/xo-aria/django-secux/blob/main/django_secux/captcha.py)

### Usage in views
```python
from django_secux import captcha

def your_views(request):
    if captcha.is_captcha_valid(request):
        return HttpResponse(f'Success!')
    else:
        return HttpResponse(f'Failed!')
```

### Usage in templates
{% raw %}
```html
{% load secux_captcha %}
...
<img src="{% captcha_src %}">
<input name="secux_captcha_input">
```
{% endraw %}

---

## JS Challenge [(+)](https://github.com/xo-aria/django-secux/blob/7b88e7d47451c54e93e35ccfc9f2cabcdcb24807/django_secux/decorator.py#L13)

### Usage in views
```python
from django_secux.decorator import js_challenge

@js_challenge
def your_views(request):
    return HttpResponse('Hello world!')
```

---

## Honeypot [(+)](https://github.com/xo-aria/django-secux/blob/main/django_secux/middleware.py)

### Usage
```python
MIDDLEWARE = [
    ...
    'django_secux.middleware.Honeypot'
]
```

---

[Previous](installation.md) | [Menu](index.md) | [Next](configuration.md)
