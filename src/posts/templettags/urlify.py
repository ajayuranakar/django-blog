from urllib import quote_plus
from django import template

rigister=template.Library()

@register.filter
def urlify(value):
	return quote_plus(value)