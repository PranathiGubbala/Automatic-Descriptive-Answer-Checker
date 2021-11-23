
import pypyodbc
class TeacherDAO(object):
    def __init__(self):
         connectionString = 'Driver={ODBC Driver 13 for SQL Server};Server=tcp:majorproject2.database.windows.net,1433;Database=EaseCheck;Uid=easeCheck;Pwd=Passw0rd;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30';
         self.connection = pypyodbc.connect(connectionString);
         self.cursor = self.connection.cursor();
         print("Connection Established")
         return;

    def saveTeacher(self,name,school,emailId,password):
        print("I am save Teacher in DAO")
        sql = "INSERT INTO teacher(name,school,emailId,password) VALUES(?,?,?,?)";
        values = [name,school,emailId,password];
        self.cursor.execute(sql,values);
        self.connection.commit();
        self.connection.close();
        print("this is inserted")
        return;


    def getTeacher(self,emailId,password):
        print("get teacher function in DAO")
        sql = "SELECT * FROM teacher WHERE emailId = ? and password = ?";
        values=[emailId,password]
        self.cursor.execute(sql, values);
        results = self.cursor.fetchall();
        print(results)
        self.connection.close();
        return results;

    def getTeacherDetails(self,teacher_id):
        print("Will get all the details from table")
        sql = "SELECT * FROM teacher WHERE id = ?";
        values=[teacher_id]
        self.cursor.execute(sql, values);
        results = self.cursor.fetchall();
        print(results)
        self.connection.close();
        return results;

    

    def updateTeacher(self,teacher_id,name,school,emailId,password):
        print("it will update in table")
        sql = "UPDATE teacher SET name = ?,school = ?, emailId = ?,password = ? WHERE id = ?";
        values=[name,school,emailId,password,teacher_id]
        self.cursor.execute(sql, values)
        self.connection.commit()
        self.connection.close()


    
