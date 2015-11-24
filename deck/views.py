from django.shortcuts import render

from deck.tasks import rexecute

def home(request):
    rexecute.apply_async(args=(["10.0.4.10", "10.0.4.68"],))
    return render(request, "home.html", {})
