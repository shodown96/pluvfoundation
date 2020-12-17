from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from taggit.models import Tag
from chat.models import Contact
from ckeditor.fields import RichTextField
from .utils import user_signal, get_client_ip


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    sex = models.CharField(max_length=10)
    about = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    dp = models.ImageField(upload_to="display_pics/", blank=True, null=True)
    location = models.CharField(max_length=100)
    position = models.CharField(max_length=100, default="Member", blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True, db_index=True)
    subscribed = models.BooleanField(default=False)
    class Meta:
        ordering = ['-date_joined']
    def delete(self, *args, **kwargs):
        self.dp.delete()
        super().delete(*args, **kwargs)
    # def save(self, *args, **kwargs):
    #     super().full_clean(*args, **kwargs)
    #     super().save(*args, **kwargs)


class Applicant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    statement = models.TextField()
    middle_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    address = models.CharField(max_length=100)
    sex = models.CharField(max_length=10)
    date_applied = models.DateTimeField(auto_now_add=True, db_index=True)
    class Meta:
        ordering = ['-date_applied']

class Task(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    completed = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    class Meta:
        ordering = ['-timestamp']

def profile_reciever(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Contact.objects.create(user=instance)


post_save.connect(profile_reciever, sender=User)

class Visitor(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    ip_address = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)

# def user_receiver(sender, instance, request, *args, **kwargs):
#     user = instance
#     ip_address = get_client_ip(request)
#     ip_qs = Visitor.objects.filter(ip_address=ip_address)
#     if not ip_qs.exists():
#         user_session = Visitor.objects.create(ip_address=ip_address)
#         if user.is_authenticated:
#             print(Visitor.objects.exists())
#             if Visitor.objects.exists():
#                 if not Visitor.objects.filter(user=user).exists():
#                     user_session.user = user
#         user_session.save()

# user_signal.connect(user_receiver)