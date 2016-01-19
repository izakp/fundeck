from __future__ import absolute_import

from celery import chord

from fundeck.celery import app

from the_deck.models import TaskRunner, Task

from the_deck.lib.remote_command import RemoteCommand

import logging
logger = logging.getLogger(__name__)

@app.task(name="task_runner_setup")
def task_runner_setup(task_runner_id):
    task_runner = TaskRunner.objects.get(id=task_runner_id)
    task_runner.state = TaskRunner.PENDING
    task_runner.save()

    return task_runner_start.apply_async(args=[task_runner_id])


@app.task(name="task_runner_start")
def task_runner_start(task_runner_id):
    task_runner = TaskRunner.objects.get(id=task_runner_id)
    tasks = [Task.objects.create(task_runner=task_runner,
                                command=task_runner.task_group.command.command,
                                host=host.fqdn,
                                username=task_runner.task_group.ssh_user.username) for host in task_runner.task_group.hosts.all()]

    task_runner.state = TaskRunner.RUNNING
    task_runner.save()

    return chord([run_task.s(task.id) for task in tasks])(task_runner_on_complete.s(task_runner_id))


@app.task(name="run_task")
def run_task(task_id):
    task = Task.objects.get(id=task_id)

    command_runner = RemoteCommand(task.command, 
                                    task.host,
                                    task.username,
                                    task.task_runner.task_group.ssh_user.private_key)
    result = command_runner.run()

    logger.info(task_id)
    logger.info((result.status, result.stderr, result.stdout))

    if result.failed:
        task.state = Task.FAILED
        task.error = result.error
    else:
        task.state = Task.SUCCEEDED
        task.stderr = result.stderr
        task.stdout = result.stdout
        task.status = result.status

    task.save()
    return task_id


@app.task(name=("task_runner_on_complete"))
def task_runner_on_complete(task_ids, task_runner_id):
    def success(tasks):
        for task in tasks:
            if task.state == Task.FAILED:
                return False
        return True

    task_runner = TaskRunner.objects.get(id=task_runner_id)
    tasks = [Task.objects.get(id=tid) for tid in task_ids]
    
    if success(tasks):
        task_runner.state = TaskRunner.SUCCEEDED
    else:
        task_runner.state = TaskRunner.FAILED

    task_runner.save()
    return task_runner_id
