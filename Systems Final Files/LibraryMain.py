from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect
from flask_bootstrap import Bootstrap
import sqlite3 as sql

app = Flask(__name__)
Bootstrap(app)

#Initial Entry

@app.route("/")
def login():
    return render_template("libMain.html")

@app.route("/login", methods = ["POST"])
def processnum():
    if request.method == "POST":
        try:
            checkNum = int(request.form["mnum"])
        except:
            return redirect(url_for('login'))
        library = sql.connect("library_data.db")
        library.row_factory = sql.Row
        cur = library.cursor()
        cur.execute("select MNumber from members")
        clist = cur.fetchall()
        if checkNum != None:
            for x in clist:
                if int(x["MNumber"]) == checkNum:
                    return redirect(url_for('main'))
            return redirect(url_for('login'))

        return redirect(url_for('login'))

@app.route("/main")
def main():
    return render_template("homepage.html")

#Registration

@app.route("/register")
def register():
    return render_template("memberreg.html")

@app.route("/newmember", methods = ["POST"])
def memberdata():
    number = request.form["num"]
    fname = request.form["fna"]
    mname = request.form["mna"]
    lname = request.form["lna"]

    library = sql.connect("library_data.db")
    library.row_factory = sql.Row
    cur = library.cursor()
    cur.execute("select MNumber from members")
    clist = cur.fetchall()
    try:
        for x in clist:
            if str(x["MNumber"]) == number:
                return redirect(url_for('register'))
                 
        if number != "" and fname != "" and lname != "":
            cur.execute("INSERT INTO members (MNumber, Fname, Mname, Lname, ACCStatus) VALUES(?, ?, ?, ?, ?)", [number, fname, mname, lname, "Member"])
            library.commit()
            return "Registration Complete!"
        else:
            return redirect(url_for('register'))
    except:
        return redirect(url_for('register'))
    library.close()
#Display Members
@app.route("/memberlist")
def memberlist():
	con = sql.connect("library_data.db")
	con.row_factory = sql.Row

	cur = con.cursor()
	cur.execute("Select * FROM members")

	rows = cur.fetchall()
	return render_template("mdisplay.html", rows = rows)
	con.close()

#View Books
@app.route("/booklist")
def booklist():
	con = sql.connect("library_data.db")
	con.row_factory = sql.Row

	cur = con.cursor()
	cur.execute("Select * FROM books")

	rows = cur.fetchall()
	return render_template("display.html", rows = rows)
	con.close()

#Checkout Step

@app.route("/option")
def option():
    return render_template("checkout.html")

@app.route("/books", methods = ["POST"])
def bookchoice():
    if request.method == "POST":
        if request.form["checkout"] == "Check-Out":
            return render_template("checked.html")
        if request.form["checkout"] == "Return":
            return render_template("returned.html")


#Add Book

@app.route("/enterbookdata")
def bookinfo():
    return render_template("newbook.html")

@app.route("/newbookentry", methods = ["POST"])
def addbook():
    library = sql.connect("library_data.db")
    cur = library.cursor()
    bookid = request.form["bid"]
    booktitle = request.form["tit"]
    bookauthor = request.form["auth"]
    try:
        if bookid != "" and booktitle != "" and bookauthor != "":
            cur.execute("INSERT INTO books (BookID, Title, Author) VALUES(?, ?, ?)", [bookid, booktitle, bookauthor])
            library.commit()
            return redirect(url_for('booklist'))
        else:
            return redirect(url_for('bookinfo'))
    except:
        return redirect(url_for('bookinfo'))
    library.close()



#def create_members():
#    database = sql.connect("library_data.db")
#    database.execute("CREATE TABLE members (MNumber INTEGER PRIMARY KEY, Fname TEXT NOT NULL, Mname TEXT, Lname TEXT NOT NULL, ACCStatus TEXT NOT NULL)")
#    database.execute("CREATE TABLE books (BookID INTEGER PRIMARY KEY, Title TEXT NOT NULL, Author TEXT NOT NULL)")
#    database.close()

#create_members()

app.run(debug = True)