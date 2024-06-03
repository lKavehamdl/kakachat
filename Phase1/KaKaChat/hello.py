#KhOMAK!!

from flask import Flask, render_template, request, redirect, url_for, session, g, current_app
from flask_mysqldb import MySQL
import MySQLdb.cursors, datetime, time, random
 

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'k..h3002'
app.config['MYSQL_DB'] = 'kakachat'

mysql = MySQL(app)
msg = ""
token = ""
chatid = 0
phoneNumber = -1

def myHash(userID):
    ans = ""
    for i in range(len(userID)):
        temp = random.randint(97, 122)
        ans += chr(temp)
    return ans

@app.route('/', methods = ['GET', 'POST'])
def index():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM authentication')
        res = cursor.fetchall()
        if request.method == "GET":
            for x in res:
                if x['IP'] == request.remote_addr and x['saveLogin'] == "1":
                    var = x['phoneNumber']
                    temp = x['token']
                    global token
                    token = temp
                    global phoneNumber
                    phoneNumber = var
                    cursor.execute('SELECT * FROM chats WHERE token1 = %s', [token])
                    chats = cursor.fetchall()
                    return redirect(url_for('chats'))
            return render_template('index.html')
        elif request.method == "POST":
            for x in res:
                if x['IP'] == request.remote_addr:
                    temp = x['token']
                    token
                    token =""
                    phoneNumber
                    phoneNumber = -1
                    cursor.execute("DELETE FROM authentication WHERE token = %s", [temp])
                    mysql.connection.commit()
                    return render_template('index.html')
    except:
        return"<h1> server error </h1>"
            
@app.route("/ru")
def read():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users')
        res = cursor.fetchall()
        return render_template("read.html", results = res)
    except:
        return"<h1> server error </h1>"    
@app.route("/ra")
def readAuthentication():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM authentication')
        res = cursor.fetchall()
        return render_template("readAuthentication.html", results = res)
    except:
        return"<h1> server error </h1>"    

@app.route("/register", methods = ['GET', 'POST'])
def create():
    try:
        msg = ""
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            username = request.form.get("username")
            phoneNumber = request.form.get("phoneNumber")
            password = request.form.get("password")
            Fname = request.form.get("FName")
            Lname = request.form.get("LName")
            userToken = myHash(username)
            if len(phoneNumber) != 11 :
                msg = "WRONG INPUT"
                return render_template('create.html', msg = msg)
            cursor.execute('INSERT INTO users VALUES (% s, % s, % s, % s, % s, %s)',(username, phoneNumber, password, Fname, Lname, userToken))
            mysql.connection.commit()
            return render_template('index.html')
        return render_template('create.html', msg = msg)
    except:
        return"<h1> server error </h1>"
    
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
                saveLogin = True
            else:
                saveLogin = False
            cursor.execute("SELECT * FROM users")
            res = cursor.fetchall()
            for x in res:
                if x['ID'] == username and x['pass'] == password:
                    var = x['token']
                    temp2 = x['phoneNumber']
                    global token
                    token = var
                    global phoneNumber
                    phoneNumber = temp2
                    cursor.execute("SELECT * FROM authentication WHERE token = %s", [token])
                    temp = cursor.fetchone()
                    try:
                        if temp['token'] == token:
                            cursor.execute("DELETE FROM authentication WHERE token = %s", [token])
                            mysql.connection.commit()
                            if saveLogin:
                                cursor.execute('INSERT INTO authentication VALUES (%s, %s, %s, %s ,%s)',(username, phoneNumber, ip, "1", token))
                                mysql.connection.commit()
                            else:
                                cursor.execute('INSERT INTO authentication VALUES (%s, %s, %s, %s)',(username, phoneNumber, ip, "0", token))
                                mysql.connection.commit()
                            return redirect(url_for('chats'))
                    except:
                        if saveLogin:
                            cursor.execute('INSERT INTO authentication VALUES (%s, %s, %s, %s, %s)',(username, phoneNumber, ip, "1", token))
                            mysql.connection.commit()
                        else:
                            cursor.execute('INSERT INTO authentication VALUES (%s, %s, %s, %s, %s)',(username, phoneNumber, ip, "0", token))
                            mysql.connection.commit()
                        return redirect(url_for('chats'))
            global msg
            msg = "invalid input"
            return render_template("login.html", msg = msg)
        elif request.method == "GET":
            msg = ""
            return render_template("login.html", msg = msg)
    except:
       return"<h1> server error </h1>"
    
