import pypyodbc
class TestDAO(object):
    """description of class"""
    def __init__(self):
         connectionString = 'Driver={ODBC Driver 13 for SQL Server};Server=tcp:majorproject2.database.windows.net,1433;Database=EaseCheck;Uid=easeCheck;Pwd=Passw0rd;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30';
         self.connection = pypyodbc.connect(connectionString);
         self.cursor = self.connection.cursor();
         print("Connection Established")
         return;

    def saveTestDetails(self,testNo,examTitle,subj,conductedOn,startTime,endTime,noq,marks,teacher_id,subId):
        print("I store the details of test")
        sql = "INSERT INTO test(testNo,examTitle,subj,conductedOn,startTime,endTime,teacher_id,subId,noq,marks) VALUES(?,?,?,?,?,?,?,?,?,?)";
        print("okay")
        values = [testNo,examTitle,subj,conductedOn,startTime,endTime,teacher_id,subId,noq,marks];
        print("gng right")
        self.cursor.execute(sql,values);
        self.connection.commit();
        self.connection.close();
        print("this is inserted")
        return;

    def getTestNo(self,student_id,present_date,present_time):
        sql = "SELECT testNo,examTitle,subj,conductedOn,startTime,endTime from test INNER JOIN registerUnder ON test.subId = registerUnder.subId  where registerUnder.student_id = ? and conductedOn >= ? order by conductedOn,startTime ASC";
        values = [student_id,present_date]
        print("okay , This is in getTestNo Dao", student_id)
        self.cursor.execute(sql,values)
        results = self.cursor.fetchall();
        print("This is in getTestNo Dao" , results)
        self.connection.commit()
        self.connection.close();
        return results;

    def getTeacherTest(self,teacher_id,present_date,present_time):
        print("I send the test that are conducted by the teacher in DAO")
        sql = "SELECT testNo,examTitle,subj,conductedOn,marks from test where teacher_id = ? order by conductedOn,startTime DESC";
        values=[teacher_id]
        print("okay..")
        self.cursor.execute(sql,values)
        results = self.cursor.fetchall();
        print(results)
        self.connection.commit()
        self.connection.close();
        return results;

    def getQuestionAnswers(self,testNo):
        sql = "SELECT testNo,examTitle,subj,marks from test where testNo = ?";
        values=[teacher_id]
        print("okay..")
        self.cursor.execute(sql,values)
        results = self.cursor.fetchall();
        print(results)
        self.connection.commit()
        self.connection.close();
        return results;

    def getTests(self,student_id,present_date, present_time):
        print("get the student test")
        sql = "SELECT testNo,examTitle,subj,conductedOn,marks from test INNER JOIN registerUnder ON test.subId = registerUnder.subId where registerUnder.student_id = ? and ((test.conductedOn < ?) or (test.conductedOn = ? and test.endtime <= ?)) order by test.conductedOn DESC";
        values=[student_id,present_date, present_date, present_time]
        print("okay..")
        self.cursor.execute(sql,values)
        results = self.cursor.fetchall();
        results = list(map(list,results))
        print(results)
        self.connection.commit()
        self.connection.close();
        return results;

    def deleteQuestionAnswer(self,testNo):
        print("I will delete the question answer")
        sql = "DELETE FROM test where testNo = ?";
        values=[testNo]
        print("Delete")
        self.cursor.execute(sql,values);
        self.connection.commit()
        self.connection.close()
        return;
    def updateTotalMarks(self, marks, testNo):
        sql = "update test set marks = ? where testNo = ?";
        values=[marks, testNo]
        print("Update Total Marks of test")
        self.cursor.execute(sql,values);
        self.connection.commit()
        self.connection.close()
        return;

    
