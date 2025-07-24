import re
from django.utils.deprecation import MiddlewareMixin

_HTML_TYPES = ('text/html', 'application/xhtml+xml')

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
        tag = match.group()
        parts.append(tag)
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
        if any(ct in content_type for ct in _HTML_TYPES):
            try:
                content = response.content.decode('utf-8')
                minified = minify_html_safe(content)
                protected_content = f"<!-- Protected By Secux -->\n{minified}"
                response.content = protected_content.encode('utf-8')
                response['Content-Length'] = str(len(response.content))
            except:
                pass
        return response
