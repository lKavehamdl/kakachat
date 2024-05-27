
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, redirect, url_for, session, g, current_app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'k..h3002'
app.config['MYSQL_DB'] = 'kakachat'

mysql = MySQL(app)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route("/r")
def read():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users')
        res = cursor.fetchall()
        return render_template("read.html", results = res)
    except:
        return "<h1> NU UH </h1>"
@app.route("/register", methods = ['GET', 'POST'])
def create():
    #try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        msg = ""
        if request.method == 'POST':
            username = request.form.get("username")
            phoneNumber = request.form.get("phoneNumber")
            password = request.form.get("password")
            Fname = request.form.get("FName")
            Lname = request.form.get("LName")
            if len(phoneNumber) != 11 :
                msg = "WRONG INPUT"
                return render_template('create.html', msg = msg)
            cursor.execute('INSERT INTO users VALUES (% s, % s, % s, % s, % s)',(username, phoneNumber, password, Fname, Lname))
            mysql.connection.commit()
            print((username, phoneNumber, password, Fname, Lname))
            return render_template('index.html')
        return render_template('create.html', msg = msg)
    # except:
    #     return "<h1> NAH </h1>"
    
@app.route("/login", methods = ['GET', 'POST'])
def login():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            username = request.form.get("useranme")
            password = request.form.get("password")
            ip = request.remote_addr
            saveLogin = request.form.get("saveLogin")
            cursor.execute("SELECT * FROM users")
            res = cursor.fetchall()
            for x in res:
                if x['ID'] == username and x['pass'] == password:
                    if saveLogin:
                        cursor.execute('INSERT INTO users VALUES (% s, % s, % s, % s)'(username, x['phoneNumber'], ip, saveLogin))
                        mysql.connection.commit()
                        print("user :" + x['username'] + "authenticated")
                    cursor.execute('SELECT * FROM chats WHERE phoneNumber1 = \"%s\"', x['phoneNumber'])
                    chats = cursor.fetchall()
                    return render_template('chats.html', chats = chats)
        return render_template('login.html')
    except:
        return "<h1> mission failed </h1>"

if __name__ == "__main__":
    app.run()