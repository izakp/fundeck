from __future__ import absolute_import

from fundeck.celery import app

from fabric.api import execute

from the_deck.models import Task

from the_deck.remote_tasks import run_command_sync

"""
rexecute.apply_async(args=("whoami", ["10.0.4.10", "10.0.4.68"],))
"""

class TaskResponse(object):
    def __init__(self, result=None):
        self.result = result

@app.task
def rsetup(tasklist, hosts):
    responses = []
    for task_id in tasklist:
        task = Task(task_id)
        if task.setup_command is None:
            responses.append(TaskResponse())
            continue
        result = execute(run_command_sync, task.setup_command, hosts=hosts)
        responses.append(TaskResponse(result=result))
    return responses

@app.task
def rpreflight(tasklist, hosts):
    responses = []
    for task_id in tasklist:
        task = Task(task_id)
        if task.preflight_command is None:
            responses.append(TaskResponse())
            continue
        result = execute(run_command_sync, task.preflight_command, hosts=hosts)
        responses.append(TaskResponse(result=result))
    return responses

@app.task
def rexecute(tasklist, hosts):
    responses = []
    for task_id in tasklist:
        task = Task(task_id)
        result = execute(run_command_sync, task.run_command, hosts=hosts)
        responses.append(TaskResponse(result=result))
    return responses

@app.task
def rteardown(tasklist, hosts):
    responses = []
    for task_id in tasklist:
        task = Task(task_id)
        if task.teardown_command is None:
            responses.append(TaskResponse())
            continue
        result = execute(run_command_sync, task.teardown_command, hosts=hosts)
        responses.append(TaskResponse(result=result))
    return responses
