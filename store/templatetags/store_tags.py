from django import template

register = template.Library()


@register.filter
def range_filter(value):
    return range(int(value))


@register.filter
def empty_stars(value):
    return range(5 - int(value))


@register.filter
def multiply(value, arg):
    return float(value) * float(arg)


@register.filter
def currency(value):
    return f"₹{float(value):,.2f}"
