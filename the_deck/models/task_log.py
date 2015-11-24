from django.db import models

from the_deck.models import Taskrunner

class TaskLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    taskrunner = models.ForeignKey(Taskrunner)
    level = models.CharField(max_length=5)
    log = models.CharField(max_length=512)
