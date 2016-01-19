from django.db import models

class SshUser(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    username = models.CharField(max_length=512, unique=True)
    private_key = models.TextField()

    def __str__(self):
        return self.username
