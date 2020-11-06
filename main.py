from controller import Controller
cont=Controller()

menu=dict({"main":["1. Work with teacher","2. Work with student","3. Generation items","4. Exit"],
           "student":["1. Find student","2. Add new student","3. Delete student","4. Update student","5. Get all student subjects",
                      "6. Get all student teachers","7. Add student teacher","8. Delete student teacher","9. Work with student phone numbers",
                      "10. Work with group menu","11. Work with teachers menu","12. Open main menu"],
           "teacher":["1. Find teacher","2. Add new teacher","3. Delete teacher","4. Update teacher","5. Work with teacher email",
           "6. Get all teacher students","7. Work with subject menu","8. Work with student menu","9. Open main menu"],
           "email":["1. Add new email","2. Delete email","3. Update email","4. Open teacher menu","5. Open main menu"],
           "subject":["1. Add new subject","2. Delete subject by id","3. Update subject","4. Get all subject teachers","5. Open teacher menu","6. Open main menu"],
           "phone":["1. Add new phone number","2. Delete phone number","3. Update phone number","4. Open student menu","5. Open main menu"],
           "group":["1. Add new group","2. Delete group","3. Update group","4. Open student menu","5. Open main menu"],
           "gen":["1. Gen teacher","2. Gen student","3. Gen teacher student link","4. Subject menu","5. Group menu","6. Main menu"]})

def print_menu(item):
    print("-------------------------------------------------")
    for command in menu[item]:
        print(command)
    print("-------------------------------------------------")

def teacher_command():
    while 1:
        print_menu("teacher")
        input_line = input("Enter command:").strip()
        try:
            input_line = int(input_line)
            if input_line == 1: cont.print_teacher_by_id()
            elif input_line == 2:cont.add_new_teacher()
            elif input_line == 3:cont.delete_teacher_by_id()
            elif input_line == 4:cont.update_teacher_by_id()
            elif input_line == 5:
                teacher_email_command()
                break
            elif input_line == 6:cont.get_all_teacher_by_id_students()
            elif input_line == 7:
                subject_command()
                break
            elif input_line == 8:
                student_command()
                break
            elif input_line == 9:
                main_menu_comand()
                break
            else:print("Enter enather command")
        except:print("Please don't enter this command: %s" % input_line)

def teacher_email_command():
    while 1:
        print_menu("email")
        input_line = input("Enter command:").strip()
        try:
            input_line = int(input_line)
            if input_line == 1:cont.add_new_email_for_teacher()
            elif input_line == 2:cont.delete_email_for_teacher()
            elif input_line == 3:cont.update_email_for_teacher()
            elif input_line == 4:
                teacher_command()
                break
            elif input_line == 5:
                main_menu_comand()
                break
            elif input_line:print("Enter enather command")
        except:print("Please don't enter this command: %s" % input_line)

def subject_command():
    while 1:
        print_menu("subject")
        input_line = input("Enter command:").strip()
        try:
            input_line = int(input_line)
            if input_line == 1:cont.add_new_subject()
            elif input_line == 2:cont.delete_subject_by_id()
            elif input_line == 3:cont.update_subject()
            elif input_line == 4:cont.get_all_subject_teachers()
            elif input_line == 5:
                teacher_command()
                break
            elif input_line == 6:
                main_menu_comand()
                break
            elif input_line:print("Enter enather command")
        except:print("Please don't enter this command: %s" % input_line)

def student_command():
    while 1:
        print_menu("student")
        input_line = input("Enter command:").strip()
        try:
            input_line = int(input_line)
            if input_line == 1: cont.print_student_by_id()
            elif input_line == 2:cont.add_new_student()
            elif input_line == 3:cont.delete_student_by_id()
            elif input_line == 4:cont.update_student_by_id()
            elif input_line == 5:cont.get_all_student_by_id_subject()
            elif input_line == 6:cont.get_all_student_by_id_teacher()
            elif input_line == 7:cont.add_new_student_teacher_link()
            elif input_line == 8:cont.delete_student_teacher_link()
            elif input_line == 9:
                student_phone_command()
                break
            elif input_line == 10:
                group_command()
                break
            elif input_line == 11:
                teacher_command()
                break
            elif input_line == 12:
                main_menu_comand()
                break
            else:print("Enter enather command")
        except:print("Please don't enter this command: %s" % input_line)

def student_phone_command():
    while 1:
        print_menu("phone")
        input_line = input("Enter command:").strip()
        try:
            input_line = int(input_line)
            if input_line == 1:cont.add_new_phone_for_student()
            elif input_line == 2:cont.delete_phone_for_student()
            elif input_line == 3:cont.update_phone_for_student()
            elif input_line == 4:
                student_command()
                break
            elif input_line == 5:
                main_menu_comand()
                break
            else:print("Enter enather command")
        except:print("Please don't enter this command: %s" % input_line)

def group_command():
    while 1:
        print_menu("group")
        input_line = input("Enter command:").strip()
        try:
            input_line = int(input_line)
            if input_line == 1:cont.add_new_group()
            elif input_line == 2:cont.delete_group_by_id()
            elif input_line == 3:cont.update_group()
            elif input_line == 4:
                student_command()
                break
            elif input_line == 5:
                main_menu_comand()
                break
            else:print("Enter enather command")
        except:print("Please don't enter this command: %s" % input_line)

def generation_menu():
    while 1:
        print_menu("gen")
        input_line = input("Enteer command:").strip()
        try:
            input_line = int(input_line)
            if input_line == 1:cont.generation_teacher()
            elif input_line == 2:cont.generation_student()
            elif input_line == 3:cont.generation_links()
            elif input_line == 4:
                subject_command()
                break
            elif input_line == 5:
                group_command()
                break
            elif input_line == 6:
                main_menu_comand()
                break
            else:
                print("Enter enather command")
        except:
            print("Please don't enter this command: %s" % input_line)

def main_menu_comand():
    while 1:
        print_menu("main")
        input_line = input("Enteer command:").strip()
        try:
            input_line = int(input_line)
            if input_line == 1:
                teacher_command()
                break
            elif input_line == 2:
                student_command()
                break
            elif input_line == 3:
                generation_menu()
                break
            elif input_line == 4:
                break
            else:print("Enter enather command")
        except:print("Please don't enter this command: %s" % input_line)

if __name__=="__main__":
    main_menu_comand()