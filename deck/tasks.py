from __future__ import absolute_import

from fundeck.celery import app

from fabric.api import execute

from deck.remote_tasks import whoami

@app.task
def rexecute(hosts):
    hosts_as_str = " ".join(hosts)
    return execute(whoami, hosts=hosts)
