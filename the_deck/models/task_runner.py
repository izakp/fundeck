from django.db import models

from celery import group
from celery.result import GroupResult

from the_deck.models.user import User
from the_deck.models.task_set import TaskSet

from the_deck.exceptions import LockAcquireError

from the_deck.lib.task_result import TaskResult
from the_deck.tasks import rexecute

class TaskRunner(models.Model):
    CREATED = 0
    PENDING = 100
    RUNNING = 200
    SUCCEEDED = 300
    FAILED = 400

    STATES = (
        (CREATED, 'CREATED'),
        (PENDING, 'PENDING'),
        (RUNNING, 'RUNNING'),
        (SUCCEEDED, 'SUCCEEDED'),
        (FAILED, 'FAILED')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    taskset = models.ForeignKey(TaskSet)
    user = models.OneToOneField(User)

    task_id = models.CharField(max_length=128)

    state = models.IntegerField(choices=STATES, default=CREATED)
    fail_as_group = models.BooleanField(default=False)

    def tick(self):
        if self.is_finalized():
            return True

        if self.state == self.CREATED:
            self.try_acquire_tasklock()
        elif self.state == self.PENDING:
            self.try_run()
        elif self.state == self.RUNNING:
            self.try_finalize()

        return False

    def try_acquire_tasklock(self):
        try:
            self.taskset.tasklock.acquire_lock(self)
        except LockAcquireError:
            return None

        self.state = self.PENDING
        self.save()
        return self

    def try_run(self):
        if not self.taskset.tasklock.lock_acquired(self):
            return None
        self.run()

    def run(self):
        signatures = [rexecute.s(self.taskset.get_tasklist(), host, self.taskset.remote_user) for host in self.taskset.get_hosts()]
        task_group_result = group(signatures)()
        task_group_result.save()

        self.task_id = task_group_result.id
        self.state = self.RUNNING
        self.save()
        return self

    def try_finalize(self):
        task_group_result = GroupResult.restore(self.task_id)
        if not task_group_result.ready():
            return None

        # TODO handle results - TaskResult

        return self.finalize(True)

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
