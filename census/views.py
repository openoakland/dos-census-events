from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def pending_events(request):
    return render(request, 'pending_events.html')