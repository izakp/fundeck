from __future__ import absolute_import

import traceback

from fundeck.celery import app

from the_deck.models import Task
from the_deck.lib.task_result import TaskResult
from the_deck.lib.remote_command import RemoteCommand

from paramiko import SSHException

@app.task
def rexecute(tasklist, host, username):
    responses = []
    for task_id in tasklist:
        task = Task(task_id)
        try:
            command_runner = RemoteCommand(task.run_command, host, username)
            result = command_runner.run()
        except SSHException:
            e = traceback.format_exc()
            responses.append(TaskResult(error=e))
        responses.append(TaskResult(result=result))
    return responses
