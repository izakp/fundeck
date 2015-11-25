from django.shortcuts import render

from the_deck.tasks import rexecute

import logging
logger = logging.getLogger(__name__)

def home(request):
    return render(request, "home.html", {})
