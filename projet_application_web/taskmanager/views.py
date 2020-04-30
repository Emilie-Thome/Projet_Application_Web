from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from taskmanager.models import Project

@login_required(login_url='/accounts/login/')
def projects(request):
    user = request.user
    projects = Project.objects.filter(members__in = [user])
    return render(request, 'taskmanager/projects.html',{'projects': projects})
