from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=80)
    members = models.ManyToManyField(User)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Task(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    description = models.TextField(max_length=200)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    due_date = models.DateField()
    priority = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    status = models.ForeignKey('Status', on_delete=models.CASCADE) # TODO it's not relevant to delete
                                                                    # a task because the status is deleted
    class Meta:
        ordering = ['priority']

    def __str__(self):
        return self.name


class Journal(models.Model):
    date = models.DateTimeField()
    entry = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE) #TODO a default user that signify that the user is deleted
    task = models.ForeignKey('Task', on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.entry


def get_complete_name(self):
    if self.first_name:
        return self.first_name + " " + self.last_name
    else:
        return self.username
User.add_to_class("__str__", get_complete_name)
