from django.shortcuts import render, redirect, get_object_or_404
from .models import Bus, Student, Attendance
from .forms import BusForm, StudentForm, AttendanceForm
from datetime import date

def bus_list(request):
    buses = Bus.objects.all()
    return render(request, 'busapp/bus_list.html', {'buses': buses})

def register_bus(request):
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bus_list')
    else:
        form = BusForm()
    return render(request, 'busapp/register_bus.html', {'form': form})

def register_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bus_list')
    else:
        form = StudentForm()
    return render(request, 'busapp/register_student.html', {'form': form})

def bus_attendance(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    students = bus.students.all()
    today = date.today()

    attendance_data = []
    for student in students:
        attendance = Attendance.objects.filter(student=student, date=today).first()
        attendance_data.append({
            'student': student,
            'present': attendance.present if attendance else None,
        })

    return render(request, 'busapp/bus_attendance.html', {
        'bus': bus,
        'attendance_data': attendance_data,
        'today': today
    })

def mark_attendance(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    students = bus.students.all()
    today = date.today()

    if request.method == 'POST':
        form = AttendanceForm(request.POST, students=students)
        if form.is_valid():
            for student in students:
                value = form.cleaned_data.get(f'student_{student.id}')
                is_present = (value == 'present')
                Attendance.objects.update_or_create(
                    student=student,
                    date=today,
                    defaults={'present': is_present}
                )
            return redirect('bus_attendance', bus_id=bus.id)
    else:
        initial = {}
        for student in students:
            attendance = Attendance.objects.filter(student=student, date=today).first()
            if attendance is not None:
                initial[f'student_{student.id}'] = 'present' if attendance.present else 'absent'
        form = AttendanceForm(students=students, initial=initial)

    return render(request, 'busapp/mark_attendance.html', {
        'bus': bus,
        'form': form,
        'today': today
    })