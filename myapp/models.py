from django.db import models
from datetime import datetime


# this is just the start
# we have to redesign this I just started the models class so we can redesign what needs ot be done


class User(models.Model):
    id = models.AutoField(("user_id"), primary_key=True, unique=True)
    # edited
    User_fName = models.CharField(max_length=200)
    # edited
    User_lName = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True, default="")
    # edited
    # user_positions = [('SA', 'Supervisor'), ('TA', 'Teaching Assistant'), ('IN', 'Instructor')]
    User_Pos = models.CharField(max_length=25, blank=True)
    User_Phone = models.CharField(max_length=200, blank=True)
    User_Address = models.TextField(max_length=500, blank=True)
    User_City = models.CharField(max_length=200, blank=True)
    User_LogPass = models.CharField(max_length=200, blank=True)
    User_isGrader = models.BooleanField(default=False, blank=True)
    User_SecAssigned = models.ManyToManyField(
        "Course", through="CourseToUser", related_name="users", blank=True
    )
    pw_reset_token = models.CharField(
        max_length=40, blank=True, default='')

    # need courses foreign key

    User_begin = models.DateTimeField(auto_now_add=True)
    User_Updated = models.DateTimeField(auto_now=True)


class Course(models.Model):
    # how do we get the different views for each user?
    id = models.AutoField(("course_id"), primary_key=True, unique=True)
    Course_Name = models.CharField(max_length=50)
    Course_Code = models.CharField(max_length=3)
    # Course_Instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    Course_Instructor = models.CharField(max_length=50, blank=True)
    Course_Description = models.CharField(max_length=150, blank=True)
    Course_isOnline = models.BooleanField(default=False)
    Course_Location = models.CharField(max_length=50, blank=True)
    Course_begin = models.DateTimeField(
        auto_now_add=True
    )  # Does this need to be a DateTimeField
    Course_Updated = models.DateTimeField(auto_now=True)


class Section(models.Model):
    id = models.AutoField(("section_id"), primary_key=True, unique=True)
    Sec_Name = models.CharField(max_length=200)
    Sec_Location = models.CharField(max_length=200)
    # foreign key for user, is there only one instructor per section/course?
    Sec_Instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    Sec_Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Sec_isOnline = models.BooleanField(default=False)
    Sec_begin = models.DateTimeField(auto_now_add=True)
    Sec_Updated = models.DateTimeField(auto_now=True)


# this represents many to many
# there is also an instance called ManyToMany in django
class CourseToUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
