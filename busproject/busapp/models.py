from django.db import models
from django.utils import timezone



class Bus(models.Model):
    bus_number = models.CharField(max_length=10)
    route = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def _str_(self):
        return f"{self.bus_number} - {self.route}"

class Student(models.Model):
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=10)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='students')

    def _str_(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    present = models.BooleanField(default=True)

    def str(self):
        return f"{self.student.name} - {'Present' if self.present else 'Absent'} on {self.date}"