from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from taskmanager.models import Project, Task, Journal, Status
from taskmanager.form import TaskForm


def permission(user, project):
    if not (user in project.members.all()):
        raise Http404

@login_required(login_url='/accounts/login/')
def projects(request):
    ''' Display every project of the user '''
    user = request.user
    projects = Project.objects.filter(members__in=[user])
    return render(request, 'taskmanager/projects.html', {'projects': projects,
                                                         'user': user})


@login_required(login_url='/accounts/login/')
def project(request, id):
    ''' Display one project with the members '''
    user = request.user
    project = get_object_or_404(Project, id=id)
    tasks = Task.objects.filter(project=project)

    permission(user, project)
    return render(request, 'taskmanager/project.html', {'project': project,
                                                            'tasks': tasks,
                                                            'user': user})


@login_required(login_url='/accounts/login/')
def task(request, id):
    ''' Display a task with the detail '''
    user = request.user
    task = get_object_or_404(Task, id=id)
    journals = Journal.objects.filter(task=task)

    permission(user, task.project)
    return render(request, 'taskmanager/task.html', {'task': task,
                                                         'journals': journals,
                                                         'user': user})




@login_required(login_url='/accounts/login/')
def newtask(request, id):
    ''' Add a new task to the project '''
    project = get_object_or_404(Project, id=id)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False) # Do not save directly in the DB
            task.project = project
            task.save()
            return redirect('task', id=task.id)
    else:
        form = TaskForm()
        form.assignee.choices = project.members.all()

    user = request.user
    return render(request, 'taskmanager/newtask.html', {'form': form,
                                                        'user': user})


@login_required(login_url='/accounts/login/')
def edittask(request, id):
    ''' Edit the task '''
    task = get_object_or_404(Task, id=id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task', id=id)
    else:
        form = TaskForm(instance=task)
        form.fields['assignee'].choices = map((lambda member: (member.id, member)),task.project.members.all())
        form.fields['status'].choices = map((lambda stat: (stat.id, stat)),Status.objects.all())

    user = request.user
    return render(request, 'taskmanager/newtask.html', {'form': form,
                                                        'task': task,
                                                        'user': user})
