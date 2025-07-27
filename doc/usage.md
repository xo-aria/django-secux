# Usage

* [Rate Limiting](#rate-limiting)
* [Fake CDN System](#fake-cdn-system)
* [Static File Optimization](#static-file-optimization)
* [User Session Management](#user-session-management)

---

## Rate Limiting

```python
from django_secux.decorator import ai_ratelimit

@ai_ratelimit()
def protected_view(request):
    return HttpResponse("Protected content")
```

---

## Fake CDN System

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

## Static File Optimization

* Minification of HTML/CSS/JS
* Font optimization
* Image compression (when using Fake CDN)

---

## User Session Management

### Create New Session

```python
create_session(user, session_key, ip=None, user_agent=None)
```

* Registers a new session for the user.
* Optional arguments: `ip`, `user_agent`.

---

### Check If Session Exists

```python
check_user_session(user, session_key)
```

* Checks if a session exists for the user and session key.
* Returns `True` if found, otherwise `False`.

---

### Get User Sessions

```python
get_user_sessions(user)
```

* Retrieves all sessions belonging to the given user.

---

### Get All Sessions

```python
get_all_sessions()
```

* Returns a list of all stored sessions.

---

### Terminate a Session

```python
terminate_session(user, session_key)
```

* Deletes the specified session from both custom model and Django's built-in Session table.
* Returns number of deleted sessions.

---

### Check If Session is Active

```python
is_session_active(session_key)
```

* Checks if the session is still valid (not expired).
* Returns `True` or `False`.

---

[Back to Index](index.md) | [Menu](index.md)
