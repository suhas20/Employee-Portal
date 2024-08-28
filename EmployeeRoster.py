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
                    return render_template('Client/ClientHome.html')
                else:
                    return redirect(url_for('userIndex'))
            else:
                flash("Invalid credentials")
        else:
            flash("No Employee found with that details")
        sqlcon.close()
    return render_template('Login/login1.html')

#-------------------------- End login functionalities--------------------------------------


@app.route('/')
def Home():
    return render_template('home/index.html')  #Login.html

@app.route('/index')
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
    return render_template('userIndex.html',notifications = notifications)


#Funtion to grt Shiftrequest page
@app.route('/getShifts')
def getShiftRequest():
    return render_template('Shiftrequest.html')

#Function to post requests
@app.route('/sendRequest', methods=['POST'])
def postRequest():
    if request.method == "POST":
        shiftID = str(uuid.uuid4())
        empName = request.form.get("EmpName")
        empEmail = request.form.get("Empemail")
        month = request.form.get("month")
        shift = request.form.get("shift")
        reason = request.form.get("reason")
        
        sqlcon = connect_to_database()
        cursor = sqlcon.cursor()
        
        Query1 = "SELECT EmpAccID FROM EmpAccounts WHERE EmpEmail = ?"
        print(f"Executing Query1: {Query1} with empEmail: {empEmail}")
        cursor.execute(Query1, (empEmail))
        result = cursor.fetchone()
        session['notification'] = []
        session['flag'] = 1 #-------------------------------------------------->#needs to check
        
        if result:
            empID = result.EmpAccID
            Query2 = """
            INSERT INTO ShiftRequest (ShiftID, EmpID, EmpName, EmpEmail, Shift, ForMonth, Reason) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(Query2, (shiftID, empID, empName, empEmail, shift, month, reason))
            sqlcon.commit()
        
            sqlcon.close()
            session['notification'].append('Test1')
            return redirect(url_for('userIndex'))
        return render_template("ShiftRequest.html")
    
    return render_template("ShiftRequest.html")

#Function to fetch shift requests
@app.route('/getRequests')
def getRequests():
    sqlcon = connect_to_database()
    cursor= sqlcon.cursor()
    sqlQuery = """
    SELECT * from Shiftrequest 
    """
    cursor.execute(sqlQuery)
    data = [row for row in cursor]
    sqlcon.close()
    return render_template("ShiftsRequestIndex.html",reqs = data)

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
        return render_template('ApplyLeave.html',data = res)

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
    WHERE ea.IsAdmin = 2 AND e.EmpAccID IS NULL
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
        return render_template('Timesheet.html',data = res)

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
    Select * from EmpAccounts where IsAdmin = 2
    """
    cursor.execute(sql_query)
    data = cursor.fetchall()
    return render_template('Admin/Trainers.html',res = data)
    

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
    cursor.execute(sqlQuery2,(empname))
    employee = cursor.fetchone()
    if employee:
        empID = employee[0]
        cursor.execute(sqlQuery,(empID))
        data = cursor.fetchall()
        res = [{'Message': row.Message} for row in data]
    sqlcon.close()
    return res

#------------------------------ End of Notification ----------------------------------

if __name__ == '__main__':
    app.run(debug=True)
