from django.urls import path
from . import views

urlpatterns = [
    path('projects', views.projects, name='projects'),
    path('project/<int:id>', views.project, name='project'),
    path('task/<int:id>', views.task, name='task'),
    path('<int:id>/newtask', views.newtask, name='newtask'),
    path('task/<int:id>/edittask', views.edittask, name='edittask'), # Usually edit is added after task id
    path('tasks', views.tasks, name='tasks'),
    path('tasks_done', views.tasks_done, name="tasks_done"),
    path('activities', views.activities, name="activities"),
]