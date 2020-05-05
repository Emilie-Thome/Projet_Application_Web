from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('project',)

        widgets = {'name':forms.TextInput(attrs={'class':'form-control col-sm-8', 'placeholder':'Name...'}),
                   'description':forms.Textarea(attrs={'class':'form-control col-sm-8 h-25', 'rows':'2','style':'height:30%', 'placeholder':'Description...'}),
                   'assignee':forms.Select(attrs={'class':'form-control col-sm-8', 'placeholder':'---------'}),
                   'start_date':forms.TextInput(attrs={'class':'form-control col-sm-8', 'type':'date'}),
                   'due_date':forms.TextInput(attrs={'class':'form-control col-sm-8', 'type':'date'}),
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


    error_css_class = "error"
    def clean(self):
        cleaned_data = super(TaskForm, self).clean()

        ''' First, Assignee must be a project member.
            This error can only be raised in the admin page '''
        project = cleaned_data.get('project')
        assignee = cleaned_data.get('assignee')

        if project :
            if not(assignee in list(project.members.all())) :
                self.add_error("assignee",
                               "The assignee must be a project member !"
                               )

        ''' Second, Due date must be after Start date '''
        start_date = cleaned_data.get('start_date')
        due_date = cleaned_data.get('due_date')

        if due_date < start_date :
            self.add_error("due_date",
                           "The due date must be after the start date !"
                           )

        return cleaned_data