from django.urls import path
from . import views

urlpatterns = [
    path('projects', views.projects, name='projects'),
    path('project/<int:id>', views.project, name='project'),
    path('task/<int:id>', views.task, name='task'),
    path('<int:id>/newtask', views.newtask, name='newtask'),
    path('task/<int:id>/edittask', views.edittask, name='edittask'), # Usually edit is added after task id

]