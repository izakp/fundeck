from django.db import models

class StaticHost(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=128)

    fqdn = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
