# django-secux

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
