from django import forms
from .models import Leave , Employee

class LeaveRequestForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), empty_label=None)  # Ajoutez cette ligne

    class Meta:
        model = Leave
        fields = ['employee', 'type_of_leave', 'start_date', 'end_date', 'reason', 'attachment']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].queryset = Employee.objects.all()