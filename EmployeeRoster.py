from flask import Flask, render_template,request, url_for, flash, jsonify, session
from werkzeug.utils import redirect
import pyodbc
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'My secret Key'

# Function to establish connection to SQL Server
def connect_to_database():
    return pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-UNVMP3TE\\SQLEXPRESS01;DATABASE=EmployeePortal;UID=sa;PWD=Suhas@20')

#funtion to register
@app.route('/register', methods = ['POST'])
def registerPage():
    if request.method == "POST":
        EmpAccID = uuid.uuid4()
        empEmail = request.form.get("EmpEmail")
        empName = request.form.get("EmpName")
        empUsername = request.form.get("EmpUsername")
        empPassword = request.form.get("EmpPassword")
        userType = request.form.get("userType")
        
        isAdmin = 1 if userType == "Admin" else 0
        
        sqlcon = connect_to_database()
        cursor = sqlcon.cursor()
        sqlQuery = """
        INSERT into EmpAccounts (EmpAccID,EmpEmail,EmpPassword,EmpName,EmpUsername,IsAdmin) values(?,?,?,?,?,?)
        """
        cursor.execute(sqlQuery,(EmpAccID,empEmail,empPassword,empName,empUsername,isAdmin))
        flash("Registered  successfully")
        sqlcon.commit()
        sqlcon.close()
        return redirect(url_for("loginPage"))
        

#Function to Login
@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    if request.method == "POST":
        EmpEmail = request.form.get("empEmail")
        EmpPass = request.form.get("empPass")
        sqlcon = connect_to_database()
        cursor = sqlcon.cursor()
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
                else:
                    return redirect(url_for('userIndex'))
            else:
                flash("Invalid credentials")
        else:
            flash("No Employee found with that details")
        sqlcon.close()
    return render_template('login.html')

#Function to get userIndex
@app.route('/userIndex')
def userIndex():
    return render_template('userIndex.html')

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
        
        print(f"Form Data - empName: {empName}, empEmail: {empEmail}, month: {month}, shift: {shift}, reason: {reason}")
        
        sqlcon = connect_to_database()
        cursor = sqlcon.cursor()
        
        Query1 = "SELECT EmpAccID FROM EmpAccounts WHERE EmpEmail = ?"
        print(f"Executing Query1: {Query1} with empEmail: {empEmail}")
        cursor.execute(Query1, (empEmail))
        result = cursor.fetchone()
        print(result)
        
        if result:
            empID = result.EmpAccID
            Query2 = """
            INSERT INTO ShiftRequest (ShiftID, EmpID, EmpName, EmpEmail, Shift, ForMonth, Reason) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(Query2, (shiftID, empID, empName, empEmail, shift, month, reason))
            sqlcon.commit()
        
            sqlcon.close()
            return redirect(url_for('Home'))
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
    
# Function to fetch data from the database
def getData():
    print("Reading")
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
    # Fetch data from the database within the application context
    data = getData()
    # Render the HTML template with the fetched data
    return render_template('displayRoster.html', data=data)

@app.route('/')
def Home():
    return render_template('Login.html')  #userIndex.html 

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
        empname = "Test3" #session['username']
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
            sqlcon.close()
            return redirect(url_for('getTimesheet'))
        flash("Error fetching data")
        
    return render_template('Timesheet.html')

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
        empname = "Test3" #session['username']
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

@app.route('/index')
def Index():
    username = session['username']
    return render_template('Index1.html',username = username)

@app.route('/insert',methods = ['POST'])
def insertData():
    if request.method == "POST":
        flash("Data inserted successfully")
        EmpID = uuid.uuid4()
        Empname = request.form.get("name")
        Empshift = request.form.get("shift")
        Empstartdate = request.form.get("date1")
        Empenddate = request.form.get("date2") 
        sqlcon = connect_to_database()
        cursor = sqlcon.cursor()
        sql_query = """
        INSERT INTO employees (EmpID, EmpName, EmpShift, EmpStartDate, EmpToDate)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sql_query, (EmpID, Empname, Empshift, Empstartdate, Empenddate))
        sqlcon.commit()
        sqlcon.close()
        return redirect(url_for('displayIndex'))

@app.route('/update', methods = ['POST'])    
def updateData():
    if request.method == "POST":
        EmpID = request.form.get("id")  # Assuming EmpID is provided in the form
        Empname = request.form.get("name")
        Empshift = request.form.get("shift")
        Empstartdate = request.form.get("date1")
        Empenddate = request.form.get("date2")
        sqlcon = connect_to_database()
        cursor = sqlcon.cursor()
        sql_query = """
        UPDATE employees
        SET EmpShift = ?, EmpStartDate = ?, EmpToDate = ?
        WHERE EmpID = ? AND EmpName = ?
        """
        cursor.execute(sql_query, ( Empshift, Empstartdate, Empenddate, EmpID, Empname))
        sqlcon.commit()
        sqlcon.close()
        flash("Data updated successfully")
        return redirect(url_for('displayIndex'))
    return render_template('displayRoster.html')


@app.route('/delete/<string:id>', methods = ['GET'])
def deleteData(id):
    flash("Employee deleted successfully.")
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    cursor.execute("DELETE from employees WHERE EmpID=?",(id))
    sqlcon.commit()
    sqlcon.close()
    return redirect(url_for('displayIndex'))

#START of TASKS

@app.route('/displayTasks')
def getTasks():
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    sql_query = """
    SELECT
        t.TaskID,
        e.Empname,
        t.CreatedOn,
        t.ShortDescription,
        t.WorkNotes
    FROM
        Tasks t
    JOIN
        employees e ON t.AssignedTo = e.EmpID;
    """
    
    cursor.execute(sql_query)
    data = [row for row in cursor]
    sqlcon.close()
    return render_template('taskIndex.html',tasks = data)#

@app.route('/task/<int:task_id>')
def task_detail(task_id):
    sqlcon = connect_to_database()
    cursor = sqlcon.cursor()
    query = """
        SELECT 
            t.TaskID,
            e.EmpName,
            t.CreatedOn,
            t.ShortDescription,
            t.WorkNotes
        FROM 
            Tasks t
        JOIN 
            employees e ON t.AssignedTo = e.EmpID
        WHERE 
            t.TaskID = ?;
    """
    cursor.execute(query, (task_id))
    task = cursor.fetchone()
    sqlcon.close()
    if task:
        task_detail = {
            'TaskID': task[0],
            'EmpName': task[1],
            'CreatedOn': task[2],
            'ShortDescription': task[3],
            'WorkNotes': task[4]
        }
        return jsonify(task_detail)
    else:
        return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
