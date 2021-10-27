from django import template

register = template.Library()


@register.filter(name='slice_last')
def slice_last(stri):
	return str(stri)[-3:]