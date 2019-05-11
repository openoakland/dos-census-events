from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import Event

def index(request):
    return render(request, 'index.html')

@staff_member_required
def pending_events(request):
    events = Event.objects.filter(approval_status="PENDING")
    return render(request, 'pending_events.html', {'events': events})