import pypyodbc

class StudentAnswer(object):
    """description of class"""
    def __init__(self):
         connectionString = 'Driver={ODBC Driver 13 for SQL Server};Server=tcp:majorproject2.database.windows.net,1433;Database=EaseCheck;Uid=easeCheck;Pwd=Passw0rd;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30';
         self.connection = pypyodbc.connect(connectionString);
         self.cursor = self.connection.cursor();
         print("Connection Established")
         return;
    def saveAnswer(self,student_id,testNo,qNo,ans,scores):
        print("here in save student")
        sql = "INSERT INTO studentAnswer(student_id,testNo,qNo,ans,scores) VALUES(?,?,?,?,?)";
        values = [student_id,testNo,qNo,ans,scores];
        self.cursor.execute(sql,values);
        self.connection.commit();
        self.connection.close();
        print("this is inserted")
        return;

    def getAnswer(self,student_id,testNo,qNo):
        sql = "SELECT ans FROM studentAnswer WHERE student_id = ? and testNo = ? and qNo = ?";
        values=[student_id,testNo,qNo]
        self.cursor.execute(sql, values);
        results = self.cursor.fetchall();
        print("here its in DAO",results)
        return results

    def updateAnswer(self,student_id,testNo,qNo,ans,scores):
        sql = "UPDATE studentAnswer SET ans = ? WHERE student_id = ? and testNo = ? and qNo = ?";
        values=[ans,student_id,testNo,qNo]
        self.cursor.execute(sql, values)
        
        self.connection.commit()
        self.connection.close()
        return;

    def getStdTestScore(self, student_id, testNo):
        sql = "SELECT SUM(scores) FROM studentAnswer WHERE student_id = ? and testNo = ?";
        values=[student_id,testNo]
        self.cursor.execute(sql, values);
        results = self.cursor.fetchall();
        print("here its in getStdTestScore DAO",results)
        
        return results

    def getStdIndiScore(self, student_id, testNo):
        sql = "SELECT qNo,scores FROM studentAnswer WHERE student_id = ? and testNo = ?";
        values=[student_id,testNo]
        self.cursor.execute(sql, values);
        results = self.cursor.fetchall();
        print("here its in getStdTestScore DAO",results)
        self.connection.commit()
        self.connection.close()
        return results

    def getStdTestAnswers(self, student_id, testNo):
        sql = "select qNo, Ans from studentanswer where student_Id = ? and testNo = ? order by qno";
        values=[student_id,testNo]
        self.cursor.execute(sql, values);
        results = self.cursor.fetchall();
        print("here its in getStdTestScore DAO",results)
        self.connection.commit()
        self.connection.close()
        return results




