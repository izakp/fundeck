from django.shortcuts import render

import logging
logger = logging.getLogger(__name__)

from the_deck.models import TaskGroup, TaskRunner

def home(request):
    return render(request, "home.html", {})

def run_task_group(request):
    return render(request, "task_runner.html", {})
