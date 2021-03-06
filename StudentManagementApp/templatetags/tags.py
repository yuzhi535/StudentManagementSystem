from django import template
from django.template.defaultfilters import stringfilter

from StudentManagementApp.models import Study

register = template.Library()


def update_variable(value):
    data = value
    return data


class SetVarNode(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""


def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return SetVarNode(parts[1], parts[3])


@register.filter(name='study_filter')
def study_filter(t_group, course):
    group = t_group.filter(course=course)
    return group


@register.filter(name='study_filter_1')
def study_filter_1(t_group, staff):
    group = t_group.filter(staff=staff)
    return group


register.tag('set', set_var)

register.filter('update_variable', update_variable)
