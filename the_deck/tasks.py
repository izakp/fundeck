from __future__ import absolute_import

from datetime import datetime

from paramiko import SSHException

from celery import chord

from fundeck.celery import app

from the_deck.models import TaskRunner, Task

from the_deck.lib.remote_command import RemoteCommand

import logging
logger = logging.getLogger(__name__)

@app.task(bind=True, max_retries=None, default_retry_delay=1)
def task_runner_setup(self, task_runner_id):
    task_runner = TaskRunner.objects.get(id=task_runner_id)
    if task_runner.state != TaskRunner.CREATED:
        logger.error("Invalid state for TaskRunner %s" % task_runner_id)
        return

    if task_runner.task_group.running:
        logger.warning("Task group id %s is already running.  Retrying in 1 second.")
        raise self.retry()

    task_runner.task_group.running = True
    task_runner.task_group.save()

    task_runner.state = TaskRunner.PENDING
    task_runner.save()

    task_runner_run.apply_async(args=[task_runner_id])


@app.task(bind=True)
def task_runner_run(self, task_runner_id):
    task_runner = TaskRunner.objects.get(id=task_runner_id)
    if task_runner.state != TaskRunner.PENDING:
        logger.error("Invalid state for TaskRunner %s" % task_runner_id)
        return

    tasks = [Task.objects.create(task_runner=task_runner,
                                command=task_runner.task_group.command.command,
                                host=host,
                                username=task_runner.task_group.ssh_user.username) for host in task_runner.task_group.collect_hosts()]

    task_runner.state = TaskRunner.RUNNING
    task_runner.save()

    chord([run_task.si(task.id) for task in tasks])(task_runner_on_complete.si(task_runner_id))

@app.task(bind=True)
def run_task(self, task_id):
    def fail_task(task):
        e = traceback.format_exc()
        logger.error(e)
        task.error = e
        task.state = Task.FAILED
        task.save()

    task = Task.objects.get(id=task_id)
    if task.state != Task.CREATED:
        logger.error("Invalid state for Task %s" % task_id)
        return

    try:
        command_runner = RemoteCommand(task.host,
                                    task.username,
                                    task.task_runner.task_group.ssh_user.private_key)
    except Exception:
        return fail_task(task)

    task.state = Task.RUNNING
    task.save()

    remote_files = task.task_runner.task_group.command.remote_files.all()
    for f in remote_files:
        try:
            command_runner.write_file(f.filename, f.content, f.permissions)
        except SSHException:
            return fail_task(task)

    task_start = datetime.now()

    try:
        result = command_runner.run(task.command)
    except SSHException:
        return fail_task(task)

    task_time = datetime.now() - task_start
    task.time = task_time.total_seconds()

    for f in remote_files:
        try:
            command_runner.delete_file(f.filename)
        except SSHException, e:
            return fail_task(task)

    if result.succeeded:
        task.state = Task.SUCCEEDED
    elif result.failed:
        task.state = Task.FAILED

    task.stderr = result.stderr
    task.stdout = result.stdout
    task.status = result.status

    task.save()


@app.task(bind=True)
def task_runner_on_complete(self, task_runner_id):
    def success(tasks):
        for task in tasks:
            if task.state == Task.FAILED:
                return False
        return True

    task_runner = TaskRunner.objects.get(id=task_runner_id)
    if task_runner.state != TaskRunner.RUNNING:
        logger.error("Invalid state for TaskRunner %s" % task_runner_id)
        return

    if success(task_runner.task_set.all()):
        task_runner.state = TaskRunner.SUCCEEDED
    else:
        task_runner.state = TaskRunner.FAILED

    task_runner.save()

    task_runner.task_group.running = False
    task_runner.task_group.save()
