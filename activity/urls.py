from django.urls import path
from .views import activity_history

urlpatterns = [
    path("", activity_history, name="activity_home"),
    path("history/", activity_history, name="activity_history"),
]
