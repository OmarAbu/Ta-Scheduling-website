import myapp.models
from myapp.models import User, Section, Course, CourseToUser


class User:
    user_id = None
    email = None
    Position = None
    fName = None
    lName = None
    phone = None
    address = None
    city = None
    username = None
    isgrader = False

    def __Init__(self, user_id="", email="", position="", fname="", lname="", phone="", address="",
                 city="", username="", isgrader=""):
        self.user_id = user_id
        self.email = email
        self.position = position
        self.fName = fname
        self.lName = lname
        self.phone = phone
        self.address = address
        self.city = city
        self.username = username
        self.isgrader = isgrader

    def getAccountInfo(self, username):
        if self.username == username and self.email:
            return User.objects.get(User_Name=username)
        else:
            return ""

    def get_user_id(self):
        if self.user_id == "":
            raise TypeError("ID cannot be blank")
        return self.user_id

    def editInfo(self, phone, address, city, fname, lname):
        if phone != "":
            self.phone = phone
            nPhone = User.objects.get(User_Phone=self.phone)
            nPhone.phone = phone
            nPhone.save()
        if address != "":
            self.address = address
            nAddress = User.objects.get(User_Address=self.address)
            nAddress.address = address
            nAddress.save()
        if city != "":
            self.city = city
            nCity = User.objects.get(User_City=self.city)
            nCity.city = city
            nCity.save()

        if fname != "":
            self.fName = fname
            name = User.objects.get(User_fName=self.fName)
            name.User_fName = fname
            name.save()
        if lname != "":
            self.lName = lname
            lastn = User.objects.get(User_lName=self.lName)
            lastn.User_lName = lname
            lastn.save()

    def filterUser(self, usertype):
        if usertype != "TA" or usertype != "SA" or usertype != "IN" or usertype == "":
            return TypeError(
                "wrong user type in put, SA= supervisor, TA = teaching assitant, IN = Instructor, or you put a blank  ")
        else:
            user_positions = User.objects.filter(User_Pos=usertype)
            return user_positions

    def viewCourseAssigned(self):
        course_for_user = []
        # how does this retrieve stuff from db?
        courses = CourseToUser.objects.get(user=self)
        return courses


