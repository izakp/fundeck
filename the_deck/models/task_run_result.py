from django.db import models

from the_deck.models.task_runner import TaskRunner

class TaskRunResult(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    task_runner = models.ForeignKey(TaskRunner)
    result = models.TextField()
    is_error = models.BooleanField(default=False)
