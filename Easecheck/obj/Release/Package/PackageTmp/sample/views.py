"""
Routes and views for the flask application.
"""

import os
import datetime
from datetime import date
#from datetime import datetime
from flask import Markup #using to flash messages onto html page 
from flask import render_template,Flask,flash,request,redirect,url_for,session
from sample import app
import MySQLdb
from flask_mysqldb import MySQL

from sample.models.TeacherDAO import TeacherDAO
from sample.models.Subject import Subject
from sample.models.TestDAO import TestDAO
from sample.models.StudentDAO import StudentDAO
from sample.models.QuestionAnswer import QuestionAnswer
from sample.models.StudentAnswer import StudentAnswer

from algo import Rake
#app=Flask(__name__)
qNo = 0
qlst = []
alst = []
n = 0
marks = 0
app.secret_key = os.urandom(24)

@app.route('/GettingStarted')
def GettingStarted():
    return render_template('GettingStarted.html')

@app.route('/')
@app.route('/home')
def home():
    return render_template(
        'Login.html',
        title='Home Page',
     
    )

#teacherLogin function.
@app.route('/teacherLogin',methods=["GET","POST"])
def teacherLogin():
    if request.method == 'POST':
         print("i am the teacher login function")
         emailId  = request.form['emailId']
         password = request.form['password']

         print(emailId)

         tdao = TeacherDAO();
         teacher = tdao.getTeacher(emailId,password)

         print(teacher)
         
         #if the teacher is there,we open the account else say invalid credentials.
         if(teacher):
             teacher_id = teacher[0][0]
             session['teacher_id'] = teacher_id
             print("I AM AFTER SESSION", teacher_id)
             name = teacher[0][1]
             session['name'] = name

             return redirect(url_for('layout'))
         else:
              return render_template('Login.html',msg1=" ' Invalid Credentials !! ' ")
    return render_template('Login.html')

#teacher Layout
@app.route('/layout',methods=["GET","POST"])
def layout():
    if 'name' in session:
            name = session.get('name')
            name = session['name']

    return render_template('SelectSubject.html',name=name)


#the teacher details are saved here
@app.route('/saveTeacher',methods=["GET","POST"])
def saveTeacher():
     print("i am save Teacher function")
     if request.method == 'POST':
         name  = request.form['name']
         school = request.form['school']
         emailId = request.form['emailId']
         password = request.form['password']
         password1 = request.form['password1']

         print(name)
         print(password)
         print(password1)

         if(password == password1):
             tdao = TeacherDAO();
             tdao.saveTeacher(name,school,emailId,password)

             return  render_template('SelectSubject.html',name = name)

         else:
            
             return render_template('teacherSignup.html',msg = " ' Check your password ! '" )

     return render_template('teacherSignup.html')



 #add the subject that a teacher is going to take.
@app.route('/addSubject',methods=["GET","POST"])
def addSubject():
    print("addSubject function")
    teacher_id = session.get('teacher_id')

    if request.method == 'POST':
        subName  = request.form['subject']
        Class = request.form['class']
        if 'teacher_id' in session:
            teacher_id = session.get('teacher_id')
            teacher_id = session['teacher_id']
            print(teacher_id)
        if 'name' in session:
            name = session.get('name')
            name = session['name']

            tdao = TeacherDAO();
            sdao = Subject();

            subId = subName[0:3] + Class + str(teacher_id)
            r = sdao.getSubName(subId)
            print("I AM HERE PROERLY")
            print(r)
            if(r != []):
                return render_template('SelectSubject.html',msg =" ' You have already registered for this subject ! ' ")
            else:
                sdao.addSubject1(subId, subName, teacher_id, 0,Class)
                return redirect(url_for('allSubjects'))
        else:
            return "teacherID session issue"
#delete subject from subject table
#delete subject
@app.route('/delSubject/<subId>',methods=["GET","POST"])
def delSubject(subId):
    sd = StudentDAO();
    sd.deleteSubject(subId)
    return redirect(url_for('allSubjects'))

