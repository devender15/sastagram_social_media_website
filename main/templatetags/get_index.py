from django import template
import ast

register = template.Library()


@register.filter(name='get_idx')
def get_idx(dictionar, comment):

	val = list(dictionar.values()).index(comment)
	return val