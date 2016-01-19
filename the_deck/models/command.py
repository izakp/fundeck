from django.db import models

class Command(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=128)
    command = models.TextField()

    def __str__(self):
        return self.name
