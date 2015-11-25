from django.db import models

from the_deck.models.static_host import StaticHost

class HostSet(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    static_hosts = models.ManyToManyField(StaticHost)

    def get_hosts(self):
        #TODO add dynamic inventories
        return [host.ip for host in self.static_hosts]
