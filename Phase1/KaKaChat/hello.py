
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
msg = ""
token = ""

@app.route('/', methods = ['GET', 'POST'])
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM authentication')
    res = cursor.fetchall()
    if request.method == "GET":
        for x in res:
            if x['IP'] == request.remote_addr:
                phoneNumber = x['phoneNumber']
                global token
                token = phoneNumber
                cursor.execute('SELECT * FROM chats WHERE phoneNumber1 = %s', [phoneNumber])
                chats = cursor.fetchall()
                #return render_template('chats.html', chats = chats)
                return redirect(url_for('chats'))
        return render_template('index.html')
    elif request.method == "POST":
        for x in res:
            if x['IP'] == request.remote_addr:
                username = x['ID']
                print(username)
                token =""
                cursor.execute("DELETE FROM authentication WHERE ID = %s", [username])
                mysql.connection.commit()
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
        msg = ""
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
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
            username = request.form.get("username")
            password = request.form.get("password")
            ip = request.remote_addr
            saveLogin = request.form.get("saveLogin")
            if(saveLogin == "on"):
                print("YES")
                saveLogin = True
            else:
                print("NO")
                saveLogin = False
            print(saveLogin)
            cursor.execute("SELECT * FROM users")
            res = cursor.fetchall()
            for x in res:
                if x['ID'] == username and x['pass'] == password:
                    phoneNumber = x['phoneNumber']
                    if saveLogin:
                        # values = (username, phoneNumber, ip, 1)
                        # print(values)
                        # print(" ======== ")
                        cursor.execute('INSERT INTO authentication VALUES (%s, %s, %s, %s)',(username, phoneNumber, ip, "1"))
                        mysql.connection.commit()
                        print("INSERTED")
                    cursor.execute('SELECT * FROM chats WHERE phoneNumber1 = %s', [phoneNumber])
                    chats = cursor.fetchall()
                    #return redirect("/chats", chats = chats)
                    Id = phoneNumber
                    #return render_template('chats.html', chats = chats)
        return render_template('login.html')
    except:
        return "<h1> mission failed </h1>"
    
@app.route("/chats", methods=['GET', 'POST'])
def chats():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'GET':
        cursor.execute("SELECT * FROM chats WHERE phoneNumber1 = %s", [token])
        res = cursor.fetchall()
        return render_template("chats.html", chats = res)
    elif request.method == 'POST':
        chatid = request.form.get('chatID')
        #print(chatid)
        return redirect(url_for('page', id = chatid))
        

@app.route("/page/<id>", methods = ['POST', 'GET'])
def page(id):
    print(id)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "GET":
        cursor.execute("SELECT * FROM messages WHERE chatID = %s", [id])
        res = cursor.fetchall()
        for x in res:
            print(x)
        return render_template("page.html", res = res)

if __name__ == "__main__":
    app.run()