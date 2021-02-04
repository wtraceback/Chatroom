from markdown import markdown
from bleach import clean, linkify


def to_html(raw):
    allowed_tags = ['a', 'abbr', 'b', 'br', 'blockquote', 'code', 'del', 'div',
                    'em', 'i', 'ul', 'li', 'ol', 'pre', 'strong', 'ul', 'h1',
                    'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'img']
    allowed_attributes = ['class', 'src', 'title', 'alt', 'href']

    html = markdown(raw, output_format='html')
    clean_html = clean(html, tags=allowed_tags, attributes=allowed_attributes)

    return linkify(clean_html)
