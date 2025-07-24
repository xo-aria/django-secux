import re
from django.utils.deprecation import MiddlewareMixin

_HTML_TYPES = ('text/html', 'application/xhtml+xml')
SCRIPT_STYLE_RE = re.compile(r'(<script.*?>.*?</script>|<style.*?>.*?</style>)', re.DOTALL | re.IGNORECASE)
TAG_SPACE_RE = re.compile(r'>\s+<')
COMMENT_RE = re.compile(r'<!--(?!\[if).*?-->', re.DOTALL)

def minify_html_safe(content):
    parts = SCRIPT_STYLE_RE.split(content)
    for i in range(len(parts)):
        if not parts[i].lower().startswith('<script') and not parts[i].lower().startswith('<style'):
            parts[i] = COMMENT_RE.sub('', parts[i])
            parts[i] = TAG_SPACE_RE.sub('><', parts[i])
            parts[i] = parts[i].strip()
    return ''.join(parts)

class Minify(MiddlewareMixin):
    def process_response(self, request, response):
        content_type = response.get('Content-Type', '')
        if any(ct in content_type for ct in _HTML_TYPES):
            try:
                content = response.content.decode('utf-8')
                minified = minify_html_safe(content)
                response.content = minified.encode('utf-8')
                response['Content-Length'] = str(len(response.content))
            except:
                pass
        return response
