import pypyodbc
class Subject(object):
    """description of class"""
    def __init__(self):
         connectionString = 'Driver={ODBC Driver 13 for SQL Server};Server=tcp:majorproject2.database.windows.net,1433;Database=EaseCheck;Uid=easeCheck;Pwd=Passw0rd;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30';
         self.connection = pypyodbc.connect(connectionString);
         self.cursor = self.connection.cursor();
         print("Connection Established")
         return;

    def addSubject1(self,subId,subName,teacher_id,noOfTest,Class):
        print("add subject function in subject Dao")
        sql="insert into subject(subId,subName,teacher_id,noOfTest,class) values(?,?,?,?,?)";
        values = [subId,subName,teacher_id,noOfTest,Class]
        self.cursor.execute(sql,values)
        self.connection.commit()
        self.connection.close()
        print("inserted")
        return;

    def getAllSubjects(self,teacher_id):
        print("here it is the getALLSubjects function in DAO")
        sql = "SELECT subName,subId,class FROM subject WHERE teacher_id = ?";
        values=[teacher_id]
        self.cursor.execute(sql, values);
        results = self.cursor.fetchall();
        print("here its in DAO",results)
        self.connection.close();
        return results;

    def getSubId(self,subject,teacher_id):
        print("here i am getSubID in DAO")
        sql = "SELECT subId FROM subject WHERE subName = ? and teacher_id = ?";
        values=[subject,teacher_id]
        self.cursor.execute(sql, values);
        results = self.cursor.fetchall();
        print("here its in DAO",results)
        
        return results;
    
    def updateTestNo(self,subId):
        print("i am the updateTestNo in DAO")
        sql = "SELECT noOfTest FROM subject WHERE subId=?";
        values=[subId]
        print("WE are going on right track")
        self.cursor.execute(sql, values);
        print("so here we reach")
        results = self.cursor.fetchall();
        a = results[0][0]
        print(a)
        a = a + 1
        b = a
        print(a)
        sql = "UPDATE subject SET noOfTest = ? WHERE subId = ?";
        values=[b,subId]
        self.cursor.execute(sql, values)
        print("here its in DAO",results)
        self.connection.commit()
        self.connection.close()
        return a

    def getSubName(self,subId):
        sql = "SELECT subName FROM subject WHERE subId = ?";
        values=[subId]
        self.cursor.execute(sql, values);
        results = self.cursor.fetchall();
        print("here its in DAO",results)
        return results
    
