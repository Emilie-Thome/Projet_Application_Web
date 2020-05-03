from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('project',)

    def clean(self):
        cleaned_data = super(TaskForm, self).clean()
        project = cleaned_data.get('project')
        assignee = cleaned_data.get('assignee')

        if project :
            if not(assignee in list(project.members.all())) :
                raise forms.ValidationError(
                    "The assignee must be a project member !"
                )

        return cleaned_data