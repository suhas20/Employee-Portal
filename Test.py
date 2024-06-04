import pyodbc
from flask import Flask, render_template

app = Flask(__name__)

#connection
sqlCon = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-UNVMP3TE\\SQLEXPRESS01;DATABASE=LibraryManagement;UID=sa;PWD=Suhas@20')


#get
def getData(sqlCon):
    print("Reading")
    cursor = sqlCon.cursor();
    cursor.execute("select * from Books")
    data = [row for row in cursor]
    return data
    #for row in cursor:
    #    print(f'{row}')

@app.route('/')
def displayData():
    with app.app_context():
        data = getData(sqlCon)
    print(data)
    return render_template('index.html',data = data)
        

#Insert
def insertData(sqlCon):
    print("Insert")
    BookId = input("Enter BookId: ")
    BookTitle = input("Enter BookTitle: ")
    BookCategory = input("Enter BookCategory: ")
    BookAuthor = input("Enter BookAuthor: ")
    BookCopies = input("Enter BookCopies: ")
    BookPubName = input("Enter BookPubName: ")
    Copyrights = input("Enter Copyrights: ")
    DateAdded = input("Enter DateAdded (YYYY-MM-DD): ")
    Status = input("Enter Status: ")

    cursor = sqlCon.cursor()
    cursor.execute("INSERT INTO Books (BookId, BookTitle, BookCategory, BookAuthor, BookCopies, BookPubName, Copyrights, DateAdded, Status)"
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (BookId, BookTitle, BookCategory, BookAuthor, BookCopies, BookPubName, Copyrights, DateAdded, Status))
    print("Inserted")
    sqlCon.commit()
    

#Delete
def deleteData(sqlCon):
    print("Deleting");
    BookID = input("Enter the book ID yo wish to delete:\n")
    cursor = sqlCon.cursor()
    cursor.execute("delete from Books where BookID = ?",BookID)
    print("Deleted!!")

getData(sqlCon)
displayData()

if __name__ == '__main__':
     with app.app_context():
        app.run(debug=True)


#Update

    




#Sql": "Data Source=LAPTOP-UNVMP3TE\\SQLEXPRESS01;Initial Catalog= \"Sports Ecommerce\";Persist Security Info=True;User ID=sa;Password=Suhas@20;TrustServerCertificate=True"
 # },