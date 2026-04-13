from django.db import models
from django.conf import settings

class CodeRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=30)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