@app.route("/chats", methods=['GET', 'POST'])
def chats():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'GET':
            cursor.execute("SELECT * FROM chats NATURAL JOIN users WHERE token1 = %s AND token = token2", [token])
            res = cursor.fetchall()
            cursor.execute("SELECT * FROM chats WHERE token1 = %s", [token])
            res2 = cursor.fetchall()
            return render_template("chats.html", chats = res, res2 = res2)
        elif request.method == 'POST':
            global chatid
            chatid = request.form.get('chatID')
            return redirect(url_for('page', id = chatid))
    except:
        return"<h1> server error </h1>"
    
@app.route("/logout", methods = ["GET", "POST"])
def logOut():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == "POST":
            global token
            cursor.execute("DELETE FROM authentication WHERE token = %s", [token])
            mysql.connection.commit()
            token = ""
            return redirect(url_for('index'))
    except:
        return"<h1> server error </h1>"
    
@app.route("/createContact", methods = ["GET", "POST"])
def createContact():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == "GET":
            return render_template("createContact.html")
        elif request.method == "POST":
            name = request.form.get("name")
            phoneNumber2 = request.form.get("phoneNumber")
            cursor.execute("SELECT token FROM users WHERE phoneNumber = %s" ,[phoneNumber2])
            tmp = cursor.fetchone()
            token2 = tmp['token']
            cursor.execute("INSERT INTO contacts(token1, token2, contactName) VALUES(%s, %s, %s)",(token, token2, name))
            mysql.connection.commit()
            cursor.execute("UPDATE chats SET contactName = %s WHERE token1 = %s AND token2 = %s", (name, token, token2))
            mysql.connection.commit()
            return redirect(url_for('chats'))
    except:
        return"<h1> server error </h1>"
@app.route("/createChat", methods = ["GET", "POST"])
def createChat():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == "GET":
            cursor.execute("SELECT * FROM contacts NATURAL JOIN USERS WHERE token1 = %s AND token = token2", [token])
            res = cursor.fetchall()
            return render_template("createChat.html", res = res)
        elif request.method == "POST":
            name = request.form.get("name")
            cursor.execute("SELECT * FROM contacts WHERE contactName = %s AND token1 = %s", (name, token))
            res = cursor.fetchone()
            token2 = res["token2"]       
            cursor.execute("INSERT INTO chats(token1, token2, contactName) VALUES(%s, %s, %s)", (token, token2, name))
            mysql.connection.commit()
            cursor.execute("SELECT * FROM chats WHERE token1 = %s AND token2 = %s", (token, token2))
            res = cursor.fetchone()
            chatId = res['chatID']
            cursor.execute("SELECT contactName FROM contacts WHERE token1 = %s AND token2 = %s", (token2, token))
            res = cursor.fetchone()
            try:
                contactName2 = res['contactName']
                cursor.execute("INSERT INTO chats(chatID, token1, token2, contactName) VALUES(%s, %s, %s, %s)", (chatId, token2, token, contactName2))
                mysql.connection.commit()
            except:
                cursor.execute("INSERT INTO chats(chatID, token1, token2) VALUES(%s, %s, %s)", (chatId, token2, token))
                mysql.connection.commit()
            return redirect(url_for('chats'))
    except:
        return"<h1> server error </h1>"
    
