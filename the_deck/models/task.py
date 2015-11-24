from django.db import models

class Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    setup_command = models.CharField(max_length=512, null=True)
    preflight_command = models.CharField(max_length=512, null=True)
    run_command = models.CharField(max_length=512, blank=False)
    teardown_command = models.CharField(max_length=512, null=True)
