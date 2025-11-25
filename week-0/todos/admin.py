from django.contrib import admin
from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    """Admin interface for Todo model."""

    list_display = ['title', 'due_date', 'resolved', 'created_at']
    list_filter = ['resolved', 'due_date', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['resolved']
    date_hierarchy = 'due_date'
