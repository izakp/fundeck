import time
import traceback

from functools import wraps

import logging
logger = logging.getLogger(__name__)

from the_deck.models import Task, TaskRunner

from the_deck.lib.exceptions import RunGuardException

def run_guard(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        if self.failed:
            raise RunGuardException("Run coordinator failed")
        if self.any_task_failed:
            self._fail()
        return func(*args, **kwargs)
    return wrapper

class RunCoordinator(object):
    WAIT = 1

    def __init__(self, task_runner):
        self.task_runner = task_runner

    @property
    def failed(self):
        return self.task_runner.state == TaskRunner.FAILED

    @property
    def any_task_failed(self):
        for task in self.task_runner.task_set.all():
            if task.state == Task.FAILED:
                return True
        return False

    def _fail(self):
        self.task_runner.state = TaskRunner.FAILED
        self.task_runner.save()
        self._release_task_group_lock()
        raise RunGuardException("Run coordinator failed")

    def _succeed(self):
        self.task_runner.state = TaskRunner.SUCCEEDED
        self.task_runner.save()
        self._release_task_group_lock()

    def _release_task_group_lock(self):
        self.task_runner.task_group.running = False
        self.task_runner.task_group.save()

    @run_guard
    def acquire_task_group_lock(self):
        if self.task_runner.state != TaskRunner.CREATED:
            self._fail()

        if self.task_runner.task_group.running:
            return False

        self.task_runner.task_group.running = True
        self.task_runner.task_group.save()

        self.task_runner.state = TaskRunner.PENDING
        self.task_runner.save()

        return True

    @run_guard
    def prepare_tasks(self, run_task):
        if self.task_runner.state != TaskRunner.PENDING:
            self._fail()

        self.task_runner.state = TaskRunner.RUNNING
        self.task_runner.save()

        hosts = self.task_runner.task_group.collect_hosts()
        tasks = [Task.objects.create(task_runner=self.task_runner,
                                        command=self.task_runner.task_group.command.command,
                                        host=host,
                                        username=self.task_runner.task_group.ssh_user.username) for host in hosts]
        for task in tasks:
            run_task.apply_async(args=[task.id])

    @run_guard
    def ensure_tasks_establish_connections(self):
        if self.task_runner.state != TaskRunner.RUNNING:
            self._fail()

        while not self._all_tasks_have_established_connections():
            time.sleep(self.WAIT)

        self.task_runner.state = TaskRunner.CONNECTIONS_ESTABLISHED
        self.task_runner.save()

    def _all_tasks_have_established_connections(self):
        for task in self.task_runner.task_set.all():
            if task.state < Task.CONNECTION_ESTABLISHED:
                return False
        return True

    @run_guard
    def ensure_tasks_prepare_assets(self):
        if self.task_runner.state != TaskRunner.CONNECTIONS_ESTABLISHED:
            self._fail()

        while not self._all_tasks_have_prepared_assets():
            time.sleep(self.WAIT)

        self.task_runner.state = TaskRunner.ASSETS_PREPARED
        self.task_runner.save()

    def _all_tasks_have_prepared_assets(self):
        for task in self.task_runner.task_set.all():
            if task.state < Task.ASSETS_PREPARED:
                return False
        return True

    @run_guard
    def ensure_commands_run(self):
        if self.task_runner.state != TaskRunner.ASSETS_PREPARED:
            self._fail()

        while not self._all_tasks_have_run_commands():
            time.sleep(self.WAIT)

        self.task_runner.state = TaskRunner.COMMANDS_RUN
        self.task_runner.save()

    def _all_tasks_have_run_commands(self):
        for task in self.task_runner.task_set.all():
            if task.state < Task.COMMAND_RUN:
                return False
        return True

    @run_guard
    def ensure_tasks_complete(self):
        if self.task_runner.state != TaskRunner.COMMANDS_RUN:
            self._fail()

        while not self._all_tasks_have_completed():
            time.sleep(self.WAIT)

        self.task_runner.state = TaskRunner.COMPLETE
        self.task_runner.save()

    def _all_tasks_have_completed(self):
        for task in self.task_runner.task_set.all():
            if task.state < Task.COMPLETE:
                return False
        return True

    @run_guard
    def finalize_run(self):
        if self.task_runner.state != TaskRunner.COMPLETE:
            self._fail()
        self._succeed()
