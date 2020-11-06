import psycopg2

class Database:
    def __init__(self):
        self.cursor=None
        self.connection=None

    def connect(self):
        try:
            self.connection=psycopg2.connect(user="postgres",password="postgres",
            host="127.0.0.1",port="5432",database="database_lab1")
            self.cursor=self.connection.cursor()
        except(Exception, psycopg2.Error) as error:
            print("Error connection with PostgreSQL",error)

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Connection closed")

    def delete_item(self, item_id, table, item_point):
        try:
            self.cursor.execute("DELETE FROM %s WHERE %s= %s" % (table, item_point, item_id))
            self.connection.commit()
        except:print("%s = %s not found"%item_point,item_id)

    def select_items(self, table):
        try:
            self.cursor.execute("select * FROM %s" % (table))
            self.connection.commit()
            return self.cursor.fetchall()
        except Exception as exp:
            print(exp)

    def select_item_by_id(self, item_id, table, item_point):
        try:
            self.cursor.execute("select * FROM %s WHERE %s= %s" % (table, item_point, item_id))
            self.connection.commit()
            return self.cursor.fetchall()
        except Exception as exp:
            print(exp)

    def get_min_max_item(self, value, params, table):
        self.cursor.execute("select %s(s.%s) from %s as s" % (value, params, table))
        self.connection.commit()
        return self.cursor.fetchall()

    #group
    def add_group(self,new_group):
        self.cursor.execute("INSERT INTO groups(name,count_students) VALUES ('%s',%s) RETURNING group_id"
                            % (new_group, 0))
        self.connection.commit()
        return self.cursor.fetchall()[0][0]

    def update_group(self,upp_group):
        self.cursor.execute("update groups set name = '%s' where group_id=%s" % (upp_group['name']
                            , upp_group['id']))
        self.connection.commit()
        print("group is updated")

    def increment_count_student(self,group):
        self.cursor.execute("UPDATE groups SET name = '%s', count_students = %s WHERE group_id = %s" %
            (group[0][1],group[0][2]+1,group[0][0]))
        self.connection.commit()

    def deincrement_count_student(self,group):
        self.cursor.execute("UPDATE groups SET name = '%s', count_students = %s WHERE group_id = %s" %
            (group[0][1],group[0][2]-1,group[0][0]))
        self.connection.commit()

    #subject
    def add_subject(self,name):
        self.cursor.execute("INSERT INTO subjects (name) VALUES ('%s') returning subject_id "% (name))
        self.connection.commit()
        return self.cursor.fetchall()[0][0]

    def update_subject(self, id, name):
        self.cursor.execute("update subjects set name = '%s' where subject_id = %s" %
                            (name,id))
        self.connection.commit()
        print("Subject successfully updated")

    #student
    def add_student(self,new_student):
        self.cursor.execute("INSERT INTO students (name, surname, \"group_id\" ) VALUES ('%s','%s',%s) returning student_id "
                            % (new_student['name'], new_student['surname'],new_student['group']))
        self.connection.commit()
        return self.cursor.fetchall()[0][0]

    def update_student(self,upp_student):
        self.cursor.execute("update students set name = '%s',surname = '%s',\"group_id\"=%s where student_id = %s" %
                            (upp_student['name'], upp_student['surname'], upp_student['group'], upp_student['id']))
        self.connection.commit()
        print("Student successfully updated")


    #student phone
    def add_student_phone(self, new_phone, item_id):
        self.cursor.execute("insert into student_phone (phone_number, student_id) values ('%s',%s)"
                            % (new_phone,item_id))
        self.connection.commit()

    def delete_some_student_phone(self, item_id,phone):
        self.cursor.execute("delete from student_phone where student_id = %s and phone_number = '%s'" % (item_id,phone))
        self.connection.commit()
        print("student phone is deleted")

    def update_students_phones(self,student_id,old_phone,new_phone):
        self.cursor.execute("update student_phone set phone_number = '%s' where student_id = %s and phone_number = '%s'"%
                            (new_phone, student_id,old_phone))
        self.connection.commit()
        print("student phone is updated")

    #teacher
    def add_teacher(self,new_teacher):
        self.cursor.execute(
            "INSERT INTO teachers(name, surname, subject_id) VALUES ('%s','%s',%s) RETURNING teacher_id"
            % (new_teacher['name'], new_teacher['surname'], new_teacher['subject']))
        self.connection.commit()
        return self.cursor.fetchall()[0][0]

    def update_teacher(self,upp_teacher):
        self.cursor.execute(
            "update teachers set name = '%s', surname = '%s', subject_id = %s where teacher_id=%s" %
            (upp_teacher['name'], upp_teacher['surname'],upp_teacher['subject'], upp_teacher['id']))
        self.connection.commit()
        print("Teacher successfully updated")

    #teacher email
    def add_teacher_email(self,new_email,item_id):
        self.cursor.execute("insert into teacher_email (email, teacher_id) values ('%s',%s)"
                            % (new_email,item_id))
        self.connection.commit()

    def delete_some_teacher_email(self, item_id,email):
        self.cursor.execute("delete from teacher_email as t where t.teacher_id = %s and t.email = '%s'" % ( item_id,email))
        self.connection.commit()
        print("teacher email (%s) is deleted" % (email))

    def update_teacher_email(self,teacher_id,old_email,new_email):
        self.cursor.execute("update teacher_email set email = '%s' "
                            "where teacher_id = %s and email = '%s'"%(new_email, teacher_id,old_email))
        self.connection.commit()
        print("teacher email (%s)->(%s) is updeted"%(old_email,new_email))

    #teacher student link
    def add_teacher_student_link(self, teacher_id,student_id):
        self.cursor.execute("insert into teacher_student (teacher_id, student_id) values (%s,%s)"
                            % (teacher_id, student_id))
        self.connection.commit()

    def delete_teacher_student_link(self, item_id,teacher_id,student_id):
        self.cursor.execute("delete from teacher_student where teacher_id = %s and student_id =%s" %(teacher_id,student_id))
        self.connection.commit()

    #some function
    def get_all_student_teachers(self,student_id,params,query):
        try:
            self.cursor.execute(
                "select t.teacher_id, t.name,t.surname,t.subject_id from teachers as t, students as s, teacher_student as ts %s"
                "where s.student_id = %s and s.student_id=ts.student_id and t.teacher_id=ts.teacher_id order by %s" % (
                query, student_id, params))
            return self.cursor.fetchall()
        except Exception as s:print(s)

    def get_all_teacher_students(self,teacher_id,params,query):
        self.cursor.execute("select s.student_id, s.name,s.surname from teachers as t, students as s, teacher_student as ts %s "
                            "where t.teacher_id = %s and s.student_id=ts.student_id and t.teacher_id=ts.teacher_id order by %s"% (query,teacher_id,params))
        return self.cursor.fetchall()

    def get_all_student_subjects(self,student_id,params,query ):
        print(params)
        try:
            self.cursor.execute(
                "select sub.subject_id, sub.name from teachers as t,subjects as sub, students as st,"
                " teacher_student as ts %s"
                "where t.teacher_id=ts.teacher_id and"
                " st.student_id = ts.student_id and st.student_id=%s and t.subject_id=sub.subject_id order by %s" % (
                query, student_id, params))
            self.connection.commit()
        except Exception as s:print(s)

        return self.cursor.fetchall()

    #gen
    def gen_name_surname_subject(self,number):
        self.cursor.execute("select chr(trunc(65 + random() * 25)::int) || array_to_string(ARRAY(SELECT "
                            "chr((97 + round(random() * 25)):: integer) FROM generate_series(1,7)), '') from generate_series(1, %s)" % number)
        return self.cursor.fetchall()

    def gen_teacher_email(self,number):
        self.cursor.execute("select array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)):: integer) FROM generate_series(1,7)), '')|| "
                            "chr(64) || array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)):: integer) FROM generate_series(1,4)), '') "
                            "from generate_series(1, %s)" % number)
        return self.cursor.fetchall()

    def gen_student_phone(self,number):
        self.cursor.execute("select trunc(900000000+random() * 99999999+1)::int from generate_series(1, %s)" % number)
        return self.cursor.fetchall()

    def gen_group(self):
        try:
            self.cursor.execute("select chr(trunc(97 + random() * 25)::int) || chr(trunc(97 + random() * 25)::int)||"
                                "trunc(random() * 99)::int from generate_series(1,1)")
            return self.cursor.fetchall()
        except:print("ddd")

    def find(self,query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except:print()