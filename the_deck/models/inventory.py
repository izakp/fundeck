from django.db import models

from the_deck.lib.chef_client import ChefClient

class Inventory(models.Model):
    class Meta:
        verbose_name_plural = "inventories"

    CHEF_CLIENT = 0

    CLIENTS = (
        (CHEF_CLIENT, 'CHEF_CLIENT'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=128)

    adapter = models.IntegerField(choices=CLIENTS, default=CHEF_CLIENT)
    query = models.CharField(max_length=512)

    def get_adapter(self):
        if self.adapter == self.CHEF_CLIENT:
            return ChefClient()

    def fqdns(self):
    	return self.get_adapter().query(self.query, returning="fqdn")
