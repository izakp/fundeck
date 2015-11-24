from django.db import models

from the_deck.models import UserProfile

class Group(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user_profile = models.ManyToManyField(UserProfile)
