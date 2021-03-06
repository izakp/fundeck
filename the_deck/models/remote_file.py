from django.db import models

class RemoteFile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    filename = models.CharField(max_length=128)
    content = models.TextField()
    permissions = models.CharField(max_length=4, default="644")

    def __str__(self):
        return self.filename