#here all the subjects that a teacher is taking is displayed.
@app.route('/allSubjects',methods=["GET","POST"])
def allSubjects():
    print("all subject function")
    if 'teacher_id' in session:
            teacher_id = session.get('teacher_id')
            teacher_id = session['teacher_id']
            print(teacher_id)
    if 'name' in session:
            name = session.get('name')
            name = session['name']

            sdao = Subject();
            lst = sdao.getAllSubjects(teacher_id)
            print("here it is in allSubjects",lst)
            return render_template("AllSubjects.html",len1 = len(lst),lst=lst,name=name)

#here it redirects to the Select subject page.
@app.route('/redirectSubject',methods=["GET","POST"])
def redirectSubject():
    if 'name' in session:
            name = session.get('name')
            name = session['name']
    return render_template("SelectSubject.html",name=name)



@app.route('/printAllSubjects',methods=["GET","POST"])
def printAllSubjects(lst):
    return render_template("AllSubjects.html",lst=lst)

@app.route('/viewStudents',methods=["GET","POST"])
def viewStudents():
    if 'name' in session:
            name = session.get('name')
            name = session['name']
    return render_template("viewStudents.html",name=name)

@app.route('/getRegisteredStudent',methods=["GET","POST"])
def getRegisteredStudent():
    print("this is getRegisteredStudent")
    if request.method == 'POST':
        subject = request.form['subName']
        Clas = request.form['class']
        sdao = Subject()
        if 'teacher_id' in session:
            teacher_id = session.get('teacher_id')
            teacher_id = session['teacher_id']
            print(teacher_id)
        if 'name' in session:
            name = session.get('name')
            name = session['name']
        subId = sdao.getSubId(subject,teacher_id)
        if(subId != []):
            subId = subId[0][0]
            stdao = StudentDAO()
            lst = stdao.getRegisterdStudents(subId,Clas)
            if(lst!=[]):
                return render_template("Students.html",lst=lst,len1=len(lst),name=name)
            else:
                return render_template("Students.html",lst=lst,len1=len(lst),name=name,msg=" ' No students registered ! ' ")
        else:
                     
            return render_template("viewStudents.html",name=name,msg = " ' Subject choosen is not registered ! ' ")



#here the details regarding the test are saved.
@app.route('/testDetails',methods=["GET","POST"])
def testDetails():
    global marks
    global qNo
    qNo = 0
    pd = date.today()
    present_date = datetime.datetime.combine(pd, datetime.time(0, 0))
    now = datetime.datetime.now().time()
    present_time = now.strftime("%H:%M")
    if 'name' in session:
            name = session.get('name')
            name = session['name']
    print("I am the test function")
    print("here we get the details of test")
    testNo = '0'
    if request.method == 'POST':
         examTitle  = request.form['examTitle']
         subj  = request.form['subject']
         conductedOn  = request.form['conductedOn']
         startTime  = request.form['startTime']
         endTime  = request.form['endTime']
         noq  = 0
         marks  = 0

         print(examTitle)

         if 'teacher_id' in session:
             teacher_id = session.get('teacher_id')
             teacher_id = session['teacher_id']
             print(teacher_id)

         sdao = Subject();
         lst = sdao.getSubId(subj,teacher_id)
         subId = lst[0][0]
         print(subId)

         s1dao = Subject();
         num = sdao.updateTestNo(subId)
         print(num)
       
         testNo = str(subId) + str(num)
         session['testNo'] = testNo
         

         tsdao = TestDAO();
         date_time_obj = datetime.datetime.strptime(conductedOn, '%Y-%m-%d')
         start_time_obj = conductedOn + " " + startTime
         time = datetime.datetime.strptime(start_time_obj, '%Y-%m-%d %H:%M')
         t = time.time()
         end_time_obj = conductedOn + " " + endTime
         tym = datetime.datetime.strptime(end_time_obj, '%Y-%m-%d %H:%M')
         t1 = tym.time()
         if((date_time_obj == present_date and t >= now and t1 > t) or date_time_obj > present_date):
             tsdao.saveTestDetails(testNo,examTitle,subj,conductedOn,startTime,endTime,noq,marks,teacher_id,subId)
             return  redirect(url_for('qNa'))
         else:
             msg = "The exam cannot be conducted on past dates or check the timings of the exam."
             return render_template("TestDetails.html",msg =msg);
    return render_template("TestDetails.html",name=name)

