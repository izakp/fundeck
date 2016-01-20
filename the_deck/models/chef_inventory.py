from django.db import models

from the_deck.lib.chef_client import ChefClient

class ChefInventory(models.Model):
    class Meta:
        verbose_name_plural = "chef inventories"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=128)
    server_url = models.CharField(max_length=512)
    pem_data = models.TextField()
    username = models.CharField(max_length=512)
    query = models.CharField(max_length=512)

    def __str__(self):
        return self.name

    def hosts(self):
        client = ChefClient(self.server_url, self.pem_data, self.username)
        return client.get_hosts_by_query(self.query)
