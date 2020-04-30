from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User)
    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Task(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE) # TODO, limit_choices_to=project.members)
    start_date = models.DateField()
    due_date = models.DateField()
    priority = models.IntegerField()
    status = models.ForeignKey('Status', on_delete=models.CASCADE) # TODO it's not relevant to delete
                                                                    # a task because the status is deleted
class Journal(models.Model):
    date = models.DateField()
    entry = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE) #TODO a default user that signify that the user is deleted
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
