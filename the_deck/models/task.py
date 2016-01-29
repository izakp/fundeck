from django.db import models

from the_deck.models.task_runner import TaskRunner

class Task(models.Model):
    CREATED = 0
    ESTABLISHING_CONNECTION = 100
    CONNECTION_ESTABLISHED = 150
    PREPARING_ASSETS = 200
    ASSETS_PREPARED = 250
    RUNNING_COMMAND = 300
    COMMAND_RUN = 350
    CLEANING_UP = 400
    COMPLETE = 500
    FAILED = 600
    SUCCEEDED = 700

    STATES = (
        (CREATED, 'CREATED'),
        (ESTABLISHING_CONNECTION, 'ESTABLISHING_CONNECTION'),
        (CONNECTION_ESTABLISHED, 'CONNECTION_ESTABLISHED'),
        (PREPARING_ASSETS, 'PREPARING_ASSETS'),
        (ASSETS_PREPARED, 'ASSETS_PREPARED'),
        (RUNNING_COMMAND, 'RUNNING_COMMAND'),
        (COMMAND_RUN, 'COMMAND_RUN'),
        (CLEANING_UP, 'CLEANING_UP'),
        (COMPLETE, 'COMPLETE'),
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
