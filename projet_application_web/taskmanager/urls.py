from django.urls import path
from . import views

urlpatterns = [
    path('projects', views.projects, name='projects'),
    path('project/<int:id>', views.project, name='project'),
    path('task/<int:id>', views.task, name='task'),
    path('newtask', views.newtask, name='newtask'),
    path('edittask/<int:id>', views.edittask, name='edittask'),
]