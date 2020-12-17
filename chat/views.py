from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from .models import Chat, Contact

User = get_user_model()

def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    chat = get_object_or_404(Chat, name=room_name)
    message_list = chat.messages.order_by('-timestamp').all()
    paginator = Paginator(message_list, 10)
    page = request.GET.get('page')
    messages = paginator.get_page(page)

    return render(request, 'chat/room.html', {
        'room_name': chat.name,
        'chat_id':chat.id,
        'cmessages': messages
    })
    
def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('timestamp').all()[:10]


def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Contact, user=user)


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)
