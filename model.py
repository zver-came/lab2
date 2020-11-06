import psycopg2

class Model:
    def __init__(self):
        self.cursor=None
        self.connection=None
        try:
            self.connection=psycopg2.connect(user="postgres",password="postgres",host="127.0.0.1",port="5432",database="database_lab1")
            self.cursor=self.connection.cursor()
        except(Exception, psycopg2.Error) as error:print("Error connection with PostgreSQL",error)

    def __del__(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Connection closed")

    def delete_item(self, item_id, table, item_point):
        self.cursor.execute("DELETE FROM %s WHERE %s= %s" % (table, item_point, item_id))
        self.connection.commit()

    def select_items(self, table):
        self.cursor.execute("select * FROM %s" % (table))
        self.connection.commit()
        return self.cursor.fetchall()

    def select_item_by_id(self, item_id, table, item_point):
        self.cursor.execute("select * FROM %s WHERE %s= %s" % (table, item_point, item_id))
        self.connection.commit()
        return self.cursor.fetchall()

    #group
    def add_group(self,new_group):
        self.cursor.execute("INSERT INTO groups(name) VALUES ('%s') RETURNING group_id"% (new_group))
        self.connection.commit()
        return self.cursor.fetchall()[0][0]

    def update_group(self,upp_group):
        self.cursor.execute("update groups set name = '%s' where group_id=%s" % (upp_group['name'], upp_group['id']))
        self.connection.commit()

    #subject
    def add_subject(self,name):
        self.cursor.execute("INSERT INTO subjects (name) VALUES ('%s') returning subject_id "% (name))
        self.connection.commit()
        return self.cursor.fetchall()[0][0]

    def update_subject(self, id, name):
        self.cursor.execute("update subjects set name = '%s' where subject_id = %s" %(name,id))
        self.connection.commit()

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

    #student phone
    def add_student_phone(self, new_phone, item_id):
        self.cursor.execute("insert into student_phone (phone_number, student_id) values ('%s',%s)"% (new_phone,item_id))
        self.connection.commit()

    def delete_some_student_phone(self, item_id,phone):
        self.cursor.execute("delete from student_phone where student_id = %s and phone_number = '%s'" % (item_id,phone))
        self.connection.commit()

    def update_students_phones(self,student_id,old_phone,new_phone):
        self.cursor.execute("update student_phone set phone_number = '%s' where student_id = %s and phone_number = '%s'"%
                            (new_phone, student_id,old_phone))
        self.connection.commit()

    #teacher
    def add_teacher(self,new_teacher):
        self.cursor.execute("INSERT INTO teachers(name, surname, subject_id) VALUES ('%s','%s',%s) RETURNING teacher_id"
            % (new_teacher['name'], new_teacher['surname'], new_teacher['subject']))
        self.connection.commit()
        return self.cursor.fetchall()[0][0]

    def update_teacher(self,upp_teacher):
        self.cursor.execute("update teachers set name = '%s', surname = '%s', subject_id = %s where teacher_id=%s" %
            (upp_teacher['name'], upp_teacher['surname'],upp_teacher['subject'], upp_teacher['id']))
        self.connection.commit()

    #teacher email
    def add_teacher_email(self,new_email,item_id):
        self.cursor.execute("insert into teacher_email (email, teacher_id) values ('%s',%s)"% (new_email,item_id))
        self.connection.commit()

    def delete_some_teacher_email(self, item_id,email):
        self.cursor.execute("delete from teacher_email as t where t.teacher_id = %s and t.email = '%s'" % ( item_id,email))
        self.connection.commit()

    def update_teacher_email(self,teacher_id,old_email,new_email):
        self.cursor.execute("update teacher_email set email = '%s' where teacher_id = %s and email = '%s'"%(new_email, teacher_id,old_email))
        self.connection.commit()

    #teacher student link
    def get_teacher_student_link(self,teacher_id,student_id):
        self.cursor.execute("select from teacher_student where teacher_id = %s and student_id = %s"% (teacher_id, student_id))
        return self.cursor.fetchall()

    def add_teacher_student_link(self, teacher_id,student_id):
        self.cursor.execute("insert into teacher_student (teacher_id, student_id) values (%s,%s)"% (teacher_id, student_id))
        self.connection.commit()

    def delete_teacher_student_link(self, teacher_id,student_id):
        self.cursor.execute("delete from teacher_student where teacher_id = %s and student_id =%s" %(teacher_id,student_id))
        self.connection.commit()

    #some function
    def get_all_student_teachers(self,student_id,query):
        self.cursor.execute("select t.teacher_id, t.name,t.surname,t.subject_id from teachers as t, students as s, teacher_student as ts %s"
            "where s.student_id = %s and s.student_id=ts.student_id and t.teacher_id=ts.teacher_id order by t.teacher_id" % (query, student_id))
        return self.cursor.fetchall()

    def get_all_teacher_students(self,teacher_id,query):
        self.cursor.execute("select s.student_id, s.name,s.surname from teachers as t, students as s, teacher_student as ts %s "
                            "where t.teacher_id = %s and s.student_id=ts.student_id and t.teacher_id=ts.teacher_id order by s.student_id"% (query,teacher_id))
        return self.cursor.fetchall()

    def get_all_student_subjects(self,student_id,query,params):
        self.cursor.execute("select sub.subject_id, sub.name from teachers as t,subjects as sub, students as st, teacher_student as ts "
                            "%s where t.teacher_id=ts.teacher_id and st.student_id = ts.student_id and st.student_id=%s "
                            "and t.subject_id=sub.subject_id %s group by sub.subject_id order by sub.subject_id" % (query, student_id,params))
        return self.cursor.fetchall()

    def get_all_subject_teachers(self,subject_id, query):
        self.cursor.execute(
            "select t.teacher_id,t.name,t.surname from subjects as sub join teachers as t using(subject_id) %s"
            " where sub.subject_id=%s " % (query, subject_id))
        return self.cursor.fetchall()

    #gen
    def gen_teachers(self,number):
        self.cursor.execute("with info as (insert into teachers (name,surname,subject_id)"
                            "select random_str(3+(random()*7)::int), random_str(3+(random()*7)::int),random_subject_id()"
                            "from generate_series(1,%s) returning teacher_id)"
                            "insert into teacher_email (email,teacher_id)"
                            "select random_email(7), teacher_id  from info" % (number))
        self.connection.commit()

    def gen_teacher_student_link(self):
        self.cursor.execute("INSERT INTO teacher_student(student_id, teacher_id) "
                            "SELECT link.student_id, link.teacher_id FROM "
                            "(select student_id,random_teacher_id() as teacher_id from students,generate_series(1,2)) as link "
                            "left join teacher_student as ts on "
                            "link.student_id=ts.student_id AND ts.teacher_id=link.teacher_id WHERE ts.student_id IS NULL "
                            "GROUP BY (link.student_id, link.teacher_id)")
        self.connection.commit()

    def gen_students(self,number):
        self.cursor.execute("with info as (insert into students (name, surname, group_id)"
                            "select random_str(3+(random() * 7)::int), random_str(3 + (random() * 7)::int),random_group_id()"
                            "from generate_series(1, %s) returning student_id)"
                            "insert into student_phone(phone_number, student_id)"
                            "select random_phone(), student_id from info"%(number))
        self.connection.commit()

    def gen_group(self,number):
        self.cursor.execute("insert into groups (name) (select chr(trunc(65 + random() * 25)::int) || chr(trunc(65 + random() * 25)::int)"
                            "|| chr(45) ||trunc(random() * 99)::int from generate_series(1,%s))"%(number))
        self.connection.commit()

    def gen_subject(self,number):
        self.cursor.execute("insert into subjects (name) select random_str(7) from generate_series(1,%s)" % (number))
        self.connection.commit()

    def find(self,query):
        self.cursor.execute(query)
        return self.cursor.fetchall()