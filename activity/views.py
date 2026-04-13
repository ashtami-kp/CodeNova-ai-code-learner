from django.shortcuts import render
from .models import Activity

def activity_history(request):
    if request.user.is_authenticated:
        activities = Activity.objects.filter(user=request.user).order_by("-timestamp")
    else:
        activities = []

    return render(request, "activity/history.html", {"activities": activities})
