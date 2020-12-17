from django import template
from django.conf import settings

ADMIN_STYLE = settings.ADMIN_STYLE
ADDRESS = settings.ADDRESS
PHONE_NUMBER = settings.PHONE_NUMBER
STATE_COUNTRY = settings.STATE_COUNTRY
WEBSITE_EMAIL = settings.WEBSITE_EMAIL
register = template.Library()

@register.simple_tag
def use_custom():
    return ADMIN_STYLE

@register.simple_tag
def address():
    return ADDRESS

@register.simple_tag
def state_country():
    return STATE_COUNTRY

@register.simple_tag
def phone_number():
    return PHONE_NUMBER

@register.simple_tag
def website_email():
    return WEBSITE_EMAIL