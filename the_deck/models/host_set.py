from django.db import models

from the_deck.models.static_host import StaticHost
from the_deck.models.inventory import Inventory

class HostSet(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=128)

    static_hosts = models.ManyToManyField(StaticHost)
    inventories = models.ManyToManyField(Inventory)

    def get_hosts(self):
        hosts = []
        for static_host in self.static_hosts:
            if not static_host.is_active:
                continue
            hosts.append(static_host.fqdn)
        for inventory in self.inventories:
        	hosts.extend(inventory.fqdns())
        return hosts
