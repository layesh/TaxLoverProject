from django import template

from taxlover.utils import add_comma, add_comma_whole

register = template.Library()


@register.filter
def format_decimal(value):
    return add_comma(value)


@register.filter
def format_decimal_to_whole(value):
    return add_comma_whole(value)
