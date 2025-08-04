import re
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.utils.html import escape
from django_secux.signals import honeypot_trap_triggered

_HTML_TYPES = ('text/html', 'application/xhtml+xml')

SCRIPT_STYLE_RE = re.compile(r'(?P<script><script.*?>.*?</script>)', re.DOTALL | re.IGNORECASE)
COMMENT_RE = re.compile(r'<!--(?!\[if).*?-->', re.DOTALL)
TAG_SPACE_RE = re.compile(r'>\s+<')
WHITESPACE_RE = re.compile(r'\s{2,}')
IMG_RE = re.compile(r'<img(?![^>]*loading=)([^>]*?)>', re.IGNORECASE)

FAKE_URLS = getattr(settings, 'SECUX_FAKE_URLS', [
    '/wp-admin.php',
    '/admin.php',
    '/ajax.php',
    '/.env',
    '/cpanel/',
    '/backup.zip',
])

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

class MinifyAndInjectFakeScripts(MiddlewareMixin):
    def process_request(self, request):
        if request.path in FAKE_URLS:
            honeypot_trap_triggered.send(
                sender=self.__class__,
                request=request,
                ip=request.META.get('REMOTE_ADDR'),
                path=request.path,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
            )

            from django.http import HttpResponse
            return HttpResponse("404 Not Found", status=404)

    def process_response(self, request, response):
        content_type = response.get('Content-Type', '')
        if any(ct in content_type for ct in _HTML_TYPES):
            try:
                content = response.content.decode('utf-8')
                injected = "\n".join(
                    f'<script src="{escape(path)}" defer async></script>'
                    for path in FAKE_URLS
                )
                if '</body>' in content:
                    content = content.replace('</body>', f'{injected}\n</body>')

                minified = minify_html_safe(content)
                protected = f"<!-- Protected By Secux -->\n{minified}"
                response.content = protected.encode('utf-8')
                response['Content-Length'] = str(len(response.content))
            except Exception:
                pass
        return response
