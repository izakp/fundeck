from django.db import models

class Host(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=128)
    fqdn = models.CharField(max_length=512, unique=True)

    def __str__(self):
        return self.name
