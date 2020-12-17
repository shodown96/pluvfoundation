from django.dispatch import Signal

object_viewed_signal = Signal(providing_args=['instance', 'request'])

user_signal = Signal(providing_args=['request'])

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip