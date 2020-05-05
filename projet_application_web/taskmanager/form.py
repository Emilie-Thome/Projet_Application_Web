from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('project',)

        widgets = {'name':forms.TextInput(attrs={'class':'form-control col-sm-8', 'placeholder':'Name...'}),
                   'description':forms.Textarea(attrs={'class':'form-control col-sm-8 h-25', 'rows':'2','style':'height:30%', 'placeholder':'Description...'}),
                   'assignee':forms.Select(attrs={'class':'form-control col-sm-8', 'placeholder':'---------'}),
                   'start_date':forms.DateInput(attrs={'class':'form-control col-sm-8', 'type':'date'}),
                   'due_date':forms.DateInput(attrs={'class':'form-control col-sm-8', 'type':'date'}),
                   'priority':forms.NumberInput(attrs={'min':1,'max':5,'class':'form-control col-sm-8'}),
                   'status':forms.Select(attrs={'class':'form-control col-sm-8', 'placeholder':'---------'})
                   }

        labels = {
            'name': 'Title :',
            'description': 'Decription :',
            'assignee': 'Assignee :',
            'start_date': 'Start date :',
            'due_date': 'Due date :',
            'priority': 'Priority :',
            'status':  'Status :',
        }
        help_texts = {
            'name': 'Some useful help text.',
        }
        error_messages = {
            'name': {
                'max_length': "This writer's name is too long.",
            },
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