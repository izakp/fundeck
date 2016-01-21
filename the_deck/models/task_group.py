from django.db import models

from the_deck.models import Command
from the_deck.models.host import Host
from the_deck.models.ssh_user import SshUser
from the_deck.models.chef_inventory import ChefInventory

class TaskGroup(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=128)
    command = models.ForeignKey(Command)
    hosts = models.ManyToManyField(Host, blank=True)
    chef_inventories = models.ManyToManyField(ChefInventory, blank=True)
    ssh_user = models.ForeignKey(SshUser)
    running = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def collect_hosts(self):
        all_hosts = []
        for host in self.hosts.all():
            all_hosts.append(host.fqdn)
        for chef_inventory in self.chef_inventories.all():
            all_hosts.extend(chef_inventory.hosts())
        return all_hosts
