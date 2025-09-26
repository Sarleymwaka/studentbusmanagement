from django import forms
from .models import Bus, Student

class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['bus_number', 'route', 'capacity']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'grade', 'bus']

class AttendanceForm(forms.Form):
    def _init_(self, *args, **kwargs):
        students = kwargs.pop('students')
        super()._init_(*args, **kwargs)
        for student in students:
            self.fields[f'student_{student.id}'] = forms.ChoiceField(
                label=student.name,
                choices=[('present', 'Present'), ('absent', 'Absent')],
                widget=forms.RadioSelect
            )