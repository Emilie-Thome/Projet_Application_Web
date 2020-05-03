from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from taskmanager.models import Project, Task, Journal, Status
from taskmanager.form import TaskForm
from django.contrib.auth.models import User

@login_required(login_url='/accounts/login/')
def projects(request):
    user = request.user
    projects = Project.objects.filter(members__in = [user])
    return render(request, 'taskmanager/projects.html',{'projects': projects,
                                                        'user' : user})

@login_required(login_url='/accounts/login/')
def project(request, id):
    user = request.user
    project = Project.objects.get(id = id)
    tasks = Task.objects.filter(project = project)
    return render(request, 'taskmanager/project.html', {'project' : project,
                                                        'tasks' : tasks,
                                                        'user' : user})

@login_required(login_url='/accounts/login/')
def task(request, id):
    user = request.user
    task = Task.objects.get(id = id)
    journals = Journal.objects.filter(task=task)
    return render(request, 'taskmanager/task.html', {'task' : task,
                                                     'journals' : journals,
                                                     'user' : user})

@login_required(login_url='/accounts/login/')
def newtask(request, id):
    project = Project.objects.get(id=id)
    if request.method == 'POST':
        form = TaskForm(request.POST or None)
        if form.is_valid():
            task = form.save()
            return redirect('task', id=task.id)
    else:
        form = TaskForm()

    user = request.user
    assignees = project.members.all()
    all_status = Status.objects.all()
    action = "/taskmanager/newtask"
    return render(request, 'taskmanager/newtask.html', {'form': form,
                                                        'project': project,
                                                        'assignees' : assignees,
                                                        'all_status' : all_status,
                                                        'action' : action,
                                                        'user' : user})

@login_required(login_url='/accounts/login/')
def edittask(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task', id=id)
    else:
        form = TaskForm(instance=task)

    user = request.user
    assignees = task.project.members.all()
    all_status = Status.objects.all()
    action = "/taskmanager/edittask/{}".format(id)
    return render(request, 'taskmanager/newtask.html', {'form': form,
                                                        'assignees' : assignees,
                                                        'all_status' : all_status,
                                                        'action' : action,
                                                        'task' : task,
                                                        'user' : user})
