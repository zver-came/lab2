from view import View
from item_search import  Search
from model import Model
from time import time
database=Model()
search=Search()
view=View()

class Controller:
    def __init__(self):
        self.the_student={}
        self.the_teacher={}

    def check_item(self):
        while 1:
            id = input("Enter id:")
            if id.isnumeric():
                if int(id)>0:
                    return int(id)
            else:print("Don't enter id: %s" % id)

    def item_select_function(self, function, element,find):
        while 1:
            print("-------------------------------------------")
            print("1. find %s\n2. enter %s id\n3. exit" % (element, element))
            input_line = input("Enter command: ").strip()
            if input_line.isnumeric():
                input_line = int(input_line)
                if (input_line == 1):
                    input_line = find()
                    function(input_line)
                elif (input_line == 2):self.cheack_id(function)
                elif (input_line == 3):break
                else:print("Try again")
            else:print("Please don`t enter this %s id -> (%s)" % (element, input_line))

    def cheack_id(self,function):
        while 1:
            id = input("Enter id:").strip()
            if id.isnumeric():
                function(int(id))
                break
            else:print("Don't enter id: %s" % id)

    def cheack_human(self,item,type):
        print("Enter %s params:"%type)
        while 1:
            item['name'] = input("Name: ").strip()
            if len(item['name']) == 0: print("Name is empty")
            else:break
        while 1:
            item['surname'] = input("Surname: ").strip()
            if len(item['surname']) == 0: print("Surname is empty")
            else:return item

    # student menu
    def add_new_student(self):
        if database.select_items("groups"):
            self.the_student=self.cheack_human(self.the_student,"student")
            search.find_group()
            groups = database.find(search.create_query())
            view.print_item(groups)
            self.the_student['group'] = False
            while not self.the_student['group']:
                id = self.check_item()
                for group in groups:
                    if (group[0] == id):
                        self.the_student['group'] = id
                        break
            view.add_new_student(self.the_student)
        else:print("Please add some group before adding student")

    def find_student(self):
        search.student_params()
        start_time = time()
        students = database.find(search.create_query())
        finish_time = time() - start_time
        view.print_item(students)
        print("request execution time: %s" % finish_time,
              "\n----------------------------------------------------------------------")
        id = self.check_item()
        for student in students:
            if (student[0] == id):
                return id
        print("Student with id = (%s) is not included in the list of found students" % id)
        return 0

    def print_student(self,student_id):
        if database.select_item_by_id(student_id, "students", "student_id"):view.print_student(student_id)
        else:print("Student with id: %s not found" % student_id)

    def print_student_by_id(self):self.item_select_function(self.print_student,"student",self.find_student)

    def delete_student(self,student_id):
        if database.select_item_by_id(student_id, "students", "student_id"):view.delete_student_by_id(student_id)
        else:print("Student with id: %s not found" % student_id)

    def delete_student_by_id(self):self.item_select_function(self.delete_student,"student",self.find_student)

    def update_student(self,student_id):
        if database.select_item_by_id(student_id,"students","student_id"):
            student = database.select_item_by_id(student_id,"students","student_id")
            self.the_student['id'] = student_id
            print("Enter params:")
            while 1:
                self.the_student['name'] = input("Name: ").strip()
                if len(self.the_student['name']) == 0: self.the_student['name'] = student[0][1]
                break
            while 1:
                self.the_student['surname'] = input("Surname: ").strip()
                if len(self.the_student['surname']) == 0: self.the_student['surname'] = student[0][2]
                break
            search.find_group()
            groups = database.find(search.create_query())
            view.print_item(groups)
            self.the_student['group'] = student[0][3]
            id = input("Enter id:").strip()
            if len(id) != 0 and id.isnumeric():
                for group in groups:
                    if (group[0] == int(id)):
                        self.the_student['group'] = int(id)
                        return
            view.update_student(self.the_student)
        else:print("Student with id: %s not found" % student_id)

    def update_student_by_id(self):self.item_select_function(self.update_student,"student",self.find_student)

    def get_all_student_teacher(self,student_id):
        if database.select_item_by_id(student_id, "students", "student_id"):
            query = ""
            input_line = input("Enter y to set teacher parameters: ")
            if (input_line == 'y'):
                search.teacher_params()
                query = search.create_query()
            view.get_all_student_teacher(student_id, query)
        else:print("Student with id: %s not found" % student_id)

    def get_all_student_by_id_teacher(self):self.item_select_function(self.get_all_student_teacher, "student", self.find_student)

    def get_all_student_subject(self, student_id):
        if database.select_item_by_id(student_id, "students", "student_id"):
            query = ""
            input_line = input("Enter y to set subject parameters: ")
            if (input_line == 'y'):
                search.find_subject()
                query = search.create_query()
            view.get_all_student_subject(student_id, query)
        else:print("Student with id: %s not found" % student_id)

    def get_all_student_by_id_subject(self):self.item_select_function(self.get_all_student_subject,"student",self.find_student)

    # teacher menu1
    def add_new_teacher(self):
        self.the_teacher = self.cheack_human(self.the_teacher, "teacher")
        search.find_subject()
        subjects=database.find(search.create_query())
        view.print_item(subjects)
        self.the_teacher['subject'] = False
        while not self.the_teacher['subject']:
            id = self.check_item()
            for subject in subjects:
                if (subject[0] == id):
                    self.the_teacher['subject'] = id
                    break
        view.add_new_teacher(self.the_teacher)

    def find_teacher(self):
        search.teacher_params()
        start_time=time()
        teachers = database.find(search.create_query())
        finish_time=time()-start_time
        view.print_item(teachers)
        print("request execution time: %s"%finish_time,"\n----------------------------------------------------------------------")
        id = self.check_item()
        for teacher in teachers:
            if (teacher[0] == id):
                return id
        print("Teacher with id = (%s) is not included in the list of found teachers" % id)
        return 0

    def print_teacher(self,teacher_id):
        if database.select_item_by_id(teacher_id, "teachers", "teacher_id"):view.print_teacher(teacher_id)
        else:print("Teacher with id: %s not found" % teacher_id)

    def print_teacher_by_id(self):self.item_select_function(self.print_teacher, "teacher", self.find_teacher)

    def delete_teacher_by_id(self):self.item_select_function(view.delete_teacher_by_id,"teacher",self.find_teacher)

    def update_tracher(self, teacher_id):
        if database.select_item_by_id(teacher_id,"teachers","teacher_id"):
            teacher = database.select_item_by_id(teacher_id,"teachers","teacher_id")
            self.the_teacher['id'] = teacher_id
            print("Enter teacher params:")
            while 1:
                self.the_teacher['name'] = input("Name: ").strip()
                if len(self.the_teacher['name']) == 0: self.the_teacher['name'] = teacher[0][1]
                break
            while 1:
                self.the_teacher['surname'] = input("Surname: ").strip()
                if len(self.the_teacher['surname']) == 0: self.the_teacher['surname'] = teacher[0][2]
                break
            search.find_subject()
            subjects = database.find(search.create_query())
            view.print_item(subjects)
            self.the_teacher['subject'] = teacher[0][3]
            id = input("Enter id:").strip()
            if len(id) != 0 and id.isnumeric():
                for subject in subjects:
                    if (subject[0] == int(id)):
                        self.the_teacher['subject'] = int(id)
                        return
            view.update_tracher(self.the_teacher)
        else:print("Teacher with id: %s not found" % teacher_id)

    def update_teacher_by_id(self):self.item_select_function(self.update_tracher,"teacher",self.find_teacher)

    def get_all_teacher_students(self,teacher_id):
        if database.select_item_by_id(teacher_id,"teachers","teacher_id"):
            query=""
            input_line=input("Enter y to set student parameters: ")
            if(input_line=='y'):
                search.student_params()
                query=search.create_query()
            view.get_all_teacher_students(teacher_id,query)
        else:print("Teacher with id-> %s not found"%teacher_id)

    def get_all_subject_teachers(self):
        search.find_subject()
        view.print_item(database.find(search.create_query()))
        subject_id=self.check_item()
        if database.select_item_by_id(subject_id,"subjects","subject_id"):
            query = ""
            input_line = input("Enter y to set teacher parameters: ")
            if (input_line == 'y'):
                search.teacher_params()
                query = search.create_query()
            view.get_all_subject_teachers(subject_id, query)
        else:print("Subject with id-> %s not found"%subject_id)

    def get_all_teacher_by_id_students(self):self.item_select_function(self.get_all_teacher_students, "teacher", self.find_teacher)
    # email menu
    def add_new_email(self,teacher_id):
        if database.select_item_by_id(teacher_id,"teachers","teacher_id"):
            while 1:
                number = input("Enter new email: ")
                if len(number) != 0:
                    view.add_new_email(teacher_id,number)
                    break
                else:print("Name is empty")
        else:print("Teacher with id: %s not found" % teacher_id)

    def add_new_email_for_teacher(self):self.item_select_function(self.add_new_email, "teacher", self.find_teacher)

    def delete_email(self,teacher_id):
        if database.select_item_by_id(teacher_id,"teachers","teacher_id"):
            try:
                number = input("Enter email adress: ").strip()
                view.delete_email(teacher_id, number)
            except:print("you enter bad email")
        else:print("Teacher with id: %s not found" % teacher_id)

    def delete_email_for_teacher(self):self.item_select_function(self.delete_email, "teacher", self.find_teacher)

    def update_email(self,teacher_id):
        if database.select_item_by_id(teacher_id,"teachers","teacher_id"):
            try:
                number1 = input("Enter old email adress: ").strip()
                while len(number1) == 0:
                    print("Email is empty")
                    number1 = input("Enter old email adress: ").strip()
                number2 = input("Enter new email adress: ").strip()
                while len(number2) == 0:
                    print("Email is empty")
                    number2 = input("Enter new email adress: ").strip()
                view.update_email(teacher_id, number1, number2)
            except:print("Email %s isn`t exist"%number1)
        else:print("Teacher with id: %s not found" % teacher_id)

    def update_email_for_teacher(self): self.item_select_function(self.update_email, "teacher", self.find_teacher)

    # subject menu
    def add_new_subject(self):
        while 1:
            number = input("Enter subject name:")
            if len(number) != 0:
                view.add_new_subject(number)
                break
            else:print("Name is empty")

    def delete_subject_by_id(self):
        subject_id = self.check_item()
        if database.select_item_by_id(subject_id,"subjects","subject_id"):view.delete_subject_by_id(subject_id)
        else:print("Subject with id: %s not found" % subject_id)

    def update_subject(self):
        subject_id = self.check_item()
        if database.select_item_by_id(subject_id,"subjects","subject_id"):
            while 1:
                number = input("Enter new subject name:")
                if len(number) != 0:
                    view.update_subject(subject_id, number)
                    break
                else:
                    print("Name is empty")
        else:print("Subject with id: %s not found" % subject_id)

    # phone menu
    def add_new_phone(self,student_id):
        if database.select_item_by_id(student_id,"students","student_id"):
            while 1:
                number = input("Enter phone number: ")
                if len(number) != 0:
                    view.add_new_phone(number,student_id)
                    break
                else:print("Phone is empty")
        else:print("Student with id: %s not found" % student_id)

    def add_new_phone_for_student(self):self.item_select_function(self.add_new_phone,"student",self.find_student)

    def delete_phone(self,student_id):
        if database.select_item_by_id(student_id,"students","student_id"):
            number = input("Enter phone number: ").strip()
            try:
                number=int(number)
                view.delete_phone(student_id,number)
            except:print("Don`t enter this student phone -> %s" % number)
        else:print("Student with id: %s not found" % student_id)

    def delete_phone_for_student(self):self.item_select_function(self.delete_phone,"student",self.find_student)

    def update_phone(self,student_id):
        if database.select_item_by_id(student_id,"students","student_id"):
            try:
                number = input("Enter phone number: ").strip()
                while len(number) == 0:
                    print("phone is empty")
                    number = input("Enter phone number: ").strip()
                new_number = input("Enter new phone: ").strip()
                while len(new_number) == 0:
                    print("phone is empty")
                    new_number = input("Enter new phone: ").strip()
                view.update_phone(student_id, number, new_number)
            except:print("Phone %s isn`t exist"%number)
        else:print("Student with id: %s not found" % student_id)

    def update_phone_for_student(self):self.item_select_function(self.update_phone, "student", self.find_student)

    # group menu
    def add_new_group(self):
        while 1:
            number = input("Enter group name:")
            if len(number) != 0:
                view.add_new_group(number)
                break
            else:print("Name is empty")

    def delete_group_by_id(self):
        group_id = self.check_item()
        if database.select_item_by_id(group_id,"groups","group_id"):view.delete_group_by_id(group_id)
        else:print("Group with id-> (%s) don`t found"%group_id)

    def update_group(self):
        group_id = self.check_item()
        if database.select_item_by_id(group_id,"groups","group_id"):
            group = {};
            group['id'] = group_id
            number = input("Enter group name:").strip()
            while 1:
                if len(number) != 0:
                    group['name'] = number
                    view.update_group(group)
                    break
                else:print("Name is empty")
        else:print("Group with id-> (%s) don`t found" % group_id)

    #generation menu
    def generation_teacher(self):
        while 1:
            number = input("Enter count generation teacher:")
            if len(number) != 0 and number.isnumeric():
                view.gen_teacher(int(number))
                break
            else:print("enter another teacher count")

    def generation_student(self):
        while 1:
            number = input("Enter count generation student:")
            if len(number) != 0 and number.isnumeric():
                view.gen_student(int(number))
                break
            else:print("enter another teacher count")

    def generation_links(self): view.gen_link()

    #link menu
    def add_new_student_teacher_link(self):
        student_id = self.find_student()
        if database.select_item_by_id(student_id, "students", "student_id"):
            teacher_id = self.find_teacher()
            if database.select_item_by_id(teacher_id, "teachers", "teacher_id"):
                if (not database.get_teacher_student_link(teacher_id, student_id)): view.add_new_student_teacher_link(teacher_id, student_id)
                else:print("Link olready exist")
            else:print("Teacher with id-> (%s) not found" % teacher_id)
        else:print("Student with id-> (%s) not found"%student_id)

    def delete_student_teacher_link(self):
        student_id = self.find_student()
        if database.select_item_by_id(student_id, "students", "student_id"):
            teacher_id = self.find_teacher()
            if database.select_item_by_id(teacher_id, "teachers", "teacher_id"):
                if (database.get_teacher_student_link(teacher_id, student_id)):
                    view.delete_student_teacher_link(teacher_id,student_id)
                else:print("Link don`t exist")
            else:print("Teacher with id-> (%s) not found" % teacher_id)
        else:print("Student with id-> (%s) not found"%student_id)