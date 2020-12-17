from django.urls import path, include
from .views import *

app_name="payment"
urlpatterns = [
    path("donate/", donate, name="donate"),
    path("callback/verify/", callback, name="verify"),
    path('cancel/', cancel, name="cancel")
]
