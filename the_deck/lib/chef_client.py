from cStringIO import StringIO

from chef import ChefAPI, Search
from chef.rsa import Key

import logging
logger = logging.getLogger(__name__)

class ChefClient(object):
    def __init__(self, chef_server_url, pemdata, username):
        self.chef_server_url = chef_server_url
        self.pemdata = StringIO(pemdata)
        self.username = username

    def get_hosts_by_query(self, query):
        instances = []
        with ChefAPI(self.chef_server_url, self.pemdata, self.username):
            try:
                res = Search('node', query)
                for row in res.data['rows']:
                    instances.append(row['automatic']['fqdn'])
            except Exception, e:
                logger.error(e)
        return instances
