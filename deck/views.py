from django.shortcuts import render

from deck.tasks import rexecute

def home(request):
    return render(request, "home.html", {})