#this is the question answer page.
@app.route('/qNa',methods=["GET","POST"])
def qNa():
    if 'name' in session:
            name = session.get('name')
            name = session['name']
    return render_template("questionAnswer.html",name=name)

#here we store the question Answer given by teacher.
@app.route('/saveQNA',methods=["GET","POST"])
def saveQNA():
    global qNo
    global marks
    print("I am the save Question answer function")
    if request.form['text'] == 'next':
        print("I am the next function")
        question  = request.form['question']
        answer  = request.form['answer']
        mark = request.form['marks']
        if 'testNo' in session:
            testNo = session.get('testNo')
            testNo = session['testNo']
            print(testNo)
        marks = marks + int(mark)
        qNo = qNo + 1
        qadao = QuestionAnswer()
        
        qadao.saveQuestionAnswer(testNo,qNo,question,answer,mark)


        return  redirect(url_for('qNa'))
     
    elif request.form['text'] == 'finish':
        print("i am the finish button")
        question  = request.form['question']
        answer  = request.form['answer']
        mark = request.form['marks']
        if 'testNo' in session:
            testNo = session.get('testNo')
            testNo = session['testNo']
            print(testNo)
        marks = marks + int(mark)
        qNo = qNo + 1

        qadao = QuestionAnswer()
        qadao.saveQuestionAnswer(testNo,qNo,question,answer,mark)
        tsdao = TestDAO();
        tsdao.updateTotalMarks(marks, testNo)

        return  redirect(url_for('viewTest'))

         

#here all the questions are displayed.
@app.route('/viewTest',methods=["GET","POST"])
def viewTest():
    print("I am the view Test function")
    if 'testNo' in session:
             testNo = session.get('testNo')
             testNo = session['testNo']
             print(testNo)
    qadao = QuestionAnswer()
    lst = qadao.getAllQuestions(testNo)
    print(lst)
    len1 = len(lst)
    if 'name' in session:
            name = session.get('name')
            name = session['name']
    return  render_template("viewTest.html",lst=lst,len1=len1,testNo=testNo,name=name)

#here we can edit the question and answer.
@app.route('/edit',methods=["GET","POST"])
def edit():
    print("I am the edit function")
    if request.method == 'POST':
        testNo = request.form['testNo']
        qNo = request.form['qNo']
        qdao = QuestionAnswer()
        if 'name' in session:
            name = session.get('name')
            name = session['name']
        if request.form['text']=='edit':
            qAlst = qdao.getQuestionAnswer(testNo,qNo)
            print(qAlst)
            question = qAlst[0][0]
            print(question)
            answer = qAlst[0][1]
            print(answer)
            marks = qAlst[0][2]
            return render_template("editQA.html",question= question, answer = answer, marks = marks,testNo = testNo,qNo=qNo,name=name)
        if request.form['text']=='delete':
            print("I am ")
            qAlst = qdao.deleteQuestionAnswer(testNo,qNo)
            qadao = QuestionAnswer()
            lst = qadao.getAllQuestions(testNo)
            print(lst)
            len1 = len(lst)
            return  render_template("viewTest.html",lst=lst,len1=len1,testNo=testNo,name=name)

@app.route('/updateQA',methods=["GET","POST"])
def updateQA():
     print("i am the update function")
     if request.method == 'POST':
        question  = request.form['question']
        answer  = request.form['answer']
        marks = request.form['marks']
        testNo = request.form['testNo']
        qNo = request.form['qNo']

        qadao = QuestionAnswer()
        qadao.updateQuestionAnswer(testNo,qNo,question,answer,marks)
        return  redirect(url_for('viewTest'))

#the teacher can view all the test
@app.route('/viewAllTest',methods=["GET","POST"])
def viewAllTest():
    if 'teacher_id' in session:
        teacher_id = session.get('teacher_id')
        teacher_id = session['teacher_id']
        print(teacher_id)
        tdao = TestDAO()
        present_date = datetime.datetime.now().date()
        present_time = datetime.datetime.now().time()
        lst = tdao.getTeacherTest(teacher_id,present_date,present_time)
        if 'name' in session:
               name = session.get('name')
               name = session['name']
        if(lst!=[]):
            lst = lst[::-1]
            testNo = lst[0][0]
           
            return render_template("TeacherTests.html",len1 = len(lst),lst=lst,testNo=testNo,name=name)
        else:
             return render_template("TeacherTests.html",len1 = len(lst),lst=lst,name=name,msg=" ' You haven't conducted any test so far .. Please go back to conduct test page for conducting a test")
