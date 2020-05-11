from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Project, Task, Journal, Status
from .form import TaskForm
import csv
import xlwt
from django.contrib.auth.models import User

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
# export and donwload data into a csv file
#
# @param request     WSGIRequest list with all HTTP Request
#
##
@login_required(login_url='/accounts/login/')
def download_data_csv(request):
    projects = Project.objects.all()
    tasks = Task.objects.all()
    statuss = Status.objects.all()
    journals = Journal.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-disposition']='attachment; filename=taskmanager.csv'

    writer = csv.writer(response, delimiter=',')

    #projects
    writer.writerow(['Project_name', 'Project_members'])
    """Pour l'instant les membres apparaitront sous la forme d'une liste au format [user1, user2,...]"""
    for project in projects:
        members=[]
        for member in project.members.all():
            members.append(member.username)
        writer.writerow([project.name, members])

    writer.writerow([])

    #status
    writer.writerow(['Status name'])
    for status in statuss:
        writer.writerow([status.name])

    writer.writerow([])
    #tasks
    writer.writerow(
        ['Task project',
         'Task name',
         'Task description',
         'Task assignee',
         'Task start_date',
         'Task due_date',
         'Task priority',
         'Task status'])

    for task in tasks:
        writer.writerow(
            [task.project.name,
             task.name,
             task.description,
             task.start_date,
             task.due_date,
             task.priority,
             task.status])

    writer.writerow([])

    #journal
    writer.writerow(
        ['Journal date', 'Journal entry', 'Journal author', 'Journal task']
    )

    for journal in journals:
        writer.writerow(
            [journal.date, journal.entry, journal.author, journal.task]
        )
    return response

##
# export and donwload data into a xls file
#
# @param request     WSGIRequest list with all HTTP Request
#
##
@login_required(login_url='/accounts/login/')
def download_data_xls(request):
    users = User.objects.all()
    projects = Project.objects.all()
    tasks = Task.objects.all()
    statuss = Status.objects.all()
    journals = Journal.objects.all()


    response = HttpResponse(content_type='application/ms-excel')
    response['Content-disposition'] = 'attachment; filename=taskmanager.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    style = xlwt.Style.easyxf(num_format_str="dd/mm/yy")
    #Users
    wu = wb.add_sheet("Users")

    row = 0
    fields = ["username",
              "first_name",
              "last_name",
              "email"]

    for i in range(len(fields)):
        wu.write(row, i, fields[i])

    for user in users:
        row +=1
        wu.write(row, 0, user.username)
        wu.write(row, 1, user.first_name)
        wu.write(row, 2, user.last_name)
        wu.write(row, 3, user.email)


    #Projects
    wp = wb.add_sheet("Projects")

    row=0
    fields=["name",
            "members"]
    for i in range(len(fields)):
        wp.write(row,i,fields[i])

    for project in projects:
        row+=1
        wp.write(row,0,project.name)
        col=0
        for member in project.members.all():
            col+=1
            wp.write(row,col, member.username)


    #Tasks
    wt = wb.add_sheet("Tasks")

    row=0
    fields=['project',
         'name',
         'description',
         'assignee',
         'start_date',
         'due_date',
         'priority',
         'status']

    for i in range(len(fields)):
        wt.write(row,i,fields[i])

    for task in tasks:
        row+=1
        wt.write(row, 0, task.project.name)
        wt.write(row, 1, task.name)
        wt.write(row, 2, task.description)
        wt.write(row, 3, task.assignee.username)
        wt.write(row, 4, task.start_date, style)
        wt.write(row, 5, task.due_date, style)
        wt.write(row, 6, task.priority)
        wt.write(row, 7, task.status.name)


     #Status
    ws = wb.add_sheet("Status")

    row=0
    fields=['name']
    for i in range(len(fields)):
        ws.write(row,i,fields[i])

    for status in statuss:
        row+=1
        ws.write(row,0,status.name)


    #Journal
    wj = wb.add_sheet("Journal")
    row=0
    fields=['date',
            'entry',
            'author',
            'task']

    for i in range(len(fields)):
        wj.write(row,i,fields[i])

    for journal in journals:
        row+=1
        wj.write(row,0,journal.date.strftime("%Y-%m-%d %H:%M"), style)
        wj.write(row,1,journal.entry)
        wj.write(row,2,journal.author.username)
        wj.write(row,3,journal.task.name)


    wb.save(response)
    return response

