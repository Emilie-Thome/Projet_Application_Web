from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    def clean(self):
        cleaned_data = super(TaskForm, self).clean()
        project = cleaned_data.get('project')
        assignee = cleaned_data.get('assignee')

        if not(assignee in list(project.members.all())) :
            raise forms.ValidationError(
                "The assignee must be a project member !"
            )

        return cleaned_data