@app.route('/deleteTest/<testNo>',methods=["GET","POST"])
def deleteTest(testNo):
    print("i delete the test")
    tdao = TestDAO();
    tdao.deleteQuestionAnswer(testNo)
    return redirect(url_for('viewAllTest'))

#it gets the question and answer for a particular test
@app.route('/questionAnswers/<testNo>',methods=["GET","POST"])
def questionAnswers(testNo):
    print(testNo)
    print("get the question answer")
    qdao = QuestionAnswer();
    res = qdao.finalQuestionAnswers(testNo)
    if 'name' in session:
            name = session.get('name')
            name = session['name']
    return render_template("testQuestionAnswer.html",len1= len(res),res=res,name=name)


#to update it gets all the details
@app.route('/getTeacher',methods=["GET","POST"])
def getTeacher():
    print("I get the teacher details")
    tdao = TeacherDAO()
    if 'teacher_id' in session:
        teacher_id = session.get('teacher_id')
        teacher_id = session['teacher_id']
        print(teacher_id)
        res = tdao.getTeacherDetails(teacher_id)
        name = res[0][1]
        school = res[0][2]
        emailId = res[0][3]
        password = res[0][4]
        if 'name' in session:
            name = session.get('name')
            name = session['name']
        return render_template("UpdateTeacher.html",school=school,emailId=emailId,password=password,password1=password,name=name)

#it will update it
@app.route('/updateTeacher',methods=["GET","POST"])
def updateTeacher():
    if request.method == 'POST':
        name  = request.form['name']
        school = request.form['school']
        emailId = request.form['emailId']
        password = request.form['password']
        password1 = request.form['password1']

        print(name)
        print(password)
        print(password1)

        if(password == password1):
            tdao = TeacherDAO();
            if 'teacher_id' in session:
                teacher_id = session.get('teacher_id')
                teacher_id = session['teacher_id']
                print(teacher_id)
            tdao.updateTeacher(teacher_id,name,school,emailId,password)
            return  redirect(url_for('layout'))

@app.route('/studentScore',methods=["GET","POST"])
def studentScore():
    print("Student score")
    if 'teacher_id' in session:
        teacher_id = session.get('teacher_id')
        teacher_id = session['teacher_id']
        print(teacher_id)
        tdao = TestDAO()
        present_date = datetime.datetime.now().date()
        present_time = datetime.datetime.now().time()
        lst = tdao.getTeacherTest(teacher_id,present_date,present_time)
        
        if 'name' in session:
            name = session.get('name')
            name = session['name']
        if(lst != []):
            testNo = lst[0][0]
            return render_template("testForScore.html",len1 = len(lst),lst=lst,testNo=testNo,name=name)
        else:
            message = Markup("<h1>No tests Taken</h1>")
            flash(message)
            return render_template("testForScore.html",len1 = len(lst),lst=lst,name=name)

    
@app.route('/getTotalScore/<testNo>',methods=["GET","POST"])
def getTotalScore(testNo):
        print("get total score")
        print(testNo)
        stdDao = StudentDAO()
        stdAns = StudentAnswer()
        students = stdDao.getStudents(testNo)
        print(students)
        testScores = []
        for student_id in students:
            stdName = stdDao.getStudentDetails(student_id[0])[0][1]
            testScores += [(stdName, stdAns.getStdTestScore(student_id[0], testNo)[0][0],student_id[0])]
        testScores.sort(key=takeScore,reverse=True)
        print(testScores)
        if 'name' in session:
            name = session.get('name')
            name = session['name']
        return render_template("GrandScore.html",lst = testScores,len1 = len(testScores),testNo=testNo,name=name)
 
@app.route('/getIndividualScore/<student_id>/<testNo>',methods=["GET","POST"])
def getIndividualScore(student_id,testNo):
    print("get getStudentScore function")
    stdAns = StudentAnswer()
    testScore = stdAns.getStdIndiScore(student_id, testNo)
    print(testScore)
    if 'name' in session:
            name = session.get('name')
            name = session['name']
    
    return render_template("IndividualScore.html",lst=testScore,len1=len(testScore),name=name)

 

