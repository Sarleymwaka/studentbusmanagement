from django.shortcuts import render, redirect, get_object_or_404
from .models import Bus, Student, Attendance
from .forms import BusForm, StudentForm, AttendanceForm
from datetime import date
from django.http import HttpResponse
import csv

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

def delete_bus(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    if request.method == 'POST':
        bus.delete()
        return redirect('bus_list')
    return redirect('bus_list')

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

def daily_attendance_overview(request):
    buses = Bus.objects.all()
    today = date.today()
    attendance_summary = []

    for bus in buses:
        students = bus.students.all()
        present_count = 0
        total_students = students.count()
        student_attendance = []

        for student in students:
            attendance = Attendance.objects.filter(student=student, date=today).first()
            is_present = attendance.present if attendance else False
            if is_present:
                present_count += 1
            student_attendance.append({
                'student': student,
                'present': is_present,
            })

        attendance_summary.append({
            'bus': bus,
            'students': student_attendance,
            'present_count': present_count,
            'total_students': total_students,
        })

    return render(request, 'busapp/daily_attendance_overview.html', {
        'attendance_summary': attendance_summary,
        'today': today
    })

def download_daily_attendance(request):
    today = date.today()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="daily_attendance_{today}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Bus Number', 'Route', 'Student Name', 'Grade', 'Present'])

    buses = Bus.objects.all()
    for bus in buses:
        for student in bus.students.all():
            attendance = Attendance.objects.filter(student=student, date=today).first()
            present = 'Yes' if (attendance and attendance.present) else 'No'
            writer.writerow([bus.bus_number, bus.route, student.name, student.grade, present])

    return response