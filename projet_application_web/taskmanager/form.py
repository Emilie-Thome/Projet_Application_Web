from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('project',)

        widgets = {'name':forms.TextInput(attrs={'class':'form-control col-sm-10', 'placeholder':'Name...'}),
                   'description':forms.Textarea(attrs={'class':'form-control col-sm-10', 'placeholder':'Description...'}),
                   'assignee':forms.Select(attrs={'class':'form-control col-sm-10', 'placeholder':'---------'}),
                   'start_date':forms.DateInput(attrs={'class':'form-control col-sm-10'}),
                   'due_date':forms.DateInput(attrs={'class':'form-control col-sm-10'}),
                   'priority':forms.NumberInput(attrs={'min':1,'max': '5','class':'form-control col-sm-10'}),
                   'status':forms.Select(attrs={'class':'form-control col-sm-10', 'placeholder':'---------'})
                   }



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