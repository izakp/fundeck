from chef import ChefAPI, Search

class ChefClient(object):
    def __init__(self, pemfile, username, server_url):
        self.pemfile = pemfile
        self.username = username

    def query(self, query, returning=None):
        instances = []
        with ChefAPI(self.server_url, self.pemfile, self.username):
            res = Search('node', query)
            for row in res.data['rows']:
                if returning is None:
                    instances.append(row)
                else:
                    instances.append(row[returning])
        return instances
