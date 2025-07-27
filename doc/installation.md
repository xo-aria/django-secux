# Installation

Install using pip:

```
pip install django-secux
```

Add to your Django project:

```python
# settings.py
INSTALLED_APPS = [
    ...
    'django_secux',
]

MIDDLEWARE = [
    ...
    'django_secux.middleware.Minify',
]
```

Apply migrations:

```
python manage.py makemigrations django_secux
python manage.py migrate
```


---

[⬅️ Back to Index](index.md) | [⬆️ Menu](index.md)
