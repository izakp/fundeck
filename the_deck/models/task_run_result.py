from django.db import models

class TaskRunResult(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey('Task')
    task_runner = models.ForeignKey('TaskRunner')
    result = models.TextField()
    is_error = models.BooleanField(default=False)
