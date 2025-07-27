# Usage

## Rate Limiting

```python
from django_secux.decorator import ai_ratelimit

@ai_ratelimit()
def protected_view(request):
    return HttpResponse("Protected content")
```

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

## Static File Optimization

- Minification of HTML/CSS/JS
- Font optimization
- Image compression (when using Fake CDN)
