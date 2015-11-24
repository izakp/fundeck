from django.db import models

from the_deck.models import Task, Group, UserProfile, Hostset

class Taskset(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tasks = models.ManyToManyField(Task) # TODO order?
    hostsets = models.ManyToManyField(Hostset)
    groups = models.ManyToManyField(Group)
    user_profiles = models.ManyToManyField(UserProfile)

    def get_tasklist(self):
        return [task.id for task in self.tasks] # TODO order?

    def get_hosts(self):
        return [hostset.get_hosts() for hostset in self.hostsets]
