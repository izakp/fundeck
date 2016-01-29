from django.shortcuts import render
from django.db.models.signals import post_save
from django.dispatch import receiver

import logging
logger = logging.getLogger(__name__)

from the_deck.models import TaskGroup, TaskRunner
from the_deck.tasks import task_run

@receiver(post_save, sender=TaskRunner)
def trigger_task_run(sender, instance, **kwargs):
    if kwargs['created']:
        task_run.apply_async([instance.id])

def home(request):
    return render(request, "home.html", {})
