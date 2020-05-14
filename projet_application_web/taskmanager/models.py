from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Project model
class Project(models.Model):
    name = models.CharField(max_length=80, verbose_name="Project name")
    members = models.ManyToManyField(User, verbose_name="Project members")

    class Meta:
        verbose_name = "project"
        # Ordering rule for 'view.projects'
        ordering = ['name']

    def __str__(self):
        return self.name

# Status model
class Status(models.Model):
    name = models.CharField(max_length=30, verbose_name="Status name")

    class Meta:
        verbose_name = "status"

    def __str__(self):
        return self.name

# Task model
class Task(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name="Task project")
    name = models.CharField(max_length=80, verbose_name="Task name")
    description = models.TextField(max_length=200, verbose_name="Task description")
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Task assignee")
    start_date = models.DateField(verbose_name="Task start date")
    due_date = models.DateField(verbose_name="Task due date")
    priority = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    status = models.ForeignKey('Status', on_delete=models.CASCADE, verbose_name="Task status") # TODO it's not relevant to delete
                                                                    # a task because the status is deleted

    modified = models.DateTimeField(default=timezone.now, verbose_name="Modified date")

    class Meta:
        verbose_name = "task"
        # Ordering rule for 'view.project'
        ordering = ['priority', 'status', 'due_date', 'modified']

    def __str__(self):
        return self.name

# Journal model
class Journal(models.Model):
    date = models.DateTimeField(default=timezone.now, verbose_name="Post date")
    entry = models.CharField(max_length=200, verbose_name="Journal entry")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Journal author") #TODO a default user that signify that the user is deleted
    task = models.ForeignKey('Task', on_delete=models.CASCADE, verbose_name="Journal task")

    class Meta:
        verbose_name = "journal"
        # Ordering rule for 'view.task'
        ordering = ['date']

    def __str__(self):
        return self.entry

# Set the user __str__ as their first/last name if it exists
# but if it don't then use the username
def get_complete_name(self):
    if self.first_name:
        return self.first_name + " " + self.last_name
    else:
        return self.username
User.add_to_class("__str__", get_complete_name)
