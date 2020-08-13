from django import template
from accounts.enums import RoleCodes
register = template.Library()

@register.simple_tag
def is_teacher(user):
    return user.role.code==RoleCodes.TEACHER.value