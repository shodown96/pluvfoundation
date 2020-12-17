from django.urls import path, include
from .views import *

app_name = "ngo"
urlpatterns = [
    path('', index, name="index"),
    path('about/', about, name="about"),
    path('contact/', contact, name="contact"),
    path('events/', events, name="events"),
    path('event/<slug:slug>/', event_details, name="event"),
    path('blog/', blog, name="blog"),
    path('blog/<slug:slug>/', post_details, name="post"),
    path('projects/', projects, name="projects"),
    path('project/<slug:slug>/', project_details, name="project"),
    path('search/', search, name="search"),
    path('gallery/', gallery, name="gallery"),
    path('become-a-member/', join, name="join"),
    path('subscribe/', subscribe, name="subscribe"),
    path('unsubscribe/<email>/', unsubscribe, name="unsubscribe"),
]
