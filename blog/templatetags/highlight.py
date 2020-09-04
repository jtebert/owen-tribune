from bs4 import BeautifulSoup
from django import template
from django.template.defaultfilters import stringfilter
import pygments
from pygments.formatters import HtmlFormatter
from pygments.lexers import guess_lexer, Python3Lexer, get_lexer_by_name

from django.utils.safestring import mark_safe
from django.utils.encoding import force_text

register = template.Library()


@register.filter
@stringfilter
def highlight(html):
    soup = BeautifulSoup(html, 'html5lib')
    codeblocks = soup.findAll('pre')
    for block in codeblocks:
        code = ''.join([str(item) for item in block.contents])
        if block.has_attr('lang'):
            language = block.get('lang')
            print('LANGUAGE:', language)
            try:
                lexer = get_lexer_by_name(language)
            except:
                raise
        else:
            try:
                lexer = guess_lexer(code)
            except:
                lexer = Python3Lexer()
        if block.has_attr('linenos'):
            formatter = HtmlFormatter(linenos='table')
        else:
            formatter = HtmlFormatter()
        code_hl = pygments.highlight(code, lexer, formatter)
        block.replaceWith(BeautifulSoup(code_hl, 'html.parser'))
    return str(soup)
