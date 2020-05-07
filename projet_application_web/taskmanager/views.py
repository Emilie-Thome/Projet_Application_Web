from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Task, Journal
from .form import TaskForm, JournalForm

##
# Handle 404 Errors
#
# @param request    WSGIRequest list with all HTTP Request
##
def handler404(request):
    return render(request, '404.html')

##
# Redirect to error404 if the user is not a project member
#
# @param user       The user from request, WSGIRequest list with all HTTP Request
# @param project    The project
##
def permission(user, project):
    if not (user in project.members.all()):
        raise Http404

##
# Display every project of the user with the
# associated members
#
# @param request    WSGIRequest list with all HTTP Request
##
@login_required(login_url='/accounts/login/')
def projects(request):
    user = request.user
    projects = Project.objects.filter(members__in=[user])
    return render(request, 'taskmanager/projects.html', {'projects': projects,
                                                         'user': user})

##
# Display one project tasks and their details
#
# @param request     WSGIRequest list with all HTTP Request
# @param             id The project's ID
##
@login_required(login_url='/accounts/login/')
def project(request, id):
    user = request.user
    project = get_object_or_404(Project, id=id)
    tasks = Task.objects.filter(project=project)

    permission(user, project) # Checks if the user is a member of the project
    return render(request, 'taskmanager/project.html', {'project': project,
                                                            'tasks': tasks,
                                                            'user': user})

##
# Display one task, details associated and history
#
# @param request     WSGIRequest list with all HTTP Request
# @param             id The task's ID
##
@login_required(login_url='/accounts/login/')
def task(request, id):
    user = request.user
    task = get_object_or_404(Task, id=id)
    journals = Journal.objects.filter(task=task)

    permission(user, task.project) # Checks if the user is a member of the project
    return render(request, 'taskmanager/task.html', {'task': task,
                                                     'journals': journals,
                                                     'user': user})

##
# Add a new task to the project
#
# @param request     WSGIRequest list with all HTTP Request
# @param             id The project's ID
##
@login_required(login_url='/accounts/login/')
def newtask(request, id):
    user = request.user
    project = get_object_or_404(Project, id=id)
    permission(user, project) # Checks if the user is a member of the project

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False) # Do not save directly in the DB
            task.project = project # The project is not in the form because it is already defined
            task.save()
            return redirect('task', id=task.id)
    else:
        form = TaskForm()
        # Set assignee choices according to the project members :
        form.fields['assignee'].choices = map((lambda member: (member.id, member)),project.members.all())
        form.fields['assignee'].choices.insert(0,("", '---------')) # Set a placeholder, because it is
                                                                    # removed with the choices setup

    return render(request, 'taskmanager/newtask.html', {'form': form,
                                                        'project': project,
                                                        'user': user})

##
# Edit a task
#
# @param request     WSGIRequest list with all HTTP Request
# @param             id The task's ID
##
@login_required(login_url='/accounts/login/')
def edittask(request, id):
    user = request.user
    task = get_object_or_404(Task, id=id)
    permission(user, task.project) # Checks if the user is a member of the project

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task) # The form is filled with current infos
        if form.is_valid():
            form.save()
            return redirect('task', id=id)
    else:
        form = TaskForm(instance=task) # The form is filled with current infos
        # Set assignee choices according to the project members :
        form.fields['assignee'].choices = map((lambda member: (member.id, member)),task.project.members.all())

    return render(request, 'taskmanager/newtask.html', {'form': form,
                                                        'task': task,
                                                        'user': user})

##
# Add a new journal to the Task
#
# @param request     WSGIRequest list with all HTTP Request
# @param             id The Task's ID
##
@login_required(login_url='/accounts/login/')
def newjournal(request, id):
    user = request.user
    task = get_object_or_404(Task, id=id)
    permission(user, task.project) # Checks if the user is a member of the project

    if request.method == 'POST':
        form = JournalForm(request.POST)
        if form.is_valid():
            journal = form.save(commit=False) # Do not save directly in the DB
            journal.task = task # The project is not in the form because it is already defined
            journal.author = user
            journal.save()
            return redirect('task', id=task.id)
    else:
        form = JournalForm()

    journals = Journal.objects.filter(task=task)
    # Use task.html and add {% if form %}
    return render(request, 'taskmanager/task.html', {'form': form,
                                                     'task': task,
                                                     'journals': journals,
                                                     'user': user})
