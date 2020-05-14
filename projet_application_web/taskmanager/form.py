from django import forms
from .models import Task, Journal, Project

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('project','modified',)  # The project is already known
                                # as a task is added to an existing
                                # project in the project page

        # Fields widgets are defined :
        widgets = {'name':forms.TextInput(attrs={'class':'form-control col-sm-8', 'placeholder':'Name...'}),
                   'description':forms.Textarea(attrs={'class':'form-control col-sm-8 h-25', 'rows':'2','style':'height:30%', 'placeholder':'Description...'}),
                   'assignee':forms.Select(attrs={'class':'form-control col-sm-8'}),
                   'start_date':forms.TextInput(attrs={'class':'form-control col-sm-8', 'type':'date'}),
                   'due_date':forms.TextInput(attrs={'class':'form-control col-sm-8', 'type':'date'}),
                   'priority':forms.NumberInput(attrs={'min':1,'max':5,'class':'form-control col-sm-8'}),
                   'status':forms.Select(attrs={'class':'form-control col-sm-8', 'placeholder':'---------'})
                   }

        # Fields labels are defined :
        labels = {
            'name': 'Title :',
            'description': 'Description :',
            'assignee': 'Assignee :',
            'start_date': 'Start date :',
            'due_date': 'Due date :',
            'priority': 'Priority :',
            'status':  'Status :',
        }

    # Set some validation rules :
    def clean(self):
        cleaned_data = super(TaskForm, self).clean()

        # First, Assignee must be a project member.
        # This error can only be raised in the admin page
        project = cleaned_data.get('project')
        assignee = cleaned_data.get('assignee')

        if project :
            if not(assignee in list(project.members.all())) :
                self.add_error("assignee",
                               "The assignee must be a project member !"
                               )

        # Second, Due date must be after Start date
        start_date = cleaned_data.get('start_date')
        due_date = cleaned_data.get('due_date')

        if due_date < start_date :
            self.add_error("due_date",
                           "The due date must be after the start date !"
                           )

        return cleaned_data

class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ('entry',)  # Only the entry is necessary

        # Fields widgets are defined :
        widgets = {'entry':forms.TextInput(attrs={'class':'form-control col-sm-9',
                                                  'placeholder':'Message...'}),}

        # Fields labels are defined :
        labels = {'entry': 'Write a message :',}

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields='__all__'

        # Fields widgets are defined :
        widgets = {'name':forms.TextInput(attrs={'class':'form-control col-sm-9',
                                                  'placeholder':'Title...'}),
                   'members':forms.SelectMultiple(attrs={'multiple':'multiple',
                                                 'id':'members'}),
                   }

        # Fields labels are defined :
        labels = {'name': 'Title :',
                  'members': 'Members :',
                  }
