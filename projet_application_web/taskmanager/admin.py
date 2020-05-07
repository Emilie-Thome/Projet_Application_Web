from django.contrib import admin
from .models import Project, Status, Task, Journal

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)
    list_filter = ('members',)


class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'due_date', 'priority', 'project')
    date_hierarchy = 'start_date'
    ordering = ('due_date', 'priority')
    search_fields = ('name',)
    list_filter = ('project', 'assignee')


class JournalAdmin(admin.ModelAdmin):
    list_display = ('entry', 'date')
    date_hierarchy = 'date'
    ordering = ('date',)
    search_fields = ('entry',)
    list_filter = ('task',)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Journal, JournalAdmin)