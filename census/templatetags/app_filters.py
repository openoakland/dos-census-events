from django import template
from datetime import date, timedelta

register = template.Library()
@register.filter(is_safe=True, name='label_with_classes')
def label_with_classes(value, arg):
    return value.label_tag(attrs={'class': arg})
