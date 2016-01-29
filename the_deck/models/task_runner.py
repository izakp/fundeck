from django.db import models
from django.contrib.auth.models import User

from the_deck.models.task_group import TaskGroup

class TaskRunner(models.Model):
    CREATED = 0
    PENDING = 100
    RUNNING = 200
    CONNECTIONS_ESTABLISHED = 300
    ASSETS_PREPARED = 400
    COMMANDS_RUN = 500
    COMPLETE = 600
    FAILED = 700
    SUCCEEDED = 800

    STATES = (
        (CREATED, 'CREATED'),
        (PENDING, 'PENDING'),
        (CONNECTIONS_ESTABLISHED, 'CONNECTIONS_ESTABLISHED'),
        (ASSETS_PREPARED, 'ASSETS_PREPARED'),
        (COMMANDS_RUN, 'COMMANDS_RUN'),
        (COMPLETE, 'COMPLETE'),
        (FAILED, 'FAILED'),
        (SUCCEEDED, 'SUCCEEDED'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    task_group = models.ForeignKey(TaskGroup)
    user = models.ForeignKey(User)
    state = models.IntegerField(choices=STATES, default=CREATED)

    def __str__(self):
        return "%s by %s at %s" % (self.task_group, self.user, self.updated_at)

