from flask import Flask, render_template,request, url_for, flash, jsonify, session
from werkzeug.utils import redirect
import pyodbc
import uuid
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'My secret Key'
notification_list = []
flag = 0
#------------------DB connection-----------------------------

# Function to establish connection to SQL Server
def connect_to_database():
    return pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-UNVMP3TE\\SQLEXPRESS01;DATABASE=EmployeePortal;')

#---------------- end Db connection-----------------------------

#----------------------- Login Functionalities ----------------------------

#funtion to register
@app.route('/register', methods = ['GET','POST'])
def registerPage():
    if request.method == "POST":
        EmpAccID = uuid.uuid4()
        empEmail = request.form.get("Usremail")
        empName = request.form.get("EmpName")
        empUsername = request.form.get("UsrName")
        empPassword = request.form.get("Usrpwd")
        role = 2
        sqlcon = connect_to_database()
        cursor = sqlcon.cursor()
        sqlQuery = """
        INSERT into EmpAccounts (EmpAccID,EmpEmail,EmpPassword,EmpName,EmpUsername,IsAdmin) values(?,?,?,?,?,?)
        """
        cursor.execute(sqlQuery,(EmpAccID,empEmail,empPassword,empName,empUsername,role))
        flash("Registered  successfully")
        sqlcon.commit()
        sqlcon.close()
        return redirect(url_for("loginPage"))
    return render_template('Login/Register.html')

@app.route('/registerAdmin', methods = ['GET','POST'])
def registerAdminPage():
    if request.method == "POST":
        EmpAccID = uuid.uuid4()
        empEmail = request.form.get("Usremail")
        empName = request.form.get("EmpName")
        empUsername = request.form.get("UsrName")
        empPassword = request.form.get("Usrpwd")
        role = request.form.get("userType")
        sqlcon = connect_to_database()
        cursor = sqlcon.cursor()
        sqlQuery = """
        INSERT into EmpAccounts (EmpAccID,EmpEmail,EmpPassword,EmpName,EmpUsername,IsAdmin) values(?,?,?,?,?,?)
        """
        cursor.execute(sqlQuery,(EmpAccID,empEmail,empPassword,empName,empUsername,role))
        flash("Registered  successfully")
        sqlcon.commit()
        sqlcon.close()
        return redirect(url_for("Index"))
    return render_template('Login/RegisterAdmin.html')
        

#Function to Login

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    if request.method == "POST":
        EmpEmail = request.form.get("usrEmail")
        EmpPass = request.form.get("UsrPwd")
        sqlcon = connect_to_database()
        cursor = sqlcon.cursor()
        session['flag'] = 0;
        sqlQuery = """ 
        SELECT * from EmpAccounts where EmpEmail = ?
        """
        result = cursor.execute(sqlQuery,(EmpEmail))
        if result:
            data = cursor.fetchone()
            password = data[2]
            isAdmin = data[5]
            if password == EmpPass:
                session['username'] = data[3]
                flash("Login successful!","success")
                if isAdmin == 1:
                    return redirect(url_for('Index'))
                elif isAdmin == 2:
                    return redirect(url_for('clientIndex'))
                else:
                    return redirect(url_for('userIndex'))
            else:
                flash("Invalid credentials")
        else:
            flash("No Employee found with that details")
        sqlcon.close()
    return render_template('Login/login1.html')

@app.route('/Logout',methods = ['GET'])
def logout():
    session['username'] = " "
    return redirect(url_for('Home'))

#-------------------------- End login functionalities--------------------------------------


@app.route('/')
def Home():
    return render_template('home/index.html')  #Login.html

@app.route('/Index')
def clientIndex():
    username = session['username']
    return redirect(url_for('clientProfile'))

@app.route('/Adminindex')
def Index():
    username = session['username']
    clients = count("assignee")
    trainers = count("Employees")
    return render_template('Admin/AdminIndex.html',username = username,Clients = clients,Trainers = trainers)

def count(tablename):
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    sql_Query = f"Select Count(*) from {tablename}"
    cursor.execute(sql_Query)
    result = cursor.fetchone()[0]
    return result

