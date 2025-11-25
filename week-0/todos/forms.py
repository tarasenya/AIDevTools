from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    """Form for creating and updating Todo items."""

    class Meta:
        model = Todo
        fields = ['title', 'description', 'due_date', 'resolved']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description (optional)'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'resolved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }