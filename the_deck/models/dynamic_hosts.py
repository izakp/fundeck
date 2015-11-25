import json

from django.db import models

class DynamicHosts(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    adapter = models.CharField(max_length=128)
    query_parameters = models.CharField(max_length=128, blank=True)

    def ips(self):
    	# Dynamic import of module named "adapter" from adapters directory
    	# instantiate adapter
    	# return adapter_instance.get_hosts(self.get_query_parameters)
    	# return a list of ips / FQDNs
    	pass

    def get_query_parameters(self):
    	if self.query_parameters is None:
    		return []
    	return json.loads(self.query_parameters)

    def set_query_parameters(self, *args):
    	self.query_parameters = json.dumps(*args)
    	self.save()
    	return self
