from django import template

register = template.Library()

@register.filter
def truncate_text(text, num):
    text = text.split('\n')
    out = ""
    for p in text:
        out += p+"\n"
        if len(out) > num:
            return out
    return out
