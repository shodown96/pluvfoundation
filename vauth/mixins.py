from .utils import object_viewed_signal, user_signal
from functools import wraps
from django.contrib.auth.models import AnonymousUser

class ObjectViewMixin(object):
    def dispatch(self, request, *args,**kwargs):
        try:
            instance = self.get_object()
        except self.model.DoesNotExist:
            instance = None
        if instance is not None:
            object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return super(ObjectViewMixin, self).dispatch(request, *args, **kwargs)

def visitor(view_func):
    def wrapped_view(request, *args, **kwargs):
        user_signal.send(request.user.__class__, instance=request.user,request=request)
        return view_func(request, *args, **kwargs)
    return wrapped_view