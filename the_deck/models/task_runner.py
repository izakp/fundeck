from django.db import models

from celery import group
from celery.result import GroupResult

from the_deck.models.user import User
from the_deck.models.task_set import TaskSet

from the_deck.exceptions import LockAcquireError

from the_deck.tasks import rsetup, rpreflight, rexecute, rteardown, TaskResult

class TaskRunner(models.Model):
    CREATED = 0
    PENDING = 100
    SETUP = 200
    PREFLIGHT = 300
    RUNNING = 400
    TEARDOWN = 500
    SUCCEEDED = 600
    FAILED = 700

    STATES = (
        (CREATED, 'CREATED'),
        (PENDING, 'PENDING'),
        (SETUP, 'SETUP'),
        (PREFLIGHT, 'PREFLIGHT'),
        (RUNNING, 'RUNNING'),
        (TEARDOWN, 'TEARDOWN'),
        (SUCCEEDED, 'SUCCEEDED'),
        (FAILED, 'FAILED')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    taskset = models.ForeignKey(TaskSet)
    user = models.OneToOneField(User)

    setup_task_id = models.CharField(max_length=128)
    preflight_task_id = models.CharField(max_length=128)
    run_task_id = models.CharField(max_length=128)
    teardown_task_id = models.CharField(max_length=128)

    state = models.IntegerField(choices=STATES, default=CREATED)
    fail_as_group = models.BooleanField(default=False)

    def tick(self):
        if self.is_finalized():
            return None

        if self.state == self.CREATED:
            self.try_acquire_tasklock()
        elif self.state == self.PENDING:
            self.try_setup()
        elif self.state == self.SETUP:
            self.try_preflight()
        elif self.state == self.PREFLIGHT:
            self.try_run()
        elif self.state == self.RUNNING:
            self.try_teardown()
        elif self.state == self.TEARDOWN:
            self.try_finalize()
        elif self.state == SUCCEEDED:
            self.finalize(True)
        elif self.state == FAILED:
            self.finalize(False)

    def create_task_group(self, func):
        signatures = [func.s(self.taskset.get_tasklist(), host, self.taskset.remote_user) for host in self.taskset.get_hosts()]
        return group(signatures)()

    def try_acquire_tasklock(self):
        try:
            self.taskset.tasklock.acquire_lock(self)
        except LockAcquireError:
            return None

        self.state = self.PENDING
        self.save()
        return self

    def try_setup(self):
        if self.taskset.requires_setup():
            return self.setup()
        else:
            return self.try_preflight()

    def setup(self):
        task_group = self.create_task_group(rsetup)
        task_group.save()

        self.setup_task_id = task_group.id
        self.state = self.SETUP
        self.save()
        return self

    def try_preflight(self):
        if self.taskset.requires_setup():
            task_group = GroupResult.restore(self.setup_task_id)
            if not task_group.ready():
                return None

            # TODO handle setup results - TaskResult

        if self.taskset.requires_preflight():
            return self.preflight()
        else:
            return self.run()

    def preflight(self):
        task_group = self.create_task_group(rpreflight)
        self.setup_task_id = task_group.id
        self.state = self.PREFLIGHT
        self.save()
        return self

    def try_run(self):
        if self.taskset.requires_preflight():
            task_group = GroupResult.restore(self.preflight_task_id)
            if not task_group.ready():
                return None

            # TODO handle preflight results - TaskResult

        return self.run()

    def run(self):
        task_group = self.create_task_group(rexecute)
        self.run_task_id = task_group.id
        self.state = self.RUNNING
        self.save()
        return self

    def try_teardown(self):
        task_group = GroupResult.restore(self.run_task_id)
        if not task_group.ready():
            return None

        # TODO handle run results

        if self.taskset.requires_teardown():
            return self.teardown()
        else:
            return self.finalize()

    def teardown(self):
        task_group = self.create_task_group(rteardown)
        self.teardown_task_id = task_group.id
        self.state = self.TEARDOWN
        self.save()
        return self

    def try_finalize(self):
        task_group = GroupResult.restore(self.teardown_task_id)
        if not task_group.ready():
            return None

        # TODO finalize results - TaskResult

        return self.finalize()

    def finalize(self, success):

        self.tasklock.release_lock()

        if success:
            self.state = self.SUCCEEDED
        else:
            self.state = self.FAILED

        self.save()
        return self

    def is_finalized(self):
        return self.state in [self.SUCCEEDED, self.FAILED]
