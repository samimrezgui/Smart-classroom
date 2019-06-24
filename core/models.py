from django.db import models

class Group(models.Model):
  name = models.CharField(max_length=30, null=True)
  level = models.IntegerField(
    choices=(
      (1, 'First year'),
      (2, 'Second year'),
      (3, 'Third year')),
    default=1
  )

  def __str__(self):
    return self.name

class Cours(models.Model):
  name = models.CharField(max_length=30)
  description = models.CharField(max_length=200)
  objectives = models.CharField(max_length=200)
  room = models.CharField(max_length=50)
  day = models.IntegerField(
    max_length=10,
    choices=(
      (1, 'Monday'),
      (2, 'Tuesday'),
      (3, 'Wednesday'),
      (4, 'Thursday'),
      (5, 'Friday'),
      (6, 'Saturday')
    ),
    default=1
  )
  start_time = models.DateField()
  end_time = models.DateField()

  def __str__(self):
    return self.name

class Topic(models.Model):
  course = models.ForeignKey(Cours, on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=30)

  def __str__(self):
    return self.name + ': ' + self.course.name

class Student(models.Model):
  group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  email = models.EmailField(max_length=50, default='')
  age = models.IntegerField()
  code = models.CharField(max_length=5)

  def __str__(self):
    return self.first_name + ' ' + self.last_name + ' in : ' + self.group.name  

class Teacher(models.Model):
  course = models.ForeignKey(Cours, on_delete=models.CASCADE, null=True)
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  email = models.EmailField(max_length=50)
  code = models.CharField(max_length=50)
  experience = models.IntegerField(default=0)
  specilization = models.CharField(
    max_length=10,
    choices=(
        ('math', 'Math'),
        ('physics', 'Physics'),
        ('arts', 'Arts'),
        ('cs', 'Computer Science')
    ),
    default='math'
  )

  def __str__(self):
    return self.first_name + ' ' + self.last_name + ' | ' + self.specilization

class Assignment(models.Model):
  author = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
  cours = models.ForeignKey(Cours, on_delete=models.CASCADE, null=True)
  name = models.CharField(max_length=30, null=True)
  date = models.DateField(null=True)

  def __str__(self):
      return self.name


class Test(Assignment):
  coeficient = models.FloatField(default=1)
  test_type = models.CharField(
    max_length=10,
    choices=(
        ('practice', 'Practice'),
        ('control', 'Control'),
        ('exam', 'Exam')
    ),
    default='practice'
  )
  
  def _str_(self):
    return 'Test of ' + self.author.specilization + ' created by ' + self.test.first_name + ' ' + self.test.last_name

class Exercise_List(Assignment):
  difficulty = models.IntegerField(
    choices=((1, 'easy'), (2, 'medium'), (3, 'hard')),
    default=1
  )

  def _str_(self):
    return 'List exercise of ' + self.author.specilization + ' created by ' + self.test.first_name + ' ' + self.test.last_name

class Exercise(models.Model):
  author = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
  test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True, blank=True)
  topic = models.ForeignKey(Topic, on_delete=models.SET_NULL ,null=True, blank=True)
  text = models.CharField(max_length=200)
  difficulty = models.IntegerField(
    choices=((1, 'easy'), (2, 'medium'), (3, 'hard')),
    default=1
  )

  def __str__(self):
    if self.topic:
      return self.text + ' | ' + self.topic.name
    return self.text

class Exercise_Multi_Choice(Exercise):
  exercise_list = models.ForeignKey(Exercise_List, on_delete=models.CASCADE, null=True, blank=True)
  possible_choices = models.TextField(max_length=1000)
  correct_choice = models.IntegerField()

class Exercise_Quest_Answer(Exercise):
  exercise_list = models.ForeignKey(Exercise_List, on_delete=models.CASCADE, null=True, blank=True)
  code_snippet = models.TextField(max_length=1000, null=True, blank=True)
  answer = models.CharField(max_length=200)


class Individual_Assignment(models.Model):
  student = models.ForeignKey(Student, on_delete=models.CASCADE)
  exercise = models.ForeignKey(Assignment, on_delete=models.CASCADE)

  def __str__(self):
    return self.student.first_name + ' working on ' + self.exercise.text


class Enrollments(models.Model):
  cours = models.ForeignKey(Cours, on_delete=models.CASCADE, null=True)
  group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

  def __str__(self):
    return self.group.name + ' is enrolled in: ' + self.cours.name

class Group_Assignment(models.Model):
  assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
  group = models.ForeignKey(Group, on_delete=models.CASCADE)

  def __str__(self):
    return self.group.name + ' takes an exercise/test of ' + self.assignment.cours.name

class Student_Exercise_List(models.Model):
  student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
  exercise_list = models.ForeignKey(Exercise_List, on_delete=models.CASCADE, null=True, blank=True)
  status = models.IntegerField(
    choices=((1, 'done'), (0, 'not done')),
    default=0
  )

class Student_Test_List(models.Model):
  student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
  test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True, blank=True)
  status = models.IntegerField(
    choices=((1, 'done'), (0, 'not done')),
    default=0
  )