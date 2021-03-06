from django import template

register = template.Library()


@register.filter('startswith')
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False


@register.filter('endswith')
def endswith(text, starts):
    if isinstance(text, str):
        return text.endswith(starts)
    return False


@register.filter()
def to_int(value):
    return int(value)
