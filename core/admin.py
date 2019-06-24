from django.contrib import admin

from .models import Test
from .models import Cours
from .models import Topic
from .models import Exercise_List
from .models import Exercise_Multi_Choice
from .models import Exercise_Quest_Answer
from .models import Teacher
from .models import Group
from .models import Student
from .models import Enrollments
from .models import Individual_Assignment
from .models import Group_Assignment
from .models import Student_Exercise_List

admin.site.register(Test)
admin.site.register(Cours)
admin.site.register(Topic)
admin.site.register(Exercise_List)
admin.site.register(Exercise_Multi_Choice)
admin.site.register(Exercise_Quest_Answer)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Enrollments)
admin.site.register(Individual_Assignment)
admin.site.register(Group_Assignment)
admin.site.register(Student_Exercise_List)