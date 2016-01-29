import time
import traceback

from datetime import datetime

import logging
logger = logging.getLogger(__name__)

from paramiko import SSHException

from the_deck.lib.remote_command import RemoteCommand
from the_deck.lib.exceptions import TaskGuardException

from the_deck.models import Task, TaskRunner

class TaskCoordinator(object):
    WAIT = 1

    def __init__(self, task):
        self.task = task
        self.task_runner = task.task_runner
        self.remote_files = task.task_runner.task_group.command.remote_files.all()

    @property
    def run_failed(self):
        return self.task_runner.state == TaskRunner.FAILED

    def fail_on_error(self):
        e = traceback.format_exc()
        self.task.error = e
        self.task.state = Task.FAILED
        self.task.save()
        raise TaskGuardException("Task failed with error %s" % repr(e))

    def _task_wait(self):
        time.sleep(self.WAIT)
        self.task_runner.refresh_from_db()
        if self.run_failed:
            raise TaskGuardException("Task runner failed")

    def establish_connection(self):
        if self.task.state != Task.CREATED:
            raise TaskGuardException("Invlaid task state %s" % self.task.state)

        self.task.state = Task.ESTABLISHING_CONNECTION
        self.task.save()

        try:
            self.command_runner = RemoteCommand(self.task.host,
                                        self.task.username,
                                        self.task.task_runner.task_group.ssh_user.private_key)
        except:
            self.fail_on_error()

    def wait_all_tasks_established_connections(self):
        if self.task.state != Task.ESTABLISHING_CONNECTION:
            raise TaskGuardException("Invlaid task state %s" % self.task.state)

        self.task.state = Task.CONNECTION_ESTABLISHED
        self.task.save()

        while self.task_runner.state < TaskRunner.CONNECTIONS_ESTABLISHED:
            self._task_wait()

        self.task.state = Task.PREPARING_ASSETS
        self.task.save()

    def prepare_assets(self):
        if self.task.state != Task.PREPARING_ASSETS:
            raise TaskGuardException("Invlaid task state %s" % self.task.state)

        for f in self.remote_files:
            try:
                self.command_runner.write_file(f.filename, f.content, f.permissions)
            except:
                self.fail_on_error()

    def wait_all_tasks_prepared_assets(self):
        if self.task.state != Task.PREPARING_ASSETS:
            raise TaskGuardException("Invlaid task state %s" % self.task.state)

        self.task.state = Task.ASSETS_PREPARED
        self.task.save()

        while self.task_runner.state < TaskRunner.ASSETS_PREPARED:
            self._task_wait()

        self.task.state = Task.RUNNING_COMMAND
        self.task.save()

    def run_command(self):
        if self.task.state != Task.RUNNING_COMMAND:
            raise TaskGuardException("Invlaid task state %s" % self.task.state)

        command_start = datetime.now()
        try:
            self.result = self.command_runner.run(self.task.command)
        except:
            self.fail_on_error()
        self.command_runtime = datetime.now() - command_start

    def wait_all_commands_run(self):
        if self.task.state != Task.RUNNING_COMMAND:
            raise TaskGuardException("Invlaid task state %s" % self.task.state)

        self.task.state = Task.COMMAND_RUN
        self.task.save()

        while self.task_runner.state < TaskRunner.COMMANDS_RUN:
            self._task_wait()

        self.task.state = Task.CLEANING_UP
        self.task.save()

    def cleanup_assets(self):
        if self.task.state != Task.CLEANING_UP:
            raise TaskGuardException("Invalid task state %s" % self.task.state)

        for f in self.remote_files:
            try:
                self.command_runner.delete_file(f.filename)
            except:
                self.fail_on_error()

    def wait_all_tasks_completed(self):
        if self.task.state != Task.CLEANING_UP:
            raise TaskGuardException("Invlaid task state %s" % self.task.state)

        self.task.state = Task.COMPLETE
        self.task.save()

        while self.task_runner.state < TaskRunner.COMPLETE:
            self._task_wait()

    def save_task_result(self):
        if self.task.state != Task.COMPLETE:
            raise TaskGuardException("Invlaid task state %s" % self.task.state)

        if self.result.succeeded:
            self.task.state = Task.SUCCEEDED
        elif self.result.failed:
            self.task.state = Task.FAILED

        self.task.time = self.command_runtime.total_seconds()
        self.task.stderr = self.result.stderr
        self.task.stdout = self.result.stdout
        self.task.status = self.result.status

        self.task.save()

