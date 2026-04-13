from django.db import models
from django.conf import settings

class Activity(models.Model):
    ACTION_CHOICES = [
        ("code_explained", "Code Explained"),
        ("debug_request", "Debug Request"),
        ("quiz_attempt", "Quiz Attempt"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.get_action_display()} at {self.timestamp}"
