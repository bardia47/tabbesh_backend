from django import template
from zarinpal.enums import Events
register = template.Library()

@register.simple_tag
def event_discount(type):
    return Events[type+'_DISCOUNT'].value


def event_amount(type):
    return Events[type+"_AMOUNT"].value