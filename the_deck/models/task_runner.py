from django.db import models

from celery import group

from the_deck.models.user import User
from the_deck.models.task_set import TaskSet

from the_deck.exceptions import LockAcquireError

from the_deck.tasks import rsetup, rpreflight, rexecute, rteardown, TaskResponse

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
        if self.state == CREATED:
            self.try_acquire_tasklock()
        elif self.state == PENDING:
            self.try_enter_setup()
        elif self.state == SETUP:
            self.try_enter_preflight()
        elif self.state == PREFLIGHT:
            self.try_run()
        elif self.state == RUNNING:
            self.try_teardown()
        elif self.state == TEARDOWN:
            self.try_finalize()
        # elif self.state == SUCCEEDED:
        #     self.finalize()
        # elif self.state == FAILED:
        #     self.finalize()

    def create_task_group(self, func):
        signatures = [func.s(self.taskset.get_tasklist(), host) for host in self.taskset.get_hosts()]
        return group(signatures)()

    def try_acquire_tasklock(self):
        try:
            self.taskset.tasklock.acquire_lock(self)
        except LockAcquireError:
            pass
        self.state = self.PENDING
        self.save()
        return self

    def try_enter_setup(self):
        pass

    def setup(self):
        task_group = self.create_task_group(rsetup)
        self.setup_task_id = task_group.id
        self.state = self.SETUP
        self.save()
        return self

    def try_enter_preflight(self):
        pass

    def preflight(self):
        task_group = self.create_task_group(rpreflight)
        self.setup_task_id = task_group.id
        self.state = self.PREFLIGHT
        self.save()
        return self

    def try_run(self):
        pass

    def run(self):
        task_group = self.create_task_group(rexecute)
        self.run_task_id = task_group.id
        self.state = self.RUNNING
        self.save()
        return self

    def try_teardown(self):
        pass

    def teardown(self):
        task_group = self.create_task_group(rteardown)
        self.teardown_task_id = task_group.id
        self.state = self.TEARDOWN
        self.save()

        self.tasklock.release_lock()

        return self

    def try_finalize(self):
        pass

    def finalize(self):
        pass
