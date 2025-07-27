# Configuration

Example configuration in `settings.py`:

```python
SECUX_MESSAGES = {
    "blocked": "This page is temporarily blocked. Please try again later.",
    "rate_exceeded": "Rate limit exceeded. This page is blocked temporarily.",
}

SECUX_STATIC = [
    STATIC_ROOT,
    *STATICFILES_DIRS,
    os.path.join(BASE_DIR, "media/uploads"),
    os.path.join(BASE_DIR, "protected/images"),
]
```


---

[⬅️ Back to Index](index.md) | [⬆️ Menu](index.md)
