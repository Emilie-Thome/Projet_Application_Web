from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from taskmanager.models import Project, Task, Journal, Status
from taskmanager.form import TaskForm
from django.contrib.auth.models import User

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

def newtask(request):
    user = request.user
    projects = Project.objects.filter(members__in = [user])
    assignees = User.objects.all() #TODO filter by selected project
    all_status = Status.objects.all()
    if request.method == 'POST':
        form = TaskForm(request.POST or None)
        if form.is_valid():
            task = Task()
            task.project = form.cleaned_data["project"]
            task.name = form.cleaned_data["name"]
            task.description = form.cleaned_data["description"]
            task.assignee = form.cleaned_data["assignee"]
            task.start_date = form.cleaned_data["start_date"]
            task.due_date = form.cleaned_data["due_date"]
            task.priority = form.cleaned_data["priority"]
            task.status = form.cleaned_data["status"]
            task.save()

            base_url = "task/"  # 1 /products/
            id = task.id  # 2 category=42
            url = '{}{}'.format(base_url, id)  # 3 /products/category=42
            return redirect(url)
    else:
        form = TaskForm()
    return render(request, 'taskmanager/newtask.html', {
        'form': form,
        'projects' : projects,
        'assignees' : assignees,
        'all_status' : all_status
    })