from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User)
    # TODO
    def __str__(self):
        return self.name
