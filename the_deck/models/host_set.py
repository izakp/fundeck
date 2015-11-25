from django.db import models

from the_deck.models.static_host import StaticHost
from the_deck.models.dynamic_hosts import DynamicHosts

class HostSet(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    static_hosts = models.ManyToManyField(StaticHost)
    dynamic_hosts = models.ManyToManyField(DynamicHosts)

    def get_hosts(self):
        hosts = []
        for static_host in self.static_hosts:
            if not static_host.is_active:
                continue
            hosts.append(static_host.fqdn)
        for dynamic_host in self.dynamic_hosts:
        	hosts.extend(dynamic_host.fqdns())
        return hosts
