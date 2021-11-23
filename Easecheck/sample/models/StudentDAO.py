import pypyodbc
class StudentDAO(object):
    """description of class"""
    def __init__(self):
         connectionString = 'Driver={ODBC Driver 13 for SQL Server};Server=tcp:majorproject2.database.windows.net,1433;Database=EaseCheck;Uid=easeCheck;Pwd=Passw0rd;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30';
         self.connection = pypyodbc.connect(connectionString);
         self.cursor = self.connection.cursor();
         print("Connection Established")
         return;

    def saveStudent(self,sname,rollNo,Class,section,school,emailId,spassword):
        print("here in save student")
        sql = "INSERT INTO student(sname,rollNo,Class,section,school,emailId,spassword) VALUES(?,?,?,?,?,?,?)";
        values = [sname,rollNo,Class,section,school,emailId,spassword];
        self.cursor.execute(sql,values);
        self.connection.commit();
        self.connection.close();
        print("this is inserted")
        return;

    def getStudent(self,emailId,spassword):
        print("get student in dAO")
        sql = "SELECT * FROM student WHERE emailId = ? and spassword = ?";
        values=[emailId,spassword]
        self.cursor.execute(sql, values);
        results = self.cursor.fetchall();
        print(results)
        self.connection.close();
        return results;

    def subjectRegister(self,student_id,subId,subName):
        print("we enter the subject")
        sql="insert into registerUnder(student_id,subId,subName) values(?,?,?)";
        values = [student_id,subId,subName]
        self.cursor.execute(sql,values)
        self.connection.commit()
        self.connection.close()
        print("inserted in register Under")
        return;

    def deleteSubject(self,student_id,subId):
        print("we enter the delete subject")
        sql="delete from registerUnder where student_id = ? and subId = ?";
        values = [student_id,subId]
        self.cursor.execute(sql,values)
        self.connection.commit()
        self.connection.close()
        print("deleted from register Under")
        return;

    def deleteSubject(self,subId):
        print("we enter the delete subject")
        sql="delete from subject where subId = ?";
        values = [subId]
        self.cursor.execute(sql,values)
        sql="delete from registerUnder where subId = ?";
        values = [subId]
        self.cursor.execute(sql,values)
        self.connection.commit()
        self.connection.close()
        print("deleted from  subject")
        return;

    

    def getAllSubjects(self,student_id):
        print("here we get the subjects")
        print("inside getAll subjects")
        sql = "SELECT subName,subId FROM registerUnder WHERE student_id = ?";
        values=[student_id]
        self.cursor.execute(sql, values);
        results = self.cursor.fetchall();
        print("here its in DAO",results)
        self.connection.close();

        return results;

    def getStudentDetails(self,student_id):
        sql = "SELECT * FROM student WHERE student_id = ?";
        values=[student_id]
        self.cursor.execute(sql, values);
        results = self.cursor.fetchall();
        #self.connection.close();
        print(results)
        
        #self.connection.close()
        return results;

    def updateStudent(self,student_id,sname,rollNo,Class,section,school,emailId,spassword):
        sql = "UPDATE student SET sname = ?,rollNo = ?,Class = ?,section= ?,school = ?, emailId = ?,spassword = ? WHERE student_id = ?";
        values=[sname,rollNo,Class,section,school,emailId,spassword,student_id]
        self.cursor.execute(sql, values)
        self.connection.commit()
        self.connection.close()
    
    def getRegisterdStudents(self,subId,Class):
        sql = "SELECT sname,class FROM student,registerUnder WHERE registerUnder.student_id = student.student_id and registerUnder.subId LIKE ? and student.Class LIKE ?;";
        values=[subId,Class]
        self.cursor.execute(sql, values);
        results = self.cursor.fetchall();
        print(results)
        self.connection.close();
        return results;

    def getStudents(self,testNo):
        sql = "SELECT student_id from registerUnder INNER JOIN test ON test.subId = registerUnder.subId where test.testNo = ?"
        values=[testNo]
        self.cursor.execute(sql, values);
        results = self.cursor.fetchall();
        print(results)
        #self.connection.close();
        return results
      





