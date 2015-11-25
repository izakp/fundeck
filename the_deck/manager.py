from __future__ import absolute_import

from fundeck.celery import app

from the_deck.models.task_runner import TaskRunner

@app.task(bind=True, max_retries=None)
def run_until_complete(self, taskrunner_id):
    taskrunner = TaskRunner(taskrunner_id)
    complete = taskrunner.tick()
    if not complete:
        raise self.retry(countdown=1)
