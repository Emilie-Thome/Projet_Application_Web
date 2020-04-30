from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from taskmanager.models import Project, Task, Journal

@login_required(login_url='/accounts/login/')
def projects(request):
    user = request.user
    projects = Project.objects.filter(members__in = [user])
    return render(request, 'taskmanager/projects.html',{'projects': projects})

@login_required(login_url='/accounts/login/')
def project(request, id):
    project = Project.objects.get(id = id)
    tasks = Task.objects.filter(project = project)
    return render(request, 'taskmanager/project.html', {'project' : project, 'tasks' : tasks})

@login_required(login_url='/accounts/login/')
def task(request, id):
    task = Task.objects.get(id = id)
    journals = Journal.objects.filter(task=task)
    return render(request, 'taskmanager/task.html', {'task' : task, 'journals' : journals})