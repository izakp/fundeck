from __future__ import absolute_import

from fundeck.celery import app

from celery.exceptions import SoftTimeLimitExceeded

from the_deck.models import TaskRunner, Task

from the_deck.lib.run_coordinator import RunCoordinator
from the_deck.lib.task_coordinator import TaskCoordinator
from the_deck.lib.exceptions import RunGuardException, TaskGuardException

import logging
logger = logging.getLogger(__name__)

TASK_TIME_LIMIT = 600

@app.task(bind=True, max_retries=None, default_retry_delay=1, soft_time_limit=TASK_TIME_LIMIT)
def task_run(self, task_runner_id):
    app.control.pool_grow(1)
    try:
        task_runner = TaskRunner.objects.get(id=task_runner_id)

        logger.info("run_coordinator.__init__")
        run_coordinator = RunCoordinator(task_runner)

        logger.info("run_coordinator.acquire_task_group_lock")
        if not run_coordinator.acquire_task_group_lock():
            logger.warning("Task group %s is already running.  Retrying in 1 second." % run_coordinator.task_runner.task_group.id)
            raise self.retry()

        logger.info("run_coordinator.prepare_tasks")
        run_coordinator.prepare_tasks(app.control.pool_grow, run_task)
        logger.info("run_coordinator.ensure_tasks_establish_connections")
        run_coordinator.ensure_tasks_establish_connections()
        logger.info("run_coordinator.ensure_tasks_prepare_assets")
        run_coordinator.ensure_tasks_prepare_assets()
        logger.info("run_coordinator.ensure_commands_run")
        run_coordinator.ensure_commands_run()
        logger.info("run_coordinator.ensure_tasks_complete")
        run_coordinator.ensure_tasks_complete()
        logger.info("run_coordinator.finalize_run")
        run_coordinator.finalize_run()
    except SoftTimeLimitExceeded:
        run_coordinator.fail()
    except RunGuardException, e:
        logger.error(e)

@app.task(bind=True, soft_time_limit=TASK_TIME_LIMIT)
def run_task(self, task_id):
    try:
        task = Task.objects.get(id=task_id)
        logger.info("task_coordinator.__init__")
        task_coordinator = TaskCoordinator(task)
        logger.info("task_coordinator.establish_connection")
        task_coordinator.establish_connection()
        logger.info("task_coordinator.wait_all_tasks_established_connections")
        task_coordinator.wait_all_tasks_established_connections()
        logger.info("task_coordinator.prepare_assets")
        task_coordinator.prepare_assets()
        logger.info("task_coordinator.wait_all_tasks_prepared_assets")
        task_coordinator.wait_all_tasks_prepared_assets()
        logger.info("task_coordinator.run_command")
        task_coordinator.run_command()
        logger.info("task_coordinator.wait_all_commands_run")
        task_coordinator.wait_all_commands_run()
        logger.info("task_coordinator.cleanup_assets")
        task_coordinator.cleanup_assets()
        logger.info("task_coordinator.wait_all_tasks_completed")
        task_coordinator.wait_all_tasks_completed()
        logger.info("task_coordinator.save_task_result")
        task_coordinator.save_task_result()
    except SoftTimeLimitExceeded:
        task_coordinator.fail_on_error()
    except TaskGuardException, e:
        logger.error(e)

