# django-secux - All-in-One Django Security & Optimization

![django-secux](https://raw.githubusercontent.com/xo-aria/django-secux/refs/heads/main/django-secux.png)

[![Downloads](https://pepy.tech/badge/django-secux)](https://pepy.tech/project/django-secux)
[![PyPI version](https://img.shields.io/pypi/v/django-secux.svg)](https://pypi.org/project/django-secux/)
![Django](https://img.shields.io/badge/Django-3.2%20|%204.2%20|%205.0-green?logo=django)
[![License](https://img.shields.io/github/license/xo-aria/django-secux)](https://github.com/xo-aria/django-secux/blob/main/LICENSE)
![Status](https://img.shields.io/badge/status-active-brightgreen)

- [Document](https://xo-aria.github.io/django-secux/doc/) 
- [Telegram](https://t.me/xo_community_dev)
- [Author](https://t.me/ghanon_dar)

### For install
```
pip install django-secux
```

### For update package
```
pip install django-secux -U
```

## Features
`v1.0.0`
- [+] AI ratelimit ( Check website/page traffic, and when abnormal traffic is detected, block the page. )
- [+] Fake CDN ( Smart compressor with built-in caching )

`v2.0.0`
- [+] Minifing all pages

`v3.0.0`
- [+] Manage user sessions ( Manage an account with all sessions for that account )
- [+] Utils ( A simple and safe method for get `IP` and `User Agent` and ... )

`v4.0.0`
- [+] Attack notification ( you can use it for `signals.py` )
- [+] Compress images size ( for `imageField` in `models` )

`v5.0.0` **[SOON]**
- [+] Captcha ( A captcha image system )
- [+] JS Challenge ( a way to detect robots )
- Honeypot ( A trap for url and fake web page )

`v6.0.0` **[SOON]**
- CSP Rules
- SEO ( automatic generate meta seo tags )
- Support `async`

`v7.0.0` **[SOON]**
- Admin dashboard
- Detect suspicious file on upload ( e.g: `image.png.php` )
- Session Signature ( Prevent session theft )

`v8.0.0` **[SOON]**
- Protect uploaded files
- Detect and clean up useless files for `media` and `static`

`v9.0.0` **[SOON]**
- Sensitive path locking ( It has a password system that repels bots and the password is secured in the backend )
- Smart protection ( sensitive pages such as login and contact us are automatically closed when attacked )
- Creating Automatic Preloading Meta Tags ( CAPMT )
