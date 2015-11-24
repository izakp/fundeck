from django.db import models

from the_deck.models import User

class UserProfile(models.Model):
  user = models.OneToOneField(User)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  is_admin = models.BooleanField(default=False)
