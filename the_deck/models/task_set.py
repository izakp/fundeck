from django.db import models

from the_deck.models.task import Task
from the_deck.models.group import Group
from the_deck.models.user_profile import UserProfile
from the_deck.models.host_set import HostSet

class TaskSet(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tasks = models.ManyToManyField(Task) # TODO order?
    hostsets = models.ManyToManyField(HostSet)
    groups = models.ManyToManyField(Group)
    user_profiles = models.ManyToManyField(UserProfile)

    def get_tasklist(self):
        return [task.id for task in self.tasks] # TODO order?

    def get_hosts(self):
        return [hostset.get_hosts() for hostset in self.hostsets]
