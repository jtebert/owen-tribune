from django import template

register = template.Library()

@register.filter(name='to_class_name')
def to_class_name(value):
    out = value.__class__.__name__
    return out