#help teacher
@app.route('/helpTeacher',methods=["GET","POST"])
def helpTeacher():
    if 'name' in session:
            name = session.get('name')
            name = session['name']
    return render_template("helpTeacher.html",name=name)

#logout
@app.route('/logout',methods=["GET","POST"])
def logout():
      return render_template("Login.html")

#here it is the student Login
@app.route('/studentLogin',methods=["GET","POST"])
def studentLogin():
     print("student login function")
     if request.method == 'POST':
         emailId  = request.form['emailId']
         spassword = request.form['spassword']

         print(emailId)

         studao = StudentDAO();
         student = studao.getStudent(emailId,spassword)

         print(student)

         if(student):
             student_id = student[0][0]
             session['student_id'] = student_id
             name = student[0][1]
             session['name'] = name
             print("I AM AFTER SESSION", student_id)
             return redirect(url_for('studentLayout'))
         else:
             return render_template('Login.html',msg2=" ' Invalid Credentials !!! ' ")
             
     return render_template('Login.html')
#student Layout function
@app.route('/studentLayout',methods=["GET","POST"])
def studentLayout():
    if 'name' in session:
            name = session.get('name')
            name = session['name']
    return render_template('RegisterSubject.html',name=name)

#save the student details
@app.route('/saveStudent',methods=["GET","POST"])
def saveStudent():
     print("Save the details of the student")
     if request.method == 'POST':
         sname  = request.form['sname']
         rollNo  = request.form['rollNo']
         Class  = request.form['class']
         section = request.form['section']
         school = request.form['school']
         emailId = request.form['emailId']
         spassword = request.form['spassword']
         password1 = request.form['password1']

         print(sname)
         print(spassword)
         print(password1)

         if(spassword == password1):
             studao = StudentDAO();
             studao.saveStudent(sname,rollNo,Class,section,school,emailId,spassword)
             return  render_template('RegisterSubject.html')

         else:
             
             return render_template('StudentSignUp.html',msg = " ' Please Check Your Password ! ' ")

     return render_template('StudentSignUp.html')

 #here the student registers under a subject
@app.route('/subjectRegister',methods=["GET","POST"])
def subjectRegister():
     student_id = 0
     if request.method == 'POST':
         subName = ""
         subId  = request.form['subId']
         if 'student_id' in session:
            student_id = session.get('student_id')
            student_id = session['student_id']
            print(student_id)
            sdao = Subject();
            studao = StudentDAO();
            r = sdao.getSubName(subId)
            if 'name' in session:
                name = session.get('name')
                name = session['name']
          
            if(r != []):
                r = r[0][0]
                subName = r
                studao.subjectRegister(student_id,subId,subName)
         
                return redirect(url_for('allStudentSubjects'))
            else:
                
                return render_template("RegisterSubject.html",msg="' Enter the correct subject code ! '",name=name)
         else:
             return "studentID session issue"
     return render_template("RegisterSubject.html",name=name)

#delete subject
@app.route('/deleteSubject/<subId>',methods=["GET","POST"])
def deleteSubject(subId):
    if 'student_id' in session:
        student_id = session.get('student_id')
        student_id = session['student_id']
        print(student_id)
    sd = StudentDAO();
    sd.deleteSubject(student_id,subId)
    return redirect(url_for('allStudentSubjects'))





@app.route('/registerSubject',methods=["GET","POST"])
def registerSubject():
    return render_template("RegisterSubject.html")

#get the subjects of that student
@app.route('/allStudentSubjects',methods=["GET","POST"])
def allStudentSubjects():
    print("get all subjects function")
    if 'student_id' in session:
            student_id = session.get('student_id')
            student_id = session['student_id']
            print(student_id)
            sdao = StudentDAO();
            lst = sdao.getAllSubjects(student_id)
            print("here it is in allSubjects",lst)
    if 'name' in session:
            name = session.get('name')
            name = session['name']
            return render_template("AllStudentSubject.html",len1 = len(lst),lst=lst,name=name)
