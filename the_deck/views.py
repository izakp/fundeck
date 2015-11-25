from django.shortcuts import render

import logging
logger = logging.getLogger(__name__)

from the_deck.manager import run_until_complete

def home(request):
    return render(request, "home.html", {})
