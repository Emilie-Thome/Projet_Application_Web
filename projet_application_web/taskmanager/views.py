import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Project, Task, Journal, Status
from .form import TaskForm, JournalForm, ProjectForm
import csv
import xlwt
import xml.etree.ElementTree as ET
import json



##
# Print the home page
#
# @param request    WSGIRequest list with all HTTP Request
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
    permission(user, project)  # Checks if the user is a member of the project

    tasks = Task.objects.filter(project=project)
    statuss = Status.objects.all()
    members = project.members.all()

    #
    infos_gantt = list(map(
        (lambda task: {"name": task.name,
                       "start": [task.start_date.year,
                                 task.start_date.month,
                                 task.start_date.day],
                       "end": [task.due_date.year,
                               task.due_date.month,
                               task.due_date.day],
                       }),
        tasks))

    infos_activity = list(map(
        lambda member: {"member": str(member),
                         "activity": list(map(
                             lambda month: sum(map(
                                 lambda journal: (journal.task in tasks
                                                  and journal.date.month == month
                                                  and journal.date.year == datetime.datetime.now().year),
                                 Journal.objects.filter(author=member))),
                             range(1, 13))),
                         },
        members))



    return render(request, 'taskmanager/project.html', {'project': project,
                                                        'tasks': tasks,
                                                        'statuss': statuss,
                                                        'members': members,
                                                        'infos_gantt': infos_gantt,
                                                        'infos_activity': infos_activity,
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
    journals = Journal.objects.filter(task=task).order_by('-date')

    permission(user, task.project)  # Checks if the user is a member of the project

    ''' New journal entry can always be posted, no specific view '''
    if request.method == 'POST':
        form = JournalForm(request.POST)
        if form.is_valid():

            task.modified = timezone.now() #On modifie l'attribut temporel modified
            task.save()

            journal = form.save(commit=False) # Do not save directly in the DB
            journal.task = task # The project is not in the form because it is already defined

            journal.author = user
            journal.date = timezone.now()
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
    permission(user, project)  # Checks if the user is a member of the project

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  # Do not save directly in the DB
            task.project = project  # The project is not in the form because it is already defined
            task.save()
            return redirect('task', id=task.id)
    else:
        form = TaskForm()
        # Set assignee choices according to the project members :
        form.fields['assignee'].choices = map((lambda member: (member.id, member)), project.members.all())
        form.fields['assignee'].choices.insert(0, ("", '---------'))  # Set a placeholder, because it is
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
    permission(user, task.project)  # Checks if the user is a member of the project

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)  # The form is filled with current infos
        if form.is_valid():
            form.save()
            return redirect('task', id=id)
    else:
        form = TaskForm(instance=task)  # The form is filled with current infos
        # Set assignee choices according to the project members :
        form.fields['assignee'].choices = map((lambda member: (member.id, member)), task.project.members.all())

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

##
# export and donwload data into a xml file
#
# @param request     WSGIRequest list with all HTTP Request
#
##
@login_required(login_url='/accounts/login/')
def download_data_xml(request):
    users = User.objects.all()
    projects = Project.objects.all()
    tasks = Task.objects.all()
    statuss = Status.objects.all()
    journals = Journal.objects.all()

    response = HttpResponse(content_type='txt/xml')
    response['Content-disposition'] = 'attachment; filename=taskmanager.xml'

    d = ET.Element('data')

    #Users
    u = ET.SubElement(d, 'Users')

    for user in users:
        us = ET.SubElement(u, 'user')
        us.set("id", user.id.__str__())
        username = ET.SubElement(us, 'username')
        username.text = user.username
        first_name = ET.SubElement(us, 'first_name')
        first_name.text = user.first_name
        last_name = ET.SubElement(us, 'last_name')
        last_name.text = user.last_name
        email = ET.SubElement(us, 'email')
        email.text = user.email

    #Projects
    p = ET.SubElement(d, 'Projects')

    for project in projects:
        pro = ET.SubElement(p, 'project')
        pro.set("id", project.id.__str__())
        name = ET.SubElement(pro,"name")
        name.text = project.name
        for member in project.members.all():
            mem = ET.SubElement(pro, 'member')
            mem.set("id", member.id.__str__())
            username = ET.SubElement(mem, 'username')
            username.text = member.username

    #Tasks
    t = ET.SubElement(d, 'Tasks')

    for task in tasks:
        ta = ET.SubElement(t,"task")
        ta.set("id", task.id.__str__())
        project = ET.SubElement(ta,"project")
        project.set("id", task.project.id.__str__())
        pname = ET.SubElement(project,"name")
        pname.text = task.project.name
        name = ET.SubElement(ta, "name")
        name.text = task.name
        description = ET.SubElement(ta,"description")
        description.text = task.description
        assignee = ET.SubElement(ta, 'assignee')
        assignee.set("id", task.assignee.id.__str__())
        username = ET.SubElement(assignee, 'username')
        username.text = task.assignee.username
        start_date = ET.SubElement(ta,"start_date")
        start_date.text = task.start_date.__str__()
        due_date = ET.SubElement(ta,"due_date")
        due_date.text = task.due_date.__str__()
        priority = ET.SubElement(ta,"priority")
        priority.text = task.priority.__str__()
        sta = ET.SubElement(ta,"status")
        sta.set("id", task.status.id.__str__())
        sname = ET.SubElement(sta, "name")
        sname.text = task.status.name

    #Status
    s = ET.SubElement(d, 'Status')

    for status in statuss:
        sta = ET.SubElement(s,"status")
        sta.set("id",status.id.__str__())
        name = ET.SubElement(sta,"name")
        name.text = status.name

    #Journal
    j = ET.SubElement(d, 'Journal')

    for journal in journals:
        jou = ET.SubElement(j,"journal")
        jou.set("id", journal.id.__str__())
        date = ET.SubElement(jou,"date")
        date.text = journal.date.__str__()
        entry = ET.SubElement(jou,"entry")
        entry.text = journal.entry
        author = ET.SubElement(jou,"author")
        author.set("id", journal.author.id.__str__())
        username = ET.SubElement(author, "username")
        username.text = journal.author.username
        task = ET.SubElement(jou,"task")
        task.set("id", journal.task.id.__str__())
        tname = ET.SubElement(task, "name")
        tname.text = journal.task.name


    tree =  ET.ElementTree(d)
    tree.write(response)

    return response


##
# export and donwload data into a json file
#
# @param request     WSGIRequest list with all HTTP Request
#
##
@login_required(login_url='/accounts/login/')
def download_data_json(request):
    users = User.objects.all()
    projects = Project.objects.all()
    tasks = Task.objects.all()
    statuss = Status.objects.all()
    journals = Journal.objects.all()

    response = HttpResponse(content_type='txt/json')
    response['Content-disposition'] = 'attachment; filename=taskmanager.json'
    data={}

    #Users
    data['Users']=[]
    for user in users:
        data['Users'].append({
            'username':user.username,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email
        })

    #Projects
    data['Projects']=[]
    for project in projects:
        data['Projects'].append({
            'name':project.name
        })
        mem=[]
        for member in project.members.all():
            mem.append(member.username)
        data['Projects'].append({
            'members':mem
        })

    #Tasks
    data['Tasks']=[]
    for task in tasks:
        data['Tasks'].append({
            'project':task.project.name,
            'name':task.name,
            'description':task.description,
            'assignee':task.assignee.username,
            'start_date':task.start_date.__str__(),
            'due_date':task.due_date.__str__(),
            'priority':task.priority.__str__(),
            'status':task.status.name
        })

    #Status
    data['Status']=[]
    for status in statuss:
        data['Status'].append({
            'name':status.name
        })

    #Journal
    data['Journal']=[]
    for journal in journals:
        data['Journal'].append({
            'date':journal.date.__str__(),
            'entry':journal.entry,
            'author':journal.author.username,
            'task':journal.task.name
        })

    json.dump(data,response)
    return response

  

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
    projects = Project.objects.filter(members=user)
    return render(request, 'taskmanager/tasks.html', {'tasks': tasks,
                                                      'projects': projects, 'user': user})

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
    projects = Project.objects.filter(members=user)
    done_only = True
    return render(request, 'taskmanager/tasks.html', {'tasks': tasks,
                                                      'projects': projects,
                                                         'user': user,
                                                      'done_only': done_only})

def activities(request):
    user = request.user
    tasks = Task.objects.filter(project__members__in=[user]).order_by('-modified')
    journals = Journal.objects.filter(task__in=tasks).order_by('-date')
    return render(request, 'taskmanager/activities.html', {'tasks': tasks,
                                                      'user': user,
                                                           'journals': journals})
  
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
            form.save_m2m()  # Have to save ManyToManyField manually because of "form.save(commit=False)"
            if not user in project.members.all():
                project.members.add(user)
            project.save()
            return redirect('project', id=project.id)
    else:
        form = ProjectForm()

    return render(request, 'taskmanager/newproject.html', {'form': form,
                                                           'user': user})

def home(request):
    return render(request, 'taskmanager/home.html', {'user': request.user})