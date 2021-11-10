from django import template

from taxlover.utils import add_comma, add_comma_whole

register = template.Library()


@register.filter
def format_decimal(value):
    if value == 0:
        return '0.00'
    else:
        return add_comma(value)


@register.filter
def format_decimal_to_whole(value):
    if value == 0:
        return 0
    else:
        return add_comma_whole(value)


@register.filter
def format_investment_amount(value):
    if value == 0:
        return ''
    else:
        return add_comma(value)


@register.filter
def format_cash_asset_outside_business(value):
    if value == 0:
        return '-'
    else:
        return add_comma(value)

