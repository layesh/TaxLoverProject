from django import template

from taxlover.utils import add_comma

register = template.Library()


@register.filter
def format_decimal(value):
    return add_comma(value)
