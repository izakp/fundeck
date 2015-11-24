from django.shortcuts import render

from the_deck.tasks import rexecute

import logging
logger = logging.getLogger(__name__)

def home(request):
    res = rexecute.apply_async(args=("ls -lah", ["10.0.4.10", "10.0.4.68"],))
    result = res.get()

    ctx = {
        "status": res.status
    }

    if res.successful():
        ctx['results'] = []
        for host, response in result.items():
            ctx['results'].append((host, response.splitlines()))
    else:
        ctx['error'] == str(result)

    return render(request, "home.html", ctx)
