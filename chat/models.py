from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Contact(models.Model):
    user = models.ForeignKey(
        User, related_name='friends', on_delete=models.CASCADE, db_index=True)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    contact = models.ForeignKey(
        Contact, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.contact.user.username


class Chat(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    participants = models.ManyToManyField(
        Contact, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return self.name
