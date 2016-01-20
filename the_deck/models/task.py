from django.db import models

from the_deck.models.task_runner import TaskRunner

class Task(models.Model):
    CREATED = 0
    RUNNING = 100
    FAILED = 200
    SUCCEEDED = 300

    STATES = (
        (CREATED, 'CREATED'),
        (RUNNING, 'RUNNING'),
        (FAILED, 'FAILED'),
        (SUCCEEDED, 'SUCCEEDED'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    task_runner = models.ForeignKey(TaskRunner)

    command = models.TextField()
    host = models.CharField(max_length=512)
    username = models.CharField(max_length=512)

    state = models.IntegerField(choices=STATES, default=CREATED)

    stdout = models.TextField(null=True, blank=True)
    stderr = models.TextField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    time = models.FloatField(null=True, blank=True)

    error = models.TextField(null=True, blank=True)

    def __str__(self):
        return 'Run "%s" on %s by %s at %s' % (self.command, self.host, self.username, self.created_at)