@app.route("/createGroupChat", methods = ["GET", "POST"])
def createGroupChat():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == "GET":
            return render_template("createGroupChat.html")
        elif request.method == "POST":
            name = request.form.get('name')
            cursor.execute("INSERT INTO chats(token1, groupName, groupOwner) VALUES(%s, %s, %s)", (token, name, token))
            mysql.connection.commit()
            return redirect(url_for('chats'))
    except:
        return"<h1> server error </h1>"
    
@app.route("/addMember", methods = ["GET", "POST"])
def addMember():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == "GET":
            cursor.execute("SELECT * FROM chats WHERE token1 = %s AND groupName IS NOT NULL AND groupOwner = %s", (token, token))
            res = cursor.fetchall()
            return render_template("addMember.html", res = res)
        if request.method == "POST":
            groupID = request.form.get("chatID")
            phoneNumber = request.form.get("user")
            cursor.execute("SELECT token FROM users WHERE phoneNumber = %s", [phoneNumber])
            temp = cursor.fetchone()
            token2 = temp['token']
            cursor.execute("SELECT * FROM chats WHERE chatID = %s", [groupID])
            res = cursor.fetchone()
            gName = res['groupName']
            cursor.execute("INSERT INTO chats(chatID, token1, groupName, groupOwner) VALUES(%s, %s, %s, %s)", (groupID, token2, gName, token))
            mysql.connection.commit()
            return redirect(url_for('chats'))
    except:
        return"<h1> server error </h1>"

@app.route("/deleteContact", methods = ["GET", "POST"])
def deleteContacts():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == "GET":
            cursor.execute("SELECT * FROM users NATURAL JOIN contacts WHERE token = token2")
            res = cursor.fetchall()
            return render_template("deleteContact.html", res = res)
        elif request.method == "POST":
            phoneNumber2 = request.form.get("phoneNumber")
            cursor.execute("SELECT * FROM users WHERE phoneNumber = %s", [phoneNumber2])
            res = cursor.fetchone()
            token2 = res['token']
            cursor.execute("DELETE FROM contacts WHERE token1 = %s AND token2 = %s", (token, token2))
            mysql.connection.commit()
            cursor.execute("UPDATE chats SET contactName = null WHERE token1 = %s AND token2 = %s", (token, token2))
            mysql.connection.commit()
            return redirect(url_for('chats'))
    except:
        return"<h1> server error </h1>"
    
@app.route("/changeContact", methods=["GET", "POST"])
def changeContact():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == "GET":
            cursor.execute("SELECT * FROM users NATURAL JOIN contacts WHERE token = token1")
            res = cursor.fetchall()
            return render_template("changeContact.html", res = res)
        elif request.method == "POST":
            newName = request.form.get("name")
            phoneNumber2 = request.form.get("phoneNumber2")
            cursor.execute("SELECT * FROM users WHERE phoneNumber = %s", [phoneNumber2])
            res = cursor.fetchone()
            token2 = res['token']
            cursor.execute("UPDATE contacts SET contactName = %s WHERE token1 = %s AND token2 = %s", (newName, token, token2))
            mysql.connection.commit()
            cursor.execute("UPDATE chats SET contactName = %s WHERE token1 = %s AND token2 = %s", (newName, token, token2))
            return redirect(url_for('chats'))
    except:
        return"<h1> server error </h1>"
    
@app.route("/contactList", methods =["GET","POST"])
def contactList():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == "GET":
            cursor.execute("SELECT * FROM contacts NATURAL JOIN users WHERE token1 = %s AND token = token2", [token])
            res = cursor.fetchall()
            return render_template("contacts.html", res = res)
    except:
        return"<h1> server error </h1>"
    
