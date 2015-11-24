from django.db import models

from the_deck.models import Taskset, TaskRunner

class LockAcquireError(Exception):
    pass

class TaskLock(models.Model):
    taskset = models.OneToOneField(Taskset)
    lock_holder = models.OneToOneField(TaskRunner, null=True)

    #Note: In context manger

    def is_locked(self):
        return self.lock is not None

    def acquire_lock(self, task_runner):
        if self.is_locked():
            raise LockAcquireError()
        self.lock_holder = task_runner
        self.save()
        return self

    def release_lock(self):
        self.lock_holder = None
        self.save()
        return self
