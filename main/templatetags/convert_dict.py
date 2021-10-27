from django import template
import ast

register = template.Library()


@register.filter(name='to_dict')
def to_dict(stri):

	dicto = ast.literal_eval(stri)

	return dicto