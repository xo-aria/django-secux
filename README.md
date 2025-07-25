# django-secux - All-in-One Django Security & Optimization

![django-secux](https://raw.githubusercontent.com/xo-aria/django-secux/refs/heads/main/django-secux.png)

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
   - [Rate Limiting](#rate-limiting)
   - [Fake CDN System](#fake-cdn-system)
   - [Static File Optimization](#static-file-optimization)
5. [Configuration](#configuration)
6. [Contributing](#contributing)

## Overview

django-secux is a comprehensive Django package that combines security protection with performance optimization features, including rate limiting, static file minification, and image compression.

## Features

- **Intelligent Rate Limiting**: Protects heavy-load pages based on real usage patterns
- **Static File Optimization**: Minification for HTML, CSS, JS
- **Fake CDN System**: Image compression with on-demand resizing
- **Easy Integration**: Simple decorator-based implementation

## Installation

```bash
pip install django-secux
```

Add to your Django project:
```python
# settings.py
INSTALLED_APPS = [
    ...
    'django_secux',
]

# For minification support
MIDDLEWARE = [
    ...
    'django_secux.middleware.Minify',
]
```

Apply migrations:
```bash
python manage.py makemigrations django_secux
python manage.py migrate
```

## Usage

### Rate Limiting

```python
from django_secux.decorator import ai_ratelimit

@ai_ratelimit()
def protected_view(request):
    return HttpResponse("Protected content")
```

### Fake CDN System

1. Add to your main `urls.py`:
```python
from django_secux.views import cdn_serve

urlpatterns = [
    ...
    path('cdn/<path:file_path>', cdn_serve, name='cdn'),
]
```

2. Run collectstatic:
```bash
python manage.py collectstatic
```

3. Use in templates:
```html
<!-- Basic usage -->
<img src="/cdn[ STATIC ]">

<!-- With resizing -->
<img src="/cdn[ STATIC ]?size=250">
```

### Static File Optimization

The package automatically handles:
- Minification of HTML/CSS/JS
- Font optimization
- Image compression (when using Fake CDN)

## Configuration

```python
# settings.py

# Security messages
SECUX_MESSAGES = {
    "blocked": "This page is temporarily blocked. Please try again later.",
    "rate_exceeded": "Rate limit exceeded. This page is blocked temporarily.",
}

# Static/media files locations
SECUX_STATIC = [
    STATIC_ROOT,
    *STATICFILES_DIRS,
    os.path.join(BASE_DIR, "media/uploads"),
    os.path.join(BASE_DIR, "protected/images"),
]
```

## Contributing

We welcome contributions! Please report issues or submit pull requests on [GitHub](https://github.com/xo-aria/django-secux).

Key areas for contribution:
- Additional optimization features
- Improved rate limiting algorithms
- Enhanced Fake CDN functionality

---

This documentation now has clear sections, better organization, and emphasizes the Fake CDN system requirements (collectstatic) while maintaining all the original information in a more professional structure.