#-------------------------- Trainer portal ------------------------------------------
#Function to get userIndex
@app.route('/userIndex')
def userIndex():
    notifications = retriveNotifications()
    username = session['username']
    return render_template('userIndex.html',notifications = notifications,username = username)


#Funtion to grt Shiftrequest page
@app.route('/getShifts')
def getShiftRequest():
    username = session['username']
    return render_template('Shiftrequest.html',username = username)

#Function to post requests
@app.route('/sendRequest', methods=['POST'])
def postRequest():
    if request.method == "POST":
        shiftID = str(uuid.uuid4())
        empName = session['username']
        month = request.form.get("month")
        shift = request.form.get("shift")
        reason = request.form.get("reason")
        status = 2
        
        sqlcon = connect_to_database()
        cursor = sqlcon.cursor()
        Query1 = """
        Select ea.EmpEmail from Employees e
        join EmpAccounts ea on e.EmpAccID = ea.EmpAccID
        where e.EmpName = ?
        """
        res = cursor.execute(Query1,(empName))
        empEmail = res.fetchone()[0]
        Query2 = "SELECT EmpAccID FROM EmpAccounts WHERE EmpEmail = ?"
        cursor.execute(Query2, (empEmail))
        result = cursor.fetchone()
        session['notification'] = []
        session['flag'] = 1 #-------------------------------------------------->#needs to check
        
        if result:
            empID = result.EmpAccID
            Query2 = """
            INSERT INTO ShiftRequest (ShiftID, EmpID, EmpName, EmpEmail, Shift, ForMonth, Reason,Action) 
            VALUES (?, ?, ?, ?, ?, ?, ?,?)
            """
            cursor.execute(Query2, (shiftID, empID, empName, empEmail, shift, month, reason,status))
            sqlcon.commit()
        
            sqlcon.close()
            session['notification'].append('Test1')
            return redirect(url_for('userIndex'))
        return render_template("ShiftRequest.html")
    
    return render_template("ShiftRequest.html")

#Function to fetch shift requests
@app.route('/getRequests')
def getRequests():
    username = session['username']
    slqCon = connect_to_database()
    cursor = slqCon.cursor()
    sqlQUERY2 = """
    SELECT * From EmpAccounts where EmpName = ?
    """
    res = cursor.execute(sqlQUERY2,username)
    emp = cursor.fetchone()
    isAdmin = emp[5]
    sqlQuery1 ="""
        SELECT * From Shiftrequest
        """
    cursor.execute(sqlQuery1)
    data = cursor.fetchall()
    if isAdmin == 1:
        return render_template('Admin/ShiftRequests.html',data = data,username = username)
    else:
        sqlQuery3 = """
        SELECT * From ShiftRequest 
        where EmpName = ?
        """
        cursor.execute(sqlQuery3,(username))
        res = cursor.fetchall()
        print(res)
        return render_template('ShiftsRequestIndex.html',data = res,username = username)

#Funtion to post Timesheet 
@app.route('/gettimesheet', methods = ['POST','GET'])
def postTimesheet():
    if request.method == "POST":
        timeID = uuid.uuid4()
        FilledTime = request.form.get("hours") + ':' + request.form.get("minutes")
        date = datetime.now().strftime('%Y-%m-%d')
        status = 0
        sqlcon = connect_to_database()
        cursor = sqlcon.cursor()
        empname = session['username']
        session['notification'] = []
        
        sqlQuery1 = """
        SELECT * from Employees where EmpName = ?
        """
        result = cursor.execute(sqlQuery1,empname)
        employee = result.fetchone()
        
        if employee:
            empid = employee[0]
            empname = employee[1]
            empemail = "exyz@gmail.com"
            
            print(timeID,empid,empname,empemail,FilledTime,date,status)
            sqlQuery2 = """
            INSERT INTO Timesheet (ID,EmpID,EmpName,EmpEmail,FilledTimeSheet,Date,Status) values (?,?,?,?,?,?,?)
            """
            cursor.execute(sqlQuery2,(timeID,empid,empname,empemail,FilledTime,date,status))
            sqlcon.commit()
            flash("Data Inserted")
            message = "TEST1"
            addNotification(message)
            session['flag'] = 1
            sqlcon.close()
            return redirect(url_for('getTimesheet'))
        flash("Error fetching data")
        
    return render_template('Timesheet.html')


