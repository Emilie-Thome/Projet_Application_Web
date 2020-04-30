from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
# from taskmanager.models import ...

@login_required(login_url='/accounts/login/')
def projects(request):
    """ View projects """
    return render(request, 'taskmanager/projects.html',)


def logout_view(request):
    logout(request)