@app.route("/deleteChat", methods = ["GET", "POST"])
def deleteChat():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == "GET":
            cursor.execute("SELECT * FROM chats NATURAL JOIN users WHERE token1 = %s AND token2 IS NOT NULL AND token2 = token", [token])
            res = cursor.fetchall()
            return render_template("deleteChat.html", res = res)
        elif request.method == "POST":
            phoneNumber2 = request.form.get("phoneNumber")
            cursor.execute("SELECT token FROM users WHERE phoneNumber = %s", [phoneNumber2])
            res = cursor.fetchone()
            token2 = res['token']
            cursor.execute("SELECT chatID FROM chats WHERE token1 = %s AND token2 = %s", (token, token2))
            res = cursor.fetchone()
            chatId = res['chatID']
            cursor.execute("DELETE FROM messages WHERE chatID = %s", [chatId])
            mysql.connection.commit()
            cursor.execute("DELETE FROM chats WHERE chatID = %s", [chatId])
            mysql.connection.commit()
            return redirect(url_for('chats'))
    except:
        return"<h1> server error </h1>"
        
@app.route("/changeGroupName", methods = ["GET", "POST"])
def changeGroupName():    
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == "GET":
            cursor.execute("SELECT DISTINCT chatID, groupName FROM chats WHERE groupOwner = %s", [token])
            res = cursor.fetchall()
            return render_template("changeGN.html", res = res)
        elif request.method == "POST":
            chatId = request.form.get("chatId")
            newName = request.form.get("name")
            cursor.execute("UPDATE chats SET groupName = %s WHERE chatID = %s", (newName, chatId))
            mysql.connection.commit()
            return redirect(url_for('chats'))
    except:
        return"<h1> server error </h1>"
    
@app.route("/leaveGP", methods = ["GET", "POST"])
def leaveGP():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == "GET":
            cursor.execute("SELECT * FROM chats WHERE token1 = %s AND groupName IS NOT NULL", [token])
            res = cursor.fetchall()
            return render_template("leaveGP.html", res = res)
        elif request.method == "POST":
            chatId = request.form.get("chatId")
            cursor.execute("DELETE FROM messages WHERE sender = %s AND chatID = %s", (token , chatId))
            mysql.connection.commit()
            cursor.execute("DELETE FROM chats WHERE token1 = %s AND chatID = %s", (token, chatId))
            mysql.connection.commit()
            return redirect(url_for('chats'))
    except:
        return"<h1> server error </h1>"
        