#Function to Delete timesheet 
@app.route('/Delete/<string:id>',methods = ['GET'])
def deleteTimesheet(id):
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    sqlQuery = """
    DELETE from Timesheet where ID = ?
    """
    cursor.execute(sqlQuery,(id))
    sqlcon.commit()
    sqlcon.close()
    return redirect(url_for('getTimesheet'))

#Funtion to get Leave reqyest page Page
@app.route('/leave')
def getLeaveRequest():
    sqlCon = connect_to_database()
    cursor = sqlCon.cursor()
    username = session['username']
    
    sqlQuery2 = """
    SELECT * from EMpAccounts where EmpName = ?
    """
    
    res = cursor.execute(sqlQuery2,username)
    emp = cursor.fetchone()
    isAdmin = emp[5]
    sqlQuery = """
    SELECT * from Leaves
    """
    cursor.execute(sqlQuery)
    data = cursor.fetchall()
    if isAdmin == 1:
        return render_template('AdminLeaves.html',data = data)
    else:
        sqlQuery3 = """
        SELECT * From Leaves where EmpName = ?
        """
        cursor.execute(sqlQuery3,(username))
        res = cursor.fetchall()
        return render_template('ApplyLeave.html',data = res,username = username)

#Function to post the leave data
@app.route('/postLeave', methods = ['POST'])
def postLeaves():
    if request.method == "POST":
        leaveID = uuid.uuid4()
        fromdate = request.form.get("fromdate")
        todate = request.form.get("todate")
        status = 0
        sqlcon = connect_to_database()
        cursor = sqlcon.cursor()
        empname = session['username'] 
        sqlQuery1 = """
        SELECT * from Employees where EmpName = ?
        """
        result = cursor.execute(sqlQuery1,empname)
        employee = result.fetchone()
        
        if employee:
            empid = employee[0]
            empname = employee[1]
            empemail = "exyz@gmail.com"
            
            sqlQuery2 = """
            INSERT INTO Leaves (ID,EmpID,EmpName,EmpEmail,FromDate,ToDate,Status) values (?,?,?,?,?,?,?)
            """
            cursor.execute(sqlQuery2,(leaveID,empid,empname,empemail,fromdate,todate,status))
            sqlcon.commit()
            flash("Data Inserted")
            sqlcon.close()
            return redirect(url_for('getLeaveRequest'))
        flash("Error fetching data")
        
    return render_template('ApplyLeave.html')


#Function to Delete Leave 
@app.route('/DeleteLeave/<string:id>',methods = ['GET'])
def deleteLeave(id):
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    sqlQuery = """
    DELETE from Leaves where ID = ?
    """
    cursor.execute(sqlQuery,(id))
    sqlcon.commit()
    sqlcon.close()
    return redirect(url_for('getLeaveRequest'))

@app.route('/MyClients',methods = ['GET'])
def MyClients():
    username = session['username']
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    sqlQuery = """
    Select ea.EmpName,ea.EmpEmail,ea.EmpUsername from assignee a
    join Employees e on e.EmpID = a.TrainerID
    join EmpAccounts ea on ea.EmpAccID = a.ClientID
    where e.EmpName = ?
    """
    res = cursor.execute(sqlQuery,(username))
    data = res.fetchall()[0]
    return render_template("Trainer/MyClients.html",data= data)

@app.route('/MyFeedback',methods=['GET'])
def feedbacks():
    username = session['username']
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    sqlQuery = """
    Select * from Feedback where trainerName = ?
    """
    cursor.execute(sqlQuery,(username))
    data = cursor.fetchall()
    return render_template("Trainer/MyFeedbacks.html",data = data,username = username)

@app.route('/MyProfile',methods=['GET'])
def myProfile():
    username = session['username']
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    sqlQuery = """
    SELECT * from EmpAccounts where EmpName = ?
    """
    cursor.execute(sqlQuery,(username))
    data = cursor.fetchall()[0]
    print(data)
    return render_template('Trainer/MyProfile.html',username = username,data = data)

#----------------------------End of Trainer Portal -------------------------------

