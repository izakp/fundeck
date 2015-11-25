from __future__ import absolute_import

import traceback

from fundeck.celery import app

from the_deck.models.task import Task

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
def execute_tasks(task_ids, host, remote_user):
    results = []
    for task_id in task_ids:
        task = Task(task_id)
        try:
            command_runner = RemoteCommand(task.run_command, host, remote_user)
            result = TaskResult(task=task, result=command_runner.run())
            if result.remote_command_failed: # BREAK ON REMOTE COMMAND FAILURE
                break
        except SSHException:
            e = traceback.format_exc()
            results.append(TaskResult(task=task, error=e))
            break # BREAK ON SSH COMMAND FAILURE
        results.append(result)
    return results
