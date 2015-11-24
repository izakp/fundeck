from django.db import models

class Host(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ip = models.CharField(max_length=128)
