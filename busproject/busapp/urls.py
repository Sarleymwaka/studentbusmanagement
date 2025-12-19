from django.urls import path
from . import views

urlpatterns = [
    path('', views.bus_list, name='bus_list'),
    path('buses/register/', views.register_bus, name='register_bus'),
    path('students/register/', views.register_student, name='register_student'),
    path('buses/<int:bus_id>/attendance/', views.bus_attendance, name='bus_attendance'),
    path('buses/<int:bus_id>/mark/', views.mark_attendance, name='mark_attendance'),
    path('buses/<int:bus_id>/delete/', views.delete_bus, name='delete_bus'),
    path('daily-attendance/', views.daily_attendance_overview, name='daily_attendance_overview'),
    path('daily-attendance/download/', views.download_daily_attendance, name='download_daily_attendance'),
]