from django.contrib import admin
from .models import Project, Status, Task

admin.site.register(Project)
admin.site.register(Status)
admin.site.register(Task)