from django import template
import ast

register = template.Library()


@register.filter(name='to_list')
def to_list(stri):

	lst = ast.literal_eval(stri)

	return lst