from __future__ import absolute_import

import traceback

from fundeck.celery import app

from the_deck.models import TaskSet
from the_deck.lib.task_result import TaskResult
from the_deck.lib.remote_command import RemoteCommand

from paramiko import SSHException

@app.task
def execute_command(command, host, username):
    try:
        command_runner = RemoteCommand(command, host, username)
        result = command_runner.run()
    except SSHException:
        e = traceback.format_exc()
        return TaskResult(error=e)
    return TaskResult(result=result)

@app.task
def execute_taskset(taskset_id, host):
    taskset = TaskSet(taskset_id)
    responses = []
    for task in taskset.tasks:
        try:
            command_runner = RemoteCommand(task.run_command, host, taskset.remote_user)
            result = command_runner.run()
        except SSHException:
            e = traceback.format_exc()
            responses.append(TaskResult(error=e))
        responses.append(TaskResult(result=result))
    return responses
