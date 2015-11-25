from django.db import models

from the_deck.models.user_profile import UserProfile

class Group(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=256)

    user_profile = models.ManyToManyField(UserProfile)
