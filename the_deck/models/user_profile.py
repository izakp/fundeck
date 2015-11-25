from django.db import models

from django.contrib.auth.models import User

class UserProfile(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  user = models.OneToOneField(User)
  username = models.CharField(max_length=128)

  is_admin = models.BooleanField(default=False)