#take test
@app.route('/test',methods=["GET","POST"])
def test():
    if 'student_id' in session:
        student_id = session.get('student_id')
        student_id = session['student_id']
        print(student_id)
    tdao = TestDAO()
    print("this is the test function")
    present_date = datetime.datetime.now().date()
    
    #present_time = datetime.datetime.now().time()
    now = datetime.datetime.now()
    present_time = now.strftime("%H:%M")
    print(present_time)

    lst = tdao.getTestNo(student_id,present_date,present_time)
    print("Test result: ", lst)
    print("Date, time", present_date, "   :: ", present_time)
    if 'name' in session:
            name = session.get('name')
            name = session['name']
    return render_template("Tests.html",len1 = len(lst),lst=lst,name=name)

#open the respective test
@app.route('/openTest',methods=["GET","POST"])
def openTest():
    global qlst
    global alst
    global n
    n = 0
    print("entered the openTest")
    if request.method == 'POST':
        testNo  = request.form['testNo']
        print(testNo)
        qdao = QuestionAnswer()

        qlst = qdao.getQuestion(testNo)
        alst = qdao.getAnswers(testNo)
        print(qlst)
        print(alst)
        if 'name' in session:
            name = session.get('name')
            name = session['name']
        return render_template("TestPage.html",q = qlst[0][0],ques=qlst[0][1],marks=qlst[0][2],testNo = testNo,len1=len(qlst),ans="",name=name)

@app.route('/getQAPage',methods=["GET","POST"])
def getQAPage():
    global n
    global qlst
   
    if 'student_id' in session:
        student_id = session.get('student_id')
        student_id = session['student_id']
        print(student_id)
    sadao = StudentAnswer()
        
   
    text = request.form['text']
    testNo = request.form['testNo']
    n = int(text) - 1
   
    print("The text value in n: ", n)
    ans = sadao.getAnswer(student_id,testNo,n+1)
    if(ans==[]):
        ans = ""
    else:
        ans = ans[0][0]

    return render_template("TestPage.html",q = qlst[n][0],ques=qlst[n][1],marks=qlst[n][2],testNo = testNo,len1=len(qlst),ans=ans)


#here the answer is submitted.
@app.route('/submitAnswers',methods=["GET","POST"])
def submitAnswers():
    global n
    #global qlst
    print("here submit d answers")
    if request.form['text'] == 'Submit Answer':
        print("submit Answer selected")
        if 'student_id' in session:
            student_id = session.get('student_id')
            student_id = session['student_id']
            print(student_id)

        if request.method == 'POST':
            ans = request.form['ans']
            qNo = request.form['quesNo']
            testNo = request.form['testNo']
            marks = request.form['marks']

            print("The text value is post  n: ", n)
            scores = getAnswerScore(ans,n)
            print("Marks is:: ", marks)
            
            print("answeris: ", ans)
            print(type(marks))
            #print("int(marks)", (int)(marks))
            if(scores):
                temp = float(marks)
                score = (int)(temp)
            else:
                score = 0
        
            sadao = StudentAnswer()
            print("answeris: ", ans)
            res = sadao.getAnswer(student_id,testNo,qNo)

            if(res == []):
                sadao.saveAnswer(student_id,testNo,qNo,ans,score)
            else:
                sadao.updateAnswer(student_id,testNo,qNo,ans,score)
        
            n = n + 1
            print("this is extra: ",n)
            ans = checkAns(student_id,testNo,n+1)
            print("this is already there",ans)
            #res1 = sadao.getAnswer(student_id,testNo,n)
            #print(res1)
            if(n < len(qlst)):
                return render_template("TestPage.html",q = qlst[n][0],ques=qlst[n][1],marks=qlst[n][2],testNo=testNo,len1=len(qlst),ans=ans)
            else:
                n = 0
                ans = checkAns(student_id,testNo,1)
                return render_template("TestPage.html",q = qlst[n][0],ques=qlst[n][1],marks=qlst[n][2],testNo = testNo,len1=len(qlst),ans=ans)
    
    elif request.form['text'] == 'Finish Test':
        print("I am finish")
        if 'student_id' in session:
            student_id = session.get('student_id')
            student_id = session['student_id']
            print(student_id)

        if request.method == 'POST':
            ans = request.form['ans']
            qNo = request.form['quesNo']
            testNo = request.form['testNo']
            marks = request.form['marks']
            scores = getAnswerScore(ans,n)
            if(scores):
                temp = float(marks)
                score = (int)(temp)
            else:
                score = 0
        
            sadao = StudentAnswer()
            print(ans)
            res = sadao.getAnswer(student_id,testNo,qNo)
            if(res == []):
                sadao.saveAnswer(student_id,testNo,qNo,ans,score)
            else:
                sadao.updateAnswer(student_id,testNo,qNo,ans,score)
        return redirect(url_for('test'))
            
