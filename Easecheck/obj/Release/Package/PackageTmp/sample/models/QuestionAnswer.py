import pypyodbc
class QuestionAnswer(object):
    """description of class"""
    def __init__(self):
         connectionString = 'Driver={ODBC Driver 13 for SQL Server};Server=tcp:easecheckserver.database.windows.net,1433;Database=trial;Uid=sonu@easecheckserver;Pwd=p@ssw0rd;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
         self.connection = pypyodbc.connect(connectionString);
         self.cursor = self.connection.cursor();
         print("Connection Established")
         return;

    def saveQuestionAnswer(self,testNo,qNo,question,answer,marks):
         print("I save the question and answer in DAO")
         print("I am the saveQuestion in DAO")
         sql = "INSERT INTO questionAnswer(testNo,qNo,question,answer,marks) VALUES(?,?,?,?,?)";
         values = [testNo,qNo,question,answer,marks];
         self.cursor.execute(sql,values);
         self.connection.commit();
         self.connection.close();
         print("this is inserted")
         return;

    def getAllQuestions(self,testNo):
         print("I will get all the questions for u")
         sql = "SELECT qNo,question,answer,marks FROM questionAnswer WHERE testNo = ?";
         values=[testNo]
         self.cursor.execute(sql, values);
         results = self.cursor.fetchall();
         print("here its in DAO",results)
         return results

    def getQuestionAnswer(self,testNo,qNo):
         print("I will get question Answer for you to edit")
         sql = "SELECT question,answer,marks FROM questionAnswer WHERE testNo = ? and qNo = ?";
         values=[testNo,qNo]
         self.cursor.execute(sql, values);
         results = self.cursor.fetchall();
         print("here its in DAO",results)
         return results

    def updateQuestionAnswer(self,testNo,qNo,question,answer,marks):
        print("i will update the question and answer DAO")
        sql = "UPDATE questionAnswer SET question = ? ,answer = ?, marks = ? WHERE testNo = ? and qNo = ?";
        values=[question,answer,marks,testNo,qNo]
        self.cursor.execute(sql, values)
        
        self.connection.commit()
        self.connection.close()
        return

    def getQuestion(self,testNo):
        sql = "SELECT qNo,question,marks FROM questionAnswer WHERE testNo = ?";
        values=[testNo]
        self.cursor.execute(sql, values);
        results = self.cursor.fetchall();
        print("here its in DAO",results)
        return results

    def getQuestionNos(self,testNo):
        sql = "SELECT qNo WHERE testNo = ?";
        values=[testNo]
        self.cursor.execute(sql, values);
        results = self.cursor.fetchall();
        print("here its in DAO",results)
        return results

    def getAnswers(self,testNo):
        sql = "SELECT answer FROM questionAnswer WHERE testNo = ?";
        values=[testNo]
        self.cursor.execute(sql, values);
        results = self.cursor.fetchall();
        print("here its in DAO",results)
        return results

    def finalQuestionAnswers(self,testNo):
        print("Will get the final Question and Answers")
        sql = "SELECT qNo,question,answer,marks FROM questionAnswer WHERE testNo = ?";
        values=[testNo]
        self.cursor.execute(sql, values);
        results = self.cursor.fetchall();
        print("here its in DAO",results)
        return results
    
    def updateQuestionNos(self,testNo,qNo):
        print("Inside updateQuestionNos")
        ls = self.getQuestionNos(testNo)
        ls.sort()
        print("qnos list: ", ls)
        if(qNo in ls):
            ind = ls.index(qNo) + 1
            for i in ls[ind:]:
                sql = "update questionanswer set qno = ? where qno = ? and testno = ?";
                values=[(i - 1), i, testNo]
                self.cursor.execute(sql, values);
        print("outside of updateQuestionNos")
        return

    def deleteQuestionAnswer(self,testNo,qNo):
        print("I will delete the question answer")
        sql = "DELETE FROM questionAnswer where testNo = ? and qNo = ?";
        values=[testNo,qNo]
        self.cursor.execute(sql,values);
        self.connection.commit()
        print("Entered updateQuestionNos")
        #elf.updateQuestionNos(testNo,qNo + 1)
        self.connection.close()
        return;





