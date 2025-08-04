import re
import random
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.utils.html import escape
from django.http import HttpResponse
from django_secux.signals import honeypot_trap_triggered

HTML_TYPES = ('text/html', 'application/xhtml+xml')

FAKE_URLS = getattr(settings, 'SECUX_FAKE_URLS', [
    '/wp-admin.php',
    '/admin.php',
    '/ajax.php',
    '/.env',
    '/cpanel/',
    '/backup.zip',
    '/config.json',
    '/cdn/jquery.js',
    '/old-login',
    '/dashboard/api',
    '/auth/session',
    '/includes/init.php'
])

def generate_fake_tags():
    fake_tags = []
    for path in random.sample(FAKE_URLS, min(6, len(FAKE_URLS))):
        tag_type = random.choice(['script', 'img', 'link', 'fetch', 'xhr', 'iframe'])
        if tag_type == 'script':
            fake_tags.append(f'<script src="{escape(path)}" defer async></script>')
        elif tag_type == 'img':
            fake_tags.append(f'<img src="{escape(path)}" style="display:none;" width="1" height="1" loading="lazy">')
        elif tag_type == 'link':
            fake_tags.append(f'<link rel="preload" href="{escape(path)}" as="script">')
        elif tag_type == 'iframe':
            fake_tags.append(f'<iframe src="{escape(path)}" style="display:none;" loading="lazy"></iframe>')
        elif tag_type == 'fetch':
            fake_tags.append(f'<script>fetch("{escape(path)}").then(()=>{{}}).catch(()=>{{}})</script>')
        elif tag_type == 'xhr':
            fake_tags.append(f'<script>let x=new XMLHttpRequest();x.open("GET","{escape(path)}",true);x.send();</script>')
    return '\n'.join(fake_tags)

def generate_fake_page(target_url):
    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>Redirecting...</title></head>
    <body>
    <h2>Session expired</h2>
    <p>Your session has expired or is invalid. Please <a href="{escape(target_url)}">click here</a> to re-authenticate.</p>
    </body>
    </html>
    """

class Honeypot(MiddlewareMixin):
    def process_request(self, request):
        if request.path in FAKE_URLS:
            honeypot_trap_triggered.send(
                sender=self.__class__,
                request=request,
                ip=request.META.get('REMOTE_ADDR'),
                path=request.path,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
            )
            if request.method == 'POST':
                bait_url = random.choice([url for url in FAKE_URLS if url != request.path])
                html = generate_fake_page(bait_url)
                return HttpResponse(html, status=200, content_type='text/html')
            return HttpResponse("404 Not Found", status=404)

    def process_response(self, request, response):
        content_type = response.get('Content-Type', '')
        if request.method == "GET" and any(ct in content_type for ct in HTML_TYPES) and response.status_code == 200:
            try:
                content = response.content.decode('utf-8')
                if '</body>' in content:
                    injected = generate_fake_tags()
                    content = content.replace('</body>', f'{injected}\n</body>')
                    content = f"<!-- Protected by Secux -->\n{content}"
                    response.content = content.encode('utf-8')
                    response['Content-Length'] = str(len(response.content))
            except Exception:
                pass
        return response

SCRIPT_STYLE_RE = re.compile(r'(?P<script><script.*?>.*?</script>)', re.DOTALL | re.IGNORECASE)
COMMENT_RE = re.compile(r'<!--(?!\[if).*?-->', re.DOTALL)
TAG_SPACE_RE = re.compile(r'>\s+<')
WHITESPACE_RE = re.compile(r'\s{2,}')
IMG_RE = re.compile(r'<img(?![^>]*loading=)([^>]*?)>', re.IGNORECASE)

def minify_html_safe(html):
    parts = []
    index = 0
    for match in SCRIPT_STYLE_RE.finditer(html):
        start, end = match.span()
        before = html[index:start]
        before = COMMENT_RE.sub('', before)
        before = TAG_SPACE_RE.sub('><', before)
        before = WHITESPACE_RE.sub(' ', before)
        before = IMG_RE.sub(r'<img loading="lazy"\1>', before)
        parts.append(before)
        parts.append(match.group())
        index = end
    remainder = html[index:]
    remainder = COMMENT_RE.sub('', remainder)
    remainder = TAG_SPACE_RE.sub('><', remainder)
    remainder = WHITESPACE_RE.sub(' ', remainder)
    remainder = IMG_RE.sub(r'<img loading="lazy"\1>', remainder)
    parts.append(remainder)
    return ''.join(parts).strip()

class Minify(MiddlewareMixin):
    def process_response(self, request, response):
        content_type = response.get('Content-Type', '')
        if request.method == "GET" and any(ct in content_type for ct in HTML_TYPES) and response.status_code == 200:
            try:
                content = response.content.decode('utf-8')
                minified = minify_html_safe(content)
                response.content = minified.encode('utf-8')
                response['Content-Length'] = str(len(response.content))
            except Exception:
                pass
        return response
