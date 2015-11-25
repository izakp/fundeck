from __future__ import absolute_import

from fundeck.celery import app

from fabric.api import execute

from the_deck.models import Task

from the_deck.remote_tasks import run_paramiko

from paramiko import SSHException

"""
rexecute.apply_async(args=("whoami", ["10.0.4.10", "10.0.4.68"],))
"""

class TaskResult(object):
    def __init__(self, result=None, error=None):
        if result is None and error is None:
            self.empty = True
            return

        self.empty = False

        if result is not None:
            self.failed = False
            self.error = None
            stdout_buf, stderr_buf, status = result
            self.stdout = stdout_buf
            self.stderr = stderr_buf
            self.status = status

        elif error is not None:
            self.failed = True
            self.error = repr(e) #TODO traceback
            self.stdout = None
            self.stderr = None
            self.status = None

    def human_result(self):
        if self.empty:
            return None

        if self.failed:
            return self.error

        if self.status != 0:
            return self.stderr.splitlines()

        return self.stdout.splitlines()


@app.task
def rsetup(tasklist, host, username):
    responses = []
    for task_id in tasklist:
        task = Task(task_id)
        if task.setup_command is None:
            responses.append(TaskResult())
            continue
        try:
            result = run_paramiko(task.setup_command, host=host, username=username)
        except SSHException, e:
            responses.append(TaskResult(error=e))
        responses.append(TaskResult(result=result))
    return responses

@app.task
def rpreflight(tasklist, host, username):
    responses = []
    for task_id in tasklist:
        task = Task(task_id)
        if task.preflight_command is None:
            responses.append(TaskResult())
            continue
        try:
            result = run_paramiko(task.preflight_command, host=host, username=username)
        except SSHException, e:
            responses.append(TaskResult(error=e))
        responses.append(TaskResult(result=result))
    return responses

@app.task
def rexecute(tasklist, host, username):
    responses = []
    for task_id in tasklist:
        task = Task(task_id)
        try:
            result = run_paramiko(task.run_command, host=host, username=username)
        except SSHException, e:
            responses.append(TaskResult(error=e))
        responses.append(TaskResult(result=result))
    return responses

@app.task
def rteardown(tasklist, host, username):
    responses = []
    for task_id in tasklist:
        task = Task(task_id)
        if task.teardown_command is None:
            responses.append(TaskResult())
            continue
        try:
            result = run_paramiko(task.teardown_command, host=host, username=username)
        except SSHException, e:
            responses.append(TaskResult(error=e))
        responses.append(TaskResult(result=result))
    return responses
