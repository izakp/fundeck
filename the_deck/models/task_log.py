from django.db import models

class TaskLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    taskrunner = models.ForeignKey('TaskRunner')
    level = models.CharField(max_length=5, default="INFO")
    log = models.CharField(max_length=512)
