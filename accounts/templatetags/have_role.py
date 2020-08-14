from django import template
from accounts.enums import RoleCodes
register = template.Library()

@register.simple_tag
def is_teacher(user):
    return user.is_teacher()