from django.urls import path, re_path
from .views import *

app_name = "vauth"
urlpatterns = [
    path('login/', mylogin, name="login"),
    path('dashboard/', dashboard, name="dashboard"),
    path('analytics/', analytics, name="analytics"),
    path('profile/', profile, name="profile"),
    path('dp/', dp, name="dp"),
    path('posts/', posts, name="posts"),
    path('edit-post/<slug:slug>/', edit_post, name="edit_post"),
    path('tasks/', tasks, name="tasks"),
    path('complete-task/<int:task_id>/', complete_task, name="complete_task"),
    path('newsletter/', newsletter, name="newsletter"),
    path('ajax-donations/', ajax_donations, name="ajax_donations"),
    path("ajax-visitors/", ajax_visitors, name="ajax_visitors"),
    #####################
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
]
