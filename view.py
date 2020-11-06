from model import Model
from time import time
database=Model()

class View:
    def print_item(self,items):
        print("----------------------------------------------------------------------")
        for item in items:
            print(item)
        print("----------------------------------------------------------------------")

    #student menu
    def print_student(self,student_id):
        student =database.select_item_by_id(student_id,"students","student_id")[0]
        print("ID: %s\t\tFullname: %s %s\tGroup: %s"%(student[0],student[1],student[2],database.select_item_by_id(student[3],"groups","group_id")[0][1]))
        self.print_item(database.select_item_by_id(student_id,"student_phone","student_id"))

    def print_teacher(self, teacher_id):
        student = database.select_item_by_id(teacher_id, "teachers", "teacher_id")[0]
        print("ID: %s\t\tFullname: %s %s\tSubject: %s" % (
        student[0], student[1], student[2], database.select_item_by_id(student[3], "subjects", "subject_id")[0][1]))
        self.print_item(database.select_item_by_id(teacher_id, "teacher_email", "teacher_id"))

    def add_new_student(self, new_student):print("Student successfully added with id ->%s"% database.add_student(new_student))

    def delete_student_by_id(self,student):
        database.delete_item(student, "student_phone", "student_id")
        database.delete_item(student, "teacher_student", "student_id")
        database.delete_item(student,"students","student_id")
        print("Student with id = (%s) successfully deleted"%student)

    def update_student(self, upp_student):
        database.update_student(upp_student)
        print("Student with id ->%s successfully updated" % upp_student['id'])

    def get_all_student_subject(self, student_id,query):
        start_time = time()
        if len(query) != 0:subjects = database.get_all_student_subjects(student_id, "natural join (" + query + ") as l "," and  l.subject_id=sub.subject_id ")
        else:subjects = database.get_all_student_subjects(student_id, query,"")
        final_time=time() - start_time
        self.print_item(subjects)
        print("request execution time: ",final_time)

    def get_all_student_teacher(self,student_id,query):
        start_time = time()
        if len(query) != 0:teachers = database.get_all_student_teachers(student_id,  "natural join (" + query + ") as l ")
        else:teachers = database.get_all_student_teachers(student_id,query)
        final_time=time() - start_time
        self.print_item(teachers)
        print("request execution time: ",final_time)

    #teacher menu
    def add_new_teacher(self, new_teacher):print("Teacher %s successfully added " % (database.add_teacher(new_teacher)))

    def delete_teacher_by_id(self,teacher_id):
        database.delete_item(teacher_id, "teacher_email", "teacher_id")
        database.delete_item(teacher_id, "teacher_student", "teacher_id")
        database.delete_item(teacher_id, "teachers", "teacher_id")
        print("Teacher %s successfully deleted " % (teacher_id))

    def update_tracher(self, upp_teacher):
        database.update_teacher(upp_teacher)
        print("Teacher %s successfully updated " % (upp_teacher['name']))

    def get_all_teacher_students(self,teacher_id,query):
        start_time = time()
        if len(query) != 0: students = database.get_all_teacher_students(teacher_id, "natural join (" + query + ") as l ")
        else: students = database.get_all_teacher_students(teacher_id, query)
        final_time = time() - start_time
        self.print_item(students)
        print("request execution time: ", final_time)

    # teacher email menu
    def add_new_email(self,teacher_id,email):
        database.add_teacher_email(email, teacher_id)
        print("Email: %s successfully added" % email)

    def delete_email(self,teacher_id,email):
        database.delete_some_teacher_email(teacher_id, email)
        print("Email: %s successfully deleted" % email)

    def update_email(self,teacher_id,old_email, new_email):
        database.update_teacher_email(teacher_id, old_email, new_email)
        print("Email successfully updated (%s)->(%s) " % (old_email, new_email))

    # teacher subject menu
    def add_new_subject(self,number):print("Subject successfully added with id-> %s"%database.add_subject(number))

    def delete_subject_by_id(self,subject_id):
        teachers = database.select_item_by_id(subject_id,"teachers","subject_id")
        for teacher in teachers:
            database.delete_item(teacher[0],"teacher_email","teacher_id")
            database.delete_item(teacher[0],"teacher_student","teacher_id")
            database.delete_item(teacher[0],"teachers","teacher_id")
        database.delete_item(subject_id,"subjects","subject_id")
        print("Subject with id: %s successfully deleted" % subject_id)

    def update_subject(self,subject_id, new_name):
        database.update_subject(subject_id,new_name)
        print("Subject successfully updated ->(%s) " % (new_name))

    # student phone menu
    def add_new_phone(self,phone,student_id):
        database.add_student_phone(phone,student_id)
        print("Phone successfully added")

    def delete_phone(self,student_id,phone):
        database.delete_some_student_phone(student_id,phone)
        print("Phone %s successfully deleted" % phone)

    def update_phone(self,student_id,old_number,new_number):
        database.update_students_phones(student_id,old_number,new_number)
        print("Phone successfully updated (%s)->(%s) " %(old_number,new_number))

    #group menu
    def add_new_group(self,new_group):print("Group successfully added with id -> %s" % database.add_group(new_group))

    def delete_group_by_id(self,group_id):
        students = database.select_item_by_id(group_id,"students","group_id")
        for student in students:
            database.delete_item(student[0],"student_phone","student_id")
            database.delete_item(student[0],"teacher_student","student_id")
            database.delete_item(student[0],"students","student_id")
        database.delete_item(group_id,"groups","group_id")
        print("Group with id: %s successfully deleted" % group_id)

    def update_group(self,group):
        database.update_group(group)
        print("Group (%s) successfully updated"%group['name'])

    #st link
    def add_new_student_teacher_link(self,teacher_id,student_id):
        try: database.add_teacher_student_link(teacher_id, student_id)
        except: print("Teacher (%s) Student (%s) link successfully added" % teacher_id, student_id)

    def delete_student_teacher_link(self,teacher_id,student_id):
        try: database.delete_teacher_student_link(teacher_id,student_id)
        except: print("Teacher (%s) Student (%s) link successfully deleted" % teacher_id, student_id)

    #gen menu
    def gen_teacher(self,number):
        start_time = time()
        database.gen_subject(int(number / 30) + 1)
        database.gen_teachers(number)
        final_time = time() - start_time
        print("request execution time: ", final_time,"\n%s teachers successfully added" % number)

    def gen_student(self,number):
        start_time = time()
        database.gen_group(int(number / 30) + 1)
        database.gen_students(number)
        final_time = time() - start_time
        print("request execution time: ", final_time, "\n%s student successfully added" % number)

    def gen_link(self):
        start_time = time()
        database.gen_teacher_student_link()
        final_time = time() - start_time
        print("request execution time: ", final_time, "\nteacher-student links successfully added")

    def get_all_subject_teachers(self,subject_id, query):
        start_time = time()
        if len(query) != 0:teachers = database.get_all_subject_teachers(subject_id, "join ("+query+") as l using(teacher_id)")
        else:teachers = database.get_all_subject_teachers(subject_id, query)
        final_time = time() - start_time
        self.print_item(teachers)
        print("request execution time: ", final_time)
