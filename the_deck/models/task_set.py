from django.db import models

from the_deck.models.task import Task
from the_deck.models.host_set import HostSet

from the_deck.lib.helpers import flatten

class TaskSet(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=128)

    remote_user = models.CharField(max_length=128)
    hostsets = models.ManyToManyField(HostSet)
    tasks = models.ManyToManyField(Task, through='TaskList')

    def get_task_ids(self):
        return [task.id for task in self.tasks]

    def get_hosts(self):
        return flatten([hostset.get_hosts() for hostset in self.hostsets])

class TaskList(models.Model):
    order = models.PositiveIntegerField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    taskset = models.ForeignKey(TaskSet, on_delete=models.CASCADE)
