from django.shortcuts import render
from django.shortcuts import redirect
from .models import Teacher
from .models import Student
from .models import Exercise
from .models import Exercise_List
from .models import Exercise_Quest_Answer
from .models import Exercise_Multi_Choice
from .models import Student_Exercise_List
from django.http import HttpResponse
import time


def index(request):
    return redirect('login')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            student = Student.objects.get(email=email)
            # If user is a student
            if student.code == password:
                request.session['student_id'] = student.id
                request.session['role'] = 'student'
                return redirect('student_home')
            else:
                return render(request, 'smart-classroom/login.html', {'error' : 'email and password do not match'})
        except:
            try:
                teacher = Teacher.objects.get(email=email)
                if teacher.code == password:
                    request.session['teacher_id'] = teacher.id
                    request.session['role'] = 'teacher'
                    return redirect('teacher_home')
                else:
                    return render(request, 'smart-classroom/login.html', {'error' : 'email and password do not match'})
            except:
                return render(request, 'smart-classroom/login.html', {'error' : 'Not registered'})
    else:
        try:
            role = request.session['role']
            # If al ready logged in student
            if role == 'student':
                return redirect('student_home')
            # If already logged in teacher
            elif role == 'teacher':
                return redirect('teacher_home')
        except:
            return render(request, 'smart-classroom/login.html', {})

def logout(request):
    try:
        role = request.session['role']
        if role == 'student':
            del request.session['role']
            del request.session['student_id']
        else:
            del request.session['role']
            del request.session['teacher_id']
    except:
        return redirect('login')
    return redirect('login')

def student_home(request):
    user_id = request.session.get('student_id')
    if user_id:
        student = Student.objects.get(pk=user_id)
        group_assignments = student.group.group_assignment_set.all()
        exercises_list = [group_ass.assignment for group_ass in group_assignments]
        done_exercises_list = Student_Exercise_List.objects.filter(student__id=user_id)
        done_exercises_list_ids = [ex_list.exercise_list.id for ex_list in done_exercises_list]
        # exercises = [exercise.exercise_list.exercise_quest_answer_set.all() for exercise in exercise_list]
        return render(
            request, 
            'smart-classroom/student_home.html', 
            {
                'student': student,
                'exercises_list': exercises_list,
                'done_exercises_list': done_exercises_list,
                'done_exercises_list_ids': done_exercises_list_ids
            }
        )
    else:
        return redirect('login')

def teacher_home(request):
    user_id = request.session.get('teacher_id')
    if user_id:
        if request.method == "POST":
            return HttpResponse("exercise saved")
        teacher = Teacher.objects.get(pk=user_id)
        return render(request, 'smart-classroom/teacher_home.html', {'teacher': teacher})
    else:
        return redirect('login')

def all_teachers(request):
    teachers = Teacher.objects.all()
    context = { 'teachers_list': teachers }
    return render(request, 'smart-classroom/index.html', context)

def teacher_view(request, teacher_id):
    teacher = Teacher.objects.get(pk=teacher_id)
    context = { 'teacher': teacher}
    return render(request, 'smart-classroom/teacher_view.html', context)

def teacher_edit(request, teacher_id):
    if request.method == 'POST':
        # Get the teacher with id: teacher_id from the database
        teacher = Teacher.objects.get(pk=teacher_id)
        # update first_name if needed
        if request.POST['first_name']:
            teacher.first_name = request.POST['first_name']
        # update last_name if needed
        if request.POST['last_name']:
            teacher.last_name = request.POST['last_name']
        if request.POST['email']:
            teacher.email = request.POST['email']
        teacher.save()
        context = { 'teacher': teacher }
        return render(request, 'smart-classroom/teacher_edit.html', context)
    elif request.method == 'GET':
        teacher = Teacher.objects.get(pk=teacher_id)
        context = { 'teacher': teacher}
        return render(request, 'smart-classroom/teacher_edit.html', context)

def exercise(request, exercise_list_id):
    #I have the student id saved here
    #exercise_list <--> Group_Assignment <--> Group <--> Student
    exercise_list = Exercise_List.objects.get(pk=exercise_list_id)
    exercises_qa = Exercise_Quest_Answer.objects.filter(exercise_list__id=exercise_list_id)
    exercises_mc = Exercise_Multi_Choice.objects.filter(exercise_list__id=exercise_list_id)
    print(exercises_qa)
    context = { 
        'exercise_list': exercise_list,
        'exercises_qa': exercises_qa,
        'exercises_cm': exercises_mc
    }
    return render(request, 'smart-classroom/exercise.html', context)

def exercise_submit(request, exercise_list_id):
    student = Student.objects.get(pk=1)
    exercise_list = Exercise_List.objects.get(pk=exercise_list_id)
    student_ex_list = Student_Exercise_List(student=student, exercise_list=exercise_list,status=1)
    student_ex_list.save()
    return redirect('student_home')

def generated_assignment(request):
    if request.POST.get('__action', None) == "save":
        return redirect('teacher_home')
    ex_num = int(request.POST['num-exercise'])
    name = request.POST['name']
    topics = request.POST.getlist('topic')
    types = request.POST.getlist('type')
    coefficients = request.POST.getlist('coefficient')
    types = request.POST.getlist('difficulty')

    exercises = Exercise_Quest_Answer.objects.all()[:ex_num]
    exercises_ids = [ex.id for ex in exercises]
    print(exercises)
    print(exercises_ids)
    
    return render(
        request, 
        'smart-classroom/generated_assignment.html', 
        { 'exercises': exercises, 'ids': exercises_ids, 'name': name })