def checkAns(student_id,testNo,n):
    sadao = StudentAnswer()
    ans = ""
    res1 = sadao.getAnswer(student_id,testNo,n)
    if(res1!=[]):
        return res1[0][0]
    else:
        return ans


#we get the score here
def getAnswerScore(ans, n):
    global alst
    teacher_ans = getWords(alst[n][0]) 
    student_ans = getWords(ans)
    #teacher_ans = getWords("The rock from which soil is derived is called parent rock.")
    #student_ans = getWords("rock derived from soil is parent rock")

    #return(str(teacher_ans) + "\n" + str(student_ans))
    return (teacher_ans == student_ans)


#To get the keywords
def getWords(sentence):
    rake = Rake("SmartStoplist.txt")
    raw_Words = rake.getKeywords(sentence)
    keyWords = set()
    for word in raw_Words:
        keyWords = keyWords.union(set(word[0].split()))
    return keyWords

#here we can view all the test given by student    
@app.route('/viewAllMyTest',methods=["GET","POST"])
def viewAllMyTest():
    if 'student_id' in session:
        student_id = session.get('student_id')
        student_id = session['student_id']
        print(student_id)
    tdao = TestDAO()
    print("this is the test function")
    print("Entered ViewAllMYTests: ")
    present_date = datetime.datetime.now().date()
    present_time = datetime.datetime.now().time()
    print("After present Time: ")
    print("Present date: ", present_date)
    print("Present time: ", present_time)
    lst = tdao.getTests(student_id, present_date, present_time)
    print(lst)
    if 'name' in session:
        name = session.get('name')
        name = session['name']
    if(lst != []):
        testNo = lst[0][0]
        return render_template("StudentTests.html",len1 = len(lst),lst=lst,testNo=testNo,name=name)
    else:
        return render_template("StudentTests.html",len1 = len(lst),lst=lst,name=name,msg=" ' Did not take any test ! ' ")
 


#it gets the question and answer for a particular test
@app.route('/squestionAnswers/<testNo>',methods=["GET","POST"])
def squestionAnswers(testNo):
    print(testNo)
    print("get the question answer")
    qdao = QuestionAnswer();
    res = qdao.finalQuestionAnswers(testNo)
    if 'name' in session:
            name = session.get('name')
            name = session['name']
    return render_template("studTestQuestionAnswer.html",len1= len(res),res= res,name=name)


#gets the student detail for edit.
@app.route('/getStudent',methods=["GET","POST"])
def getStudent():
    studao = StudentDAO()
    if 'student_id' in session:
        student_id = session.get('student_id')
        student_id = session['student_id']
        print(student_id)
        res = studao.getStudentDetails(student_id)
        sname = res[0][1]
        rollNo = res[0][2]
        Class = res[0][3]
        section = res[0][4]
        school = res[0][5]
        emailId = res[0][6]
        spassword = res[0][7]
        if 'name' in session:
            name = session.get('name')
            name = session['name']
        return render_template("UpdateStudent.html",sname=sname,rollNo=rollNo,Class= Class,section = section, school=school,emailId=emailId,spassword=spassword,password1=spassword,name=name)



@app.route('/updateStudent',methods=["GET","POST"])
def updateStudent():
    print("entered the updateStudent")
    if request.method == 'POST':
        sname  = request.form['sname']
        rollNo =  request.form['rollNo']
        Class =  request.form['Class']
        section =  request.form['section']
        school = request.form['school']
        emailId = request.form['emailId']
        spassword = request.form['spassword']
        password1 = request.form['password1']

        print(sname)
        print(spassword)
        print(password1)

        if(spassword == password1):
            studao = StudentDAO();
            if 'student_id' in session:
                student_id = session.get('student_id')
                student_id = session['student_id']
                print(student_id)
                studao.updateStudent(student_id,sname,rollNo,Class,section,school,emailId,spassword)
            return  redirect(url_for('studentLayout'))

