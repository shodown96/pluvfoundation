from django import template
from chat.views import get_user_contact
register = template.Library()

@register.filter
def get_contact_chats(user):
    contact = get_user_contact(user)
    return contact.chats.all()