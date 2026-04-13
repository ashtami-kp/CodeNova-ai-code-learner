from django.contrib import admin
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "description", "timestamp")
    list_filter = ("action", "timestamp")
    search_fields = ("user__username", "description")