#help student
@app.route('/helpStudent',methods=["GET","POST"])
def helpStudent():
    if 'name' in session:
            name = session.get('name')
            name = session['name']
    return render_template("helpStudent.html",name=name)








    

@app.route('/classScores',methods=["GET","POST"])
def classScores():
    print("my Scores")
    if 'student_id' in session:
        student_id = session.get('student_id')
        student_id = session['student_id']
        print(student_id)
    if 'name' in session:
            name = session.get('name')
            name = session['name']
    tdao = TestDAO()
    print("this is the test function")
    present_date = datetime.datetime.now().date()
    present_time = datetime.datetime.now().time()
    lst = tdao.getTests(student_id,present_date,present_time)
    
    print(lst)
    if(lst != []):
        testNo = lst[0][0]
        return render_template("ClassTestsScore.html",len1 = len(lst),lst=lst,testNo=testNo,student_id=student_id,name=name)
    else:
        return render_template("ClassTestsScore.html",len1 = len(lst),lst=lst,student_id=student_id,name=name,msg=" ' No tests conducted ! ' ")
def takeScore(lst):
    return(lst[1])

@app.route('/getClassScore/<testNo>',methods=["GET","POST"])
def getClassScore(testNo):
    print("get total score")
    print(testNo)
    if 'name' in session:
            name = session.get('name')
            name = session['name']
    stdDao = StudentDAO()
    stdAns = StudentAnswer()
    students = stdDao.getStudents(testNo)
    print(students)
    testScores = []
    for student_id in students:
        stdName = stdDao.getStudentDetails(student_id[0])[0][1]
        testScores += [(stdName, stdAns.getStdTestScore(student_id[0], testNo)[0][0],student_id[0])]
    print(testScores)
    testScores.sort(key=takeScore)
    print(testScores)
    return render_template("ClassScore.html",lst = testScores,len1 = len(testScores),name=name)

         
@app.route('/myScores',methods=["GET","POST"])
def myScores():
    print("my Scores")
    if 'student_id' in session:
        student_id = session.get('student_id')
        student_id = session['student_id']
        print(student_id)
    tdao = TestDAO()
    print("this is the test funn")
    present_date = datetime.datetime.now().date()
    present_time = datetime.datetime.now().time()
    lst = tdao.getTests(student_id,present_date,present_time)
    print(lst)
    
    if 'name' in session:
            name = session.get('name')
            name = session['name']
    if(lst != []):
        testNo = lst[0][0]
        return render_template("StudentTestsScore.html",len1 = len(lst),lst=lst,testNo=testNo,student_id=student_id,name=name)
    else:
        return render_template("StudentTestsScore.html",len1 = len(lst),lst=lst,student_id=student_id,name=name,msg=" ' Did not take any test ! '")

@app.route('/studentIndividualScore/<testNo>/<student_id>',methods=["GET","POST"])
def studentIndividualScore(testNo,student_id):
    print("get getIndividualScore function")
    stdAns = StudentAnswer()
    testScore = stdAns.getStdIndiScore(student_id, testNo)
    print(testScore)
    if 'name' in session:
            name = session.get('name')
            name = session['name']
    
    return render_template("MyScore.html",lst=testScore,len1=len(testScore),name=name)

@app.route('/studentTestAnswers/<testNo>/<student_id>',methods=["GET","POST"])
def studentTestAnswers(testNo,student_id):
    print("get studentTestAnswers function")
    stdAns = StudentAnswer()
    std_answrs = stdAns.getStdTestAnswers(student_id, testNo)
    print(std_answrs)
    if 'name' in session:
            name = session.get('name')
            name = session['name']
    return render_template("CompareAnswers.html",lst=std_answrs,len1=len(std_answrs),name=name)
    #return render_template("StudentTestAnswers.html",lst=std_answrs,len1=len(std_answrs),name=name)

if __name__ == "main":
    x = 0
    app.run()