from django.db import models

from the_deck.models import Command
from the_deck.models.host import Host
from the_deck.models.ssh_user import SshUser

class TaskGroup(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    command = models.ForeignKey(Command)
    hosts = models.ManyToManyField(Host)
    ssh_user = models.ForeignKey(SshUser)

    def __str__(self):
        return 'Run "%s" on %s' % (self.command, [str(h.name) for h in self.hosts.all()])