#----------------------------Admin Portal ----------------------------------------
@app.route('/insert',methods = ['POST'])
def insertData():
    if request.method == "POST":
        flash("Data inserted successfully")
        EmpID = uuid.uuid4()
        Empname = request.form.get("EmpName")
        Empshift = request.form.get("shift")
        Empstartdate = request.form.get("date1")
        Empenddate = request.form.get("date2") 
    
        sqlcon = connect_to_database()
        cursor = sqlcon.cursor()
        Sql_query1="""
        Select EmpAccID from EmpAccounts where EmpName = ?
        """
        cursor.execute(Sql_query1,(Empname))
        TrainerName = cursor.fetchone()[0]
        sql_query = """
        INSERT INTO employees (EmpID, EmpAccID, EmpName, EmpShift, EmpStartDate, EmpToDate)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql_query, (EmpID,TrainerName, Empname, Empshift, Empstartdate, Empenddate))
        sqlcon.commit()
        sqlcon.close()
        return redirect(url_for('displayData'))

@app.route('/update', methods = ['POST'])    
def updateData():
    if request.method == "POST": 
        Empname = request.form.get("TrainerName")
        Empshift = request.form.get("shift")
        Empstartdate = request.form.get("date1")
        Empenddate = request.form.get("date2")
        sqlcon = connect_to_database()
        cursor = sqlcon.cursor()
        sql_query1 = """
        Select EmpID from Employees where EmpName = ?
        """
        cursor.execute(sql_query1,(Empname))
        id = cursor.fetchone()[0]
        sql_query = """
        UPDATE employees
        SET EmpShift = ?, EmpStartDate = ?, EmpToDate = ?
        WHERE EmpID = ?
        """
        cursor.execute(sql_query, ( Empshift, Empstartdate, Empenddate, id))
        sqlcon.commit()
        sqlcon.close()
        flash("Data updated successfully")
        return redirect(url_for('displayData'))
    return render_template('displayRoster.html')


@app.route('/delete/<string:id>', methods = ['GET'])
def deleteData(id):
    flash("Employee deleted successfully.")
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    cursor.execute("DELETE from employees WHERE EmpID=?",(id))
    sqlcon.commit()
    sqlcon.close()
    return redirect(url_for('displayData'))

#START of trainers

@app.route('/displayTasks')
def getTasks():
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    sql_query = """
    SELECT
        e.EmpAccID,e.EmpName,ep.EmpName from EmpAccounts e 
    LEFT JOIN
        assignee a on e.EmpAccID = a.ClientID
    LEFT JOIN
        Employees ep on ep.EmpID = a.TrainerID
    Where
        e.IsAdmin = 2
    """
    Trainers = getData()
    cursor.execute(sql_query)
    data = [row for row in cursor]
    sqlcon.close()
    return render_template('taskIndex.html',tasks = data,TrainerNames = Trainers)


   
# Function to fetch data from the database
def getData():
    with app.app_context():
        sqlCon = connect_to_database()
        cursor = sqlCon.cursor()
        cursor.execute("SELECT * FROM Employees")
        data = [row for row in cursor]
        sqlCon.close()  # Close the connection
    return data

# Route to display the HTML page
@app.route('/Display')
def displayData():
    data = getData()
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    
    sql_query1 = """
    SELECT ea.EmpName 
    FROM EmpAccounts ea
    LEFT JOIN Employees e ON ea.EmpAccID = e.EmpAccID
    WHERE ea.IsAdmin = 0 AND e.EmpAccID IS NULL
    """
    Sql_query2="""
    Select EmpName from Employees
    """
    cursor.execute(sql_query1)
    res = cursor.fetchall()
    emp_names = [row[0] for row in res]
    
    cursor.execute(Sql_query2)
    result = cursor.fetchall()
    TrainerNames = [row[0] for row in result]
    return render_template('displayRoster.html', data=data,EmpNames = emp_names,TrainersName = TrainerNames)

@app.route('/AcceptShiftrequest/<string:id>',methods = ['GET'])
def acceptShiftrequest(id):
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    sqlQuery = """
    UPDATE Shiftrequest SET Action = 1 where ShiftID = ?
    """
    cursor.execute(sqlQuery,(id))
    sqlcon.commit()
    sqlcon.close()
    return redirect(url_for('getRequests'))

#Function to Reject Shift request 
@app.route('/RejectShiftrequest/<string:id>',methods = ['GET'])
def rejectShiftrequest(id):
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    sqlQuery = """
    UPDATE Shiftrequest SET Action = 0 where ShiftID = ?
    """
    cursor.execute(sqlQuery,(id))
    sqlcon.commit()
    sqlcon.close()
    return redirect(url_for('getRequests'))
#Function to get Timesheet page
@app.route('/timesheet')
def getTimesheet():
    username = session['username']
    slqCon = connect_to_database()
    cursor = slqCon.cursor()
    sqlQUERY2 = """
    SELECT * From EmpAccounts where EmpName = ?
    """
    res = cursor.execute(sqlQUERY2,username)
    emp = cursor.fetchone()
    isAdmin = emp[5]
    sqlQuery1 ="""
        SELECT * From Timesheet
        """
    cursor.execute(sqlQuery1)
    data = cursor.fetchall()
    if isAdmin == 1:
        return render_template('AdminTimesheet.html',data = data)
    else:
        sqlQuery3 = """
        SELECT * From Timesheet where EmpName = ?
        """
        cursor.execute(sqlQuery3,(username))
        res = cursor.fetchall()
        return render_template('Timesheet.html',data = res,username = username)

#Function to accept timesheet 
@app.route('/Accept/<string:id>',methods = ['GET'])
def acceptTimesheet(id):
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    sqlQuery = """
    UPDATE Timesheet SET Status = 1 where ID = ?
    """
    cursor.execute(sqlQuery,(id))
    sqlcon.commit()
    sqlcon.close()
    return redirect(url_for('getTimesheet'))

#Function to Reject timesheet 
@app.route('/Reject/<string:id>',methods = ['GET'])
def rejectTimesheet(id):
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    sqlQuery = """
    UPDATE Timesheet SET Status = 2 where ID = ?
    """
    cursor.execute(sqlQuery,(id))
    sqlcon.commit()
    sqlcon.close()
    return redirect(url_for('getTimesheet'))

#Function to accept Leave 
@app.route('/AcceptLeave/<string:id>',methods = ['GET'])
def acceptLeave(id):
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    sqlQuery = """
    UPDATE Leaves SET Status = 1 where ID = ?
    """
    cursor.execute(sqlQuery,(id))
    sqlcon.commit()
    sqlcon.close()
    return redirect(url_for('getLeaveRequest'))

#Function to Reject Leave 
@app.route('/RejectLeave/<string:id>',methods = ['GET'])
def rejectLeave(id):
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    sqlQuery = """
    UPDATE Leaves SET Status = 2 where ID = ?
    """
    cursor.execute(sqlQuery,(id))
    sqlcon.commit()
    sqlcon.close()
    return redirect(url_for('getLeaveRequest'))

#Function to assign client to Trainers
@app.route('/AssignClients',methods=['POST'])
def assignClient():
    ClientID = request.form.get('ClientID')
    TrainerName = request.form.get('EmpName')
    assigneeID = uuid.uuid4()
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    
    getID = """
    select EmpID from Employees where EmpName = ?
    """
    res = cursor.execute(getID,(TrainerName))
    TrainerID = res.fetchone()[0]
    sql_query = """
    Insert into assignee(AssignID,ClientID,TrainerID) values(?,?,?)
    """
    cursor.execute(sql_query,(assigneeID,ClientID,TrainerID))
    sqlcon.commit()
    
    return redirect(url_for('getTasks'))

#Function to transfer client to Trainers
@app.route('/transferClients',methods=['POST'])
def transferClient():
    ClientID = request.form.get('ClientID')
    TrainerName = request.form.get('EmpName')
    assigneeID = uuid.uuid4()
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    
    getID = """
    select EmpID from Employees where EmpName = ?
    """
    res = cursor.execute(getID,(TrainerName))
    TrainerID = res.fetchone()[0]
    sql_query = """
    update assignee set TrainerID = ? where ClientID = ?
    """
    cursor.execute(sql_query,(TrainerID,ClientID))
    sqlcon.commit()
    
    return redirect(url_for('getTasks'))

#function to get all trainers
@app.route('/Trainers',methods=['GET'])
def getAlltrainers():
    sql_con = connect_to_database()
    cursor = sql_con.cursor()
    
    sql_query = """
    Select * from EmpAccounts where IsAdmin = 0
    """
    cursor.execute(sql_query)
    data = cursor.fetchall()
    return render_template('Admin/Trainers.html',res = data)


@app.route('/Feedbacks',methods=['GET'])
def getAllFeedbacks():
    sql_con = connect_to_database()
    cursor = sql_con.cursor()
    
    sql_query = """
    Select * from Feedback
    """
    cursor.execute(sql_query)
    data = cursor.fetchall()
    return render_template('Admin/Feedbacks.html',res = data)
    

#------------------------- End of Admin Portal -------------------------------

#-------------------------Notification ---------------------------------------
def addNotification(messages):
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    sqlQuery = """
    INSERT into Notifications(NotificationID,Message,EmpID) values(?,?,?)
    """
    sqlQuery2 = """
    SELECT * from Employees where EmpName = ?
    """
    empname = session['username'] 
    cursor.execute(sqlQuery2,(empname))
    employee = cursor.fetchone()
    
    if employee:
        notificationID = uuid.uuid4()
        message = messages
        empID = employee[0]
        cursor.execute(sqlQuery,(notificationID,message,empID))
        sqlcon.commit()
    sqlcon.close()
    
def retriveNotifications():
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    sqlQuery = """
    SELECT Message from Notifications where EmpID = ?
    """
    empname = session['username']
    sqlQuery2 = """
    SELECT * From Employees where EmpName = ?
    """
    res = "No messages"
    cursor.execute(sqlQuery2,(empname))
    employee = cursor.fetchone()
    if employee:
        empID = employee[0]
        cursor.execute(sqlQuery,(empID))
        data = cursor.fetchall()
        
        if data:
            res = [{'Message': row[0]} for row in data]
        else:
            res = "No messages"
        print(res)
    sqlcon.close()
    return res

#------------------------------ End of Notification ----------------------------------


#------------------------------ Start of client portal --------------------------------

@app.route('/clientProfile',methods = ['GET'])
def clientProfile():
    username = session['username']
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    sqlQuery = """
    SELECT * from EmpAccounts where EmpName = ?
    """
    cursor.execute(sqlQuery,(username))
    data = cursor.fetchall()[0]
    return render_template('Client/ClientHome.html',username = username,data = data)
    
@app.route('/Myschedule', methods = ['GET'])
def mySchedule():
    username = session['username']
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    sqlQuery = """
    SELECT e.EmpName,e.EmpShift from Employees e
    Join assignee a on e.EmpID = a.TrainerID
    Join Empaccounts ea on ea.EmpAccID = a.ClientID
    where ea.EmpName = ?
    """
    cursor.execute(sqlQuery,(username))
    res = cursor.fetchall()[0]
    return render_template('Client/ClientSchedule.html',username = username,data = res)
    
@app.route('/feedback',methods=['POST'])
def feedback():
    if request.method == 'POST':
        username = session['username']
        sqlcon = connect_to_database()
        cursor = sqlcon.cursor()
        Id = uuid.uuid4()
        mes = request.form.get("message")
        date = datetime.now().strftime('%Y-%m-%d')
        print(mes)
        sqlquery1 ="""
        Select e.EmpName from Employees e
        join assignee a on e.EmpID = a.TrainerID
        join EmpAccounts ea on ea.EmpAccID = a.ClientID
        where ea.EmpName = ?
        """
        sqlQuery2 = """
        Insert into Feedback(FeedbackID,ClientName,TrainerName,Message,Date) values(?,?,?,?,?)
        """
        res = cursor.execute(sqlquery1,(username))
        TrainerName = res.fetchone()[0]
        cursor.execute(sqlQuery2,(Id,username,TrainerName,mes,date))
        sqlcon.commit()
        sqlcon.close()
    return redirect(url_for('mySchedule'))

if __name__ == '__main__':
    app.run(debug=True)
