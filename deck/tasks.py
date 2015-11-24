from __future__ import absolute_import

from fundeck.celery import app

from fabric.api import execute

from deck.remote_tasks import run_command_sync, run_command_parallel

"""
rexecute.apply_async(args=(["10.0.4.10", "10.0.4.68"],))
"""

@app.task
def rexecute(hosts, parallel=False):
    if parallel:
        return execute(run_command_parallel, hosts=hosts)
    else:
        return execute(run_command_sync, hosts=hosts)
