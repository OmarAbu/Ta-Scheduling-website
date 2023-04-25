from django.shortcuts import render, redirect
from django.views import View

from myapp.Classes.supervisor import Supervisor
from myapp.Classes.users import Users, UserUtility
from myapp.models import User, Course, Section, CourseToUser
from myapp.Classes.courses import CourseUtility
from . import views


# Create your views here.


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(
            User_LogName=username, User_LogPass=password)
        if user:
            # used to store the username in the session, so that it can be used later
            request.session['username'] = username
            return redirect('home')
        else:
            # return status code 302
            return redirect('login')


class Home(View):
    def get(self, request):
        return render(request, 'home.html')


class AccountBase(View):
    def get(self, request):
        users = UserUtility.get_all_users()
        return render(request, 'accountbase.html', {"users": users})

    def post(self, request):
        # get value of method from within request.POST
        method = request.POST.get('method')

        # filterUser functionality
        if method == 'filterUser':
            users = Users.filterUser(request.POST.get('position'))
            #  the isinstance function checks if the result variable contains an instance of the TypeError class
            if isinstance(users, ValueError):
                return render(request, 'accountbase.html', {"message": "You didn't select a User Type"})
            return render(request, 'accountbase.html', {"users": users})

        # searchUser functionality
        elif method == "searchUser":
            user = Users.searchUser(request.POST.get('search'))
            if isinstance(user, ValueError):
                return render(request, 'accountbase.html', {"message": user})
            return render(request, 'accountbase.html', {"users": user})

        # deleteUser functionality
        elif method == "deleteUser":
            username = request.POST.get('username')
            Supervisor.deleteUser(username)
            user = UserUtility.get_all_users()
            return render(request, 'accountbase.html', {"users": user})

        # create account functionality
        else:
            result = Supervisor.create_account(request.POST.get('firstname'), request.POST.get('lastname'),
                                               request.POST.get(
                                                   'email'), request.POST.get('username'),
                                               request.POST.get('password'),
                                               request.POST.get(
                                                   'address'), request.POST.get('city'),
                                               request.POST.get('number'), request.POST.get('position'))
            if isinstance(result, ValueError):
                return render(request, 'createaccount.html',
                              {"message": result})
            users = UserUtility.get_all_users()
            return render(request, 'accountbase.html', {"users": users})


# want to return the same view but for a specific course


class EditCourse(View):

    def get(self, request, *args, **kwargs):
        c_code = kwargs['Course_Code']
        course = Course.objects.get(Course_Code=c_code)
        return render(request, 'courseedit.html', {'course': course})

    def post(self, request, *args, **kwargs):
        course_code = kwargs['Course_Code']
        actCourse = Course.objects.get(Course_Code=course_code)
        made_instructor = request.POST.get('Course_Instructor')
        if made_instructor == actCourse.Course_Instructor:
            return render(request, 'courseedit.html', {"message": "this instructor is already assigned to the course type a different name to remove the user "})

        elif actCourse.Course_Instructor is not "":
            print(Course.objects.get(Course_Code=course_code).Course_Instructor)
            Supervisor.removeInstructorFromClass(request.POST.get('Course_Instructor'), course_code)
            return redirect('courseedit', Course_Code=course_code)
        else:
            Supervisor.addInstructor(request.POST.get('Course_Instructor'), course_code)
            return redirect('home/course_base/', {course_code})


class CreateAccount(View):
    def get(self, request):
        return render(request, 'createaccount.html')

    def post(self, request):
        return render(request, 'createaccount.html')


class EditAccount(View):
    def get(self, request):
        return render(request, 'editaccount.html')


class CourseBase(View):
    def get(self, request):
        courses = CourseUtility.get_course_list()
        return render(request, 'course_base.html', {"courses": courses})

    def post(self, request):
        CourseUtility.create_course(request.POST.get('course_name'), request.POST.get('course_code'),
                                    request.POST.get('course_desc'))
        courses = CourseUtility.get_course_list()
        return render(request, 'course_base.html', {"courses": courses})


class CreateCourse(View):
    TEMPLATE = "createcourse.html"

    def get(self, request):
        return render(request, 'createcourse.html')

    def post(self, request):
        return render(request, 'createcourse.html', {"success": "course created"})


class EditPersonalInformation(View):
    def get(self, request):
        return render(request, 'personal_information.html')

    def post(self, request):
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        address = request.POST.get('address')
        position = request.POST.get('position')
        userAccount = Users.getUserByUsername(request.session['username'])

        Users.editInfo(userAccount, fname=firstname, lname=lastname,
                       email=email, phone=phone, address=address, position=position)
        return render(request, 'personal_information.html', {"success": "information updated"})
