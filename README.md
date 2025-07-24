![django-secux](https://raw.githubusercontent.com/xo-aria/django-secux/refs/heads/main/django-secux.png)
# django-secux

[![PyPI version](https://img.shields.io/pypi/v/django-secux?label=PyPI&color=blue&logo=python)](https://pypi.org/project/django-secux/)
[![Python Versions](https://img.shields.io/pypi/pyversions/django-secux?logo=python&color=brightgreen)](https://pypi.org/project/django-secux/)
[![Django Versions](https://img.shields.io/badge/Django-3.2%20|%204.0%20|%204.2%20|%205.0-blue?logo=django)](#)
[![License](https://img.shields.io/github/license/xo-aria/django-secux?color=green)](LICENSE)
[![Stars](https://img.shields.io/github/stars/xo-aria/django-secux?style=social)](https://github.com/xo-aria/django-secux/stargazers)
[![Issues](https://img.shields.io/github/issues/xo-aria/django-secux?logo=github)](https://github.com/xo-aria/django-secux/issues)
[![Last Commit](https://img.shields.io/github/last-commit/xo-aria/django-secux?logo=git)](https://github.com/xo-aria/django-secux/commits)

**django-secux** is a simple yet powerful Django security package that protects heavy-load pages by rate-limiting access based on real usage patterns stored in the database.

---

## 🚀 Features

* 🔐 Blocks pages when abnormal request patterns are detected
* 📊 Logs each view's daily request count in your database
* 🕝 Automatically blocks overused views for a customizable time window
* ✅ Super easy to use with just a decorator!

---

## 📦 Installation

```bash
pip install django-secux
```

Then add it to your Django project:

```python
# settings.py
INSTALLED_APPS = [
    ...
    'django_secux',
]
```

Apply migrations:

```bash
python manage.py makemigrations django_secux
python manage.py migrate
```

---

## ⚙️ Usage

Just decorate your heavy or sensitive views with `@ai_ratelimit()`:

```python
from django_secux.decorator import ai_ratelimit

@ai_ratelimit()
def my_view(request):
    return HttpResponse("Hello, world!")
```

This view will now be monitored. If accessed too frequently within a day, it will be blocked for 5 minutes.

---

## ✏️ Customization

You can customize the block and warning messages shown to users in your `settings.py`:

```python
SECUX_MESSAGES = {
    "blocked": "⛔ This page is temporarily blocked. Please try again later.",
    "rate_exceeded": "⚠️ Rate limit exceeded. This page is blocked temporarily.",
}
```

Feel free to translate or rephrase these messages as needed.

---

## 🧠 Ideas or Issues?

Feel free to contribute, fork or submit issues on GitHub.

Let's keep Django apps safe and clean!
