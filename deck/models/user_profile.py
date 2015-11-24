from django.db import models

from deck.models import User

class UserProfile(models.Model):
  user = models.OneToOneField(User)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
