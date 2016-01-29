from django.db import models

from the_deck.models.remote_file import RemoteFile

class Command(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=128)
    command = models.CharField(max_length=2048)
    remote_files = models.ManyToManyField(RemoteFile, blank=True)

    def __str__(self):
        return self.name
