from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Task, Journal, Status
from .form import TaskForm, JournalForm, ProjectForm

##
#Print the home page
#
#@param request    WSGIRequest list with all HTTP Request
##
def home(request):
    return render(request, 'home.html')

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
    my_tasks = Task.objects.filter(project=project).filter(assignee=user)
    tasks = Task.objects.filter(project=project)
    statuss = Status.objects.all()
    members = project.members.all()
    
    permission(user, project) # Checks if the user is a member of the project
    return render(request, 'taskmanager/project.html', {'project': project,
                                                        'my_tasks': my_tasks,
                                                        'tasks': tasks,
                                                        'statuss': statuss,
                                                        'members': members,
                                                        'user': user})



##
# Display one task, details associated and history
# History can be added
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

    ''' New journal entry can always be posted, no specific view '''
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

    return render(request, 'taskmanager/task.html', {'form': form,
                                                     'task': task,
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
# Display every task of the user with the
# associated person responsible for the task
#
# @param request    WSGIRequest list with all HTTP Request
##
@login_required(login_url='/accounts/login/')
def tasks(request):
    user = request.user
    tasks = Task.objects.filter(project__members__in=[user])
    return render(request, 'taskmanager/tasks.html', {'tasks': tasks,
                                                         'user': user})

##
# Display every done task of the user with the
# associated person responsible for the task
#
# @param request    WSGIRequest list with all HTTP Request
##
@login_required(login_url='/accounts/login/')
def tasks_done(request):
    user = request.user
    tasks = Task.objects.filter(project__members__in=[user]).filter(status__name="Terminée")
    done_only = True
    return render(request, 'taskmanager/tasks.html', {'tasks': tasks,
                                                         'user': user,
                                                      'done_only': done_only})

##
# Add a project
#
# @param request     WSGIRequest list with all HTTP Request
##
@login_required(login_url='/accounts/login/')
def newproject(request):
    user = request.user

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)  # Do not save directly in the DB
            project.save()
            form.save_m2m() # Have to save ManyToManyField manually because of "form.save(commit=False)"
            if not user in project.members.all() :
                project.members.add(user)
            project.save()
            return redirect('project', id=project.id)
    else:
        form = ProjectForm()

    return render(request, 'taskmanager/newproject.html', {'form': form,
                                                           'user': user})