@app.route("/page/<id>", methods = ['POST', 'GET'])
def page(id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == "GET":
            cursor.execute("SELECT DISTINCT * FROM messages NATURAL JOIN users WHERE chatID = %s AND sender = token ORDER BY messageTime", [id])
            res = cursor.fetchall()
            return render_template("page.html", res = res, token = token)
        elif request.method == "POST":
            message = request.form.get("message")
            ts = time.time()
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("INSERT INTO messages(chatID, message, messageTime, sender) VALUES(%s, %s, %s, %s)", (id, message, timeStamp, token))
            mysql.connection.commit()
            return redirect(url_for('page', id = id))
    except:
        return"<h1> server error </h1>"

    
@app.route("/deleteMessage", methods = ["GET" , "POST"])
def deleteMessage():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == "GET":
            cursor.execute("SELECT * FROM messages WHERE chatID = %s AND sender = %s" ,(chatid, token))
            res = cursor.fetchall()
            return render_template("deleteM.html", res = res)
        elif request.method == "POST":
            mID = request.form.get("messageId")
            cursor.execute("DELETE FROM messages WHERE sender = %s AND messageID = %s", (token, mID))
            mysql.connection.commit()
            return redirect(url_for('page', id = chatid))
    except:
        return"<h1> server error </h1>"
    
@app.route("/editMessage", methods = ["GET" , "POST"])
def editMessage():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == "GET":
            cursor.execute("SELECT * FROM messages WHERE chatID = %s AND sender = %s" ,(chatid, token))
            res = cursor.fetchall()
            return render_template("editM.html", res = res)
        elif request.method == "POST":
            mID = request.form.get("messageId")
            newMessage = request.form.get("message")
            cursor.execute("UPDATE messages SET message = %s WHERE sender = %s AND messageID = %s", (newMessage, token, mID))
            mysql.connection.commit()
            return redirect(url_for('page', id = chatid))
    except:
        return"<h1> server error </h1>"

@app.route("/page/", methods= ["GET", "POST"])
def test():
    try:
        if request.method == "POST":
            return redirect(url_for('page', id = chatid), code=307)
    except:
        return"<h1> server error </h1>"
    
@app.route("/changeInfo", methods =["GET", "POST"])
def changeInfo():
    try:
        if request.method == "GET":
            return render_template("PersonalInfo.html")
    except:
        return"<h1> server error </h1>"
    
@app.route("/changeUsername", methods = ["GET", "POST"])
def changeUsername():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == "GET":
            return render_template("changeUsername.html")
        if request.method == "POST":
            newUsername = request.form.get("username")
            cursor.execute("UPDATE users SET ID = %s WHERE token = %s", (newUsername, token))
            mysql.connection.commit()
            cursor.execute("UPDATE authentication SET ID = %s WHERE token = %s", (newUsername, token))
            mysql.connection.commit()
            return redirect(url_for('chats'))
    except:
        return"<h1> server error </h1>"
    
    
@app.route("/changePassword", methods = ["GET", "POST"])
def changePassword():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == "GET":
            return render_template("changePassword.html")
        if request.method == "POST":
            newPassword = request.form.get("password")
            cursor.execute("UPDATE users SET pass = %s WHERE token = %s", (newPassword, token))
            mysql.connection.commit()
            return redirect(url_for('chats'))
    except:
        return"<h1> server error </h1>"
    
@app.route("/changeFirstName", methods = ["GET", "POST"])
def changeFname():
    try:  
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == "GET":
            return render_template("changeFname.html")
        if request.method == "POST":
            newFname = request.form.get("Fname")
            cursor.execute("UPDATE users SET Fname = %s WHERE token = %s", (newFname, token))
            mysql.connection.commit()
            return redirect(url_for('chats'))
    except:
        return"<h1> server error </h1>"
    
@app.route("/changeLastName", methods = ["GET", "POST"])
def changeLname():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == "GET":
            return render_template("changeLname.html")
        if request.method == "POST":
            newLname = request.form.get("Lname")
            cursor.execute("UPDATE users SET Lname = %s WHERE token = %s", (newLname, token))
            mysql.connection.commit()
            return redirect(url_for('chats'))
    except:
        return"<h1> server error </h1>"
    
    
@app.route("/changePhoneNumber", methods = ["GET", "POST"])
def changePhoneNumber():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == "GET":
            return render_template("changePhoneNumber.html")
        if request.method == "POST":
            newPhoneNumber = request.form.get("phoneNumber")
            cursor.execute("UPDATE users SET phoneNumber = %s WHERE token = %s", (newPhoneNumber, token))
            mysql.connection.commit()
            cursor.execute("UPDATE authentication SET phoneNumber = %s WHERE token = %s", (newPhoneNumber, token))
            mysql.connection.commit()
            return redirect(url_for('chats'))
    except:
        return"<h1> server error </h1>"
    
    
@app.route("/deleteAccount", methods = ["GET", "POST"])
def deleteUser():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == "GET":
            global token
            cursor.execute("DELETE FROM messages WHERE sender = %s", [token])
            mysql.connection.commit()
            cursor.execute("DELETE FROM chats WHERE token1 = %s OR token2 = %s", (token, token))
            mysql.connection.commit()
            cursor.execute("DELETE FROM authentication WHERE token = %s", [token])
            mysql.connection.commit()
            cursor.execute("DELETE FROM users WHERE token = %s", [token])
            mysql.connection.commit()
            token = ""
            return redirect(url_for('index'))
    except:
        return"<h1> server error </h1>"
        
@app.route("/yourInfo", methods = ["GET", "POST"])
def Info():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == "GET":
            cursor.execute("SELECT ID, phoneNumber, pass, FName, LName FROM users WHERE token = %s", [token])
            res = cursor.fetchall()
            return render_template("showInfo.html", res = res)
    except:
        return"<h1> server error </h1>"
        
if __name__ == "__main__":
    app.run()