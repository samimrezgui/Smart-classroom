from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('student/home', views.student_home, name='student_home'),
    path('exercise/<int:exercise_list_id>', views.exercise, name='exercise'),
    path('exercise/<int:exercise_list_id>/submit', views.exercise_submit, name='exercise_submit'),
    path('teachers', views.all_teachers, name='all_teachers'),
    path('teacher/home', views.teacher_home, name='teacher_home'),
    path('teachers/view/<int:teacher_id>', views.teacher_view, name='teacher_detail'),
    path('teachers/edit/<int:teacher_id>', views.teacher_edit, name='teacher_detail'),
    path('generated', views.generated_assignment, name='generated_assignment')
]