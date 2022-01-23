from django.db import models
from django.contrib.auth.models import User


class Email(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    email = models.EmailField(max_length=200, unique=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.email


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body
