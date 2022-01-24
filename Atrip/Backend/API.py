# coding=utf8
from flask import Flask, render_template, jsonify, request ,session, app
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL
from datetime import timedelta
import MySQLdb.cursors
import re
import bcrypt
import secrets
import string
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import googlemaps
from findRoute import allResults,sortResult

app = Flask(__name__)
app.secret_key = 'SoftDev'
app.config['MYSQL_HOST'] = 'computerengineering.3bbddns.com'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'SD'
app.config['MYSQL_PORT'] = 34674
mysql = MySQL(app)
cors = CORS(app, resources={r"/api/*": {"origins": "localhost:8080/*"}})

Testform = [
     {'name': 'BURGER', 'ingredients': ['this', 'that', 'blah']},
     {'name': 'HOTDOG', 'ingredients': ['Chicken', 'Bread']}
 ]


@app.route("/register", methods = ['GET', 'POST'])
@cross_origin()
def register():
    # Output message if something goes wrong...
    form = {'result' : False,'msg' : ''}
    content = request.get_json()
    # print("get in stage 1")
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and content['username'] and content['password'] and content['email'] and content['firstname'] and content['lastname'] and content['birthday']:
        # Create variables for easy access
        # print("get in stage 2")
        print(content)
        username = content['username']
        password = content['password']
        email = content['email']
        firstname = content['firstname']
        lastname = content['lastname']
        birthday = content['birthday']
        # print("username =",username,"password",password,"email",email)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Atrip_Users WHERE BINARY Username = %s or email = %s', (username,email))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            form['msg'] = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            form['msg'] = 'Invalid email address!'
        elif (not re.match(r'[A-Za-z0-9]+', username)) or (len(username) < 8) or (len(username) > 15):
            form['msg'] = 'Username must contain only characters and numbers and length between 8 and 15!'
        elif (not all(x.isalpha or x == "" for x in firstname)) or (len(firstname) > 25):
            form['msg'] = 'Plese enter valid name'
        elif (not all(x.isalpha or x == "" for x in lastname)) or (len(lastname) > 25):
            form['msg'] = 'Please enter valid surname'
        elif (len(password) < 8 or len(password) > 25):
            form['msg'] = """Password's length must between 8 and 15!"""


        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            salt = bcrypt.gensalt()
            cursor.execute('INSERT INTO Atrip_Users (username,password,email,role,FirstName,LastName,Nickname,Date) VALUES (%s, %s, %s, %s, %s, %s, %s ,%s)', (username, bcrypt.hashpw(password.encode('utf8'), salt), email,"user",firstname,lastname,username,birthday))
            mysql.connection.commit()
            form['result'] = True
            form['msg'] = 'You have successfully registered!'
            print('You have successfully registered!')
    else:
        # Form is empty... (no POST data)
        # print("get in stage 3")
        form['msg'] = 'Please fill out the form!'
    # Show registration form with message (if any)
    # print(jsonify(form))
    return jsonify(form)


@app.route("/editData", methods = ['GET', 'POST'])
@cross_origin()
def editData():
    # Output message if something goes wrong...
    form = {'FirstName' : '','LastName' : '' ,'Nickname' : '' , 'Picture' : '','msg' : ''}
    content = request.get_json()
    print(content)
    if request.method == 'POST' and content['nickName'] and content['firstName'] and content['lastName'] and content['image'] and content['id']:
        if (not all(x.isalpha or x == "" for x in content['firstName'])) or (len(content['firstName']) > 25):
            form['msg'] = 'Plese enter valid name'
        elif (not all(x.isalpha or x == "" for x in content['lastName'])) or (len(content['lastName']) > 25):
            form['msg'] = 'Please enter valid surname'
        elif (not all(x.isalpha or x == "" for x in content['nickName']) or (len(content['nickName']) > 15)):
            form['msg'] = 'Please enter valid nickname'
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('Update Atrip_Users set FirstName = %s,LastName = %s,Nickname = %s,Picture = %s where ID = %s',(content['firstName'],content['lastName'],content['nickName'],content['image'],content["id"]))
            mysql.connection.commit()
            form ["FirstName"] = content['firstName']
            form ["LastName"] = content['lastName']
            form ["Nickname"] = content['nickName']
            form ["Picture"] = content['image']
            form['result'] = True
            form['msg'] = 'success'
            print('success')
    else:
        form['msg'] = 'Please enter the form!'
    return jsonify(form)


@app.route("/login", methods = ['POST'])
@cross_origin()
def login():
    # Output message if something goes wrong...
    # Check if "username" and "password" POST requests exist (user submitted form)
    form = {'id' : "",'Username' : "", 'FirstName' : "", 'LastName' : "" , 'Nickname' : "" , "Email" : "" , "Tel" : "" ,"Tag" : "","Love" : "","Checkin" : "","Favorite" : "","Role" : "","Picture" : "","msg" : ""}
    if request.method == 'POST':
        content = request.get_json()
        username = content['username']
        password = content['password']
        # Create variables for easy access
        # Check if account exists using MySQL
        if username and password:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM Atrip_Users WHERE BINARY username = %s', [username])
            # Fetch one record and return result
            account = cursor.fetchone()
            # If account exists in accounts table in out database
            if account:
                # Create session data, we can access this data in other routes
                if bcrypt.checkpw(password.encode('utf-8'),account["Password"].encode('utf-8')):
                    form['id'] = account['ID']
                    form['Username'] = account['Username']
                    form['FirstName'] = account['FirstName']
                    form['LastName'] = account['LastName']
                    form['Nickname'] = account['Nickname']
                    form['Email'] = account['Email']
                    form['Tel'] = account['Tel']
                    form['Tag'] = account['Tag']
                    form['Love'] = account['Love'].split(",")
                    form['Checkin'] = account['Checkin']
                    form['Favorite'] = account['Favorite']
                    form['Role'] = account['Role']
                    form['Picture'] = account['Picture'].decode("utf-8")
                    form['msg'] = 'Logged in successfully!'
                else:
                    form['msg'] = 'Incorrect password!'
            else:
                # Account doesnt exist or username/password incorrect
                form['msg'] = 'Incorrect Username'
    # Show the login form with message (if any)
        else:
            form['msg'] = 'Please fill out the form!'
        # print(form)
        return jsonify(form)

@app.route("/location", methods = ['GET', 'POST'])
@cross_origin()
def location():
    if request.method == 'POST':
        content = request.get_json()
        if content["query"] == "":
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            print(content["current"])
            if int(content["current"]) < 10:
                cursor.execute('SELECT keyID,nameTH,provinceTH,coordinate,latitude,longitude,typeTH,descriptionTH,pictureURL,phoneNumber,website,ownerID,isVerify,Username FROM Atrip_Places INNER JOIN Atrip_Users where Atrip_Places.ownerID = Atrip_Users.ID ORDER BY keyID LIMIT 10')
            else:
                cursor.execute('SELECT keyID,nameTH,provinceTH,coordinate,latitude,longitude,typeTH,descriptionTH,pictureURL,phoneNumber,website,ownerID,isVerify,Username FROM Atrip_Places INNER JOIN Atrip_Users where Atrip_Places.ownerID = Atrip_Users.ID ORDER BY keyID LIMIT %s',[content["current"]])
            account = cursor.fetchall()
            for i in range(0,len(account),1):
                account[i]["pictureURL"] = account[i]["pictureURL"].decode("utf-8")
            # print(account[i])
    return jsonify(account)

@app.route("/approvelocation", methods = ['GET', 'POST'])
@cross_origin()
def approvelocation():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT keyID,nameTH,provinceTH,coordinate,latitude,longitude,typeTH,descriptionTH,pictureURL,phoneNumber,website,ownerID,isVerify,Username FROM Atrip_Places INNER JOIN Atrip_Users where Atrip_Places.ownerID = Atrip_Users.ID and isVerify = 0 ORDER BY keyID')
        account = cursor.fetchall()
        for i in range(0,len(account),1):
            account[i]["pictureURL"] = account[i]["pictureURL"].decode("utf-8")

        return jsonify(account)
    return jsonify({"msg" : "Error"})

@app.route("/validate", methods = ['GET', 'POST'])
@cross_origin()
def validate():
    if request.method == 'POST':
        content = request.get_json()
        if (content["status"] == 0):
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('Delete from Atrip_Places where keyID = %s',[content["key"]])
            mysql.connection.commit()
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('Update Atrip_Places set isVerify = 1 where keyID = %s',[content["key"]])
            mysql.connection.commit()
    return jsonify({"msg" : "success"})

@app.route("/saveTrip", methods = ['GET', 'POST'])
@cross_origin()
def saveTrip():
    if request.method == 'POST':
        content = request.get_json()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT Favorite from Atrip_Users where ID = %s",[content["id"]])
        account = cursor.fetchone()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT ownerID from Atrip_Trips where keyID = %s",[content["key"]])
        check = cursor.fetchone()
        print(check,content["id"])
        if (str(check["ownerID"]) == str(content["id"])):
            return jsonify({"msg" : "You can't choose your trip as favorite"})
        # print(content)
        # print(account)
        if (account["Favorite"]):
            # print("Enter")
            favorite = account["Favorite"].split(",")
            # print(favorite)
            if str(content['key']) in favorite:
                return jsonify({"msg" : "Already has Data"})
            account["Favorite"] = account["Favorite"] + "," + str(content['key'])
            cursor.execute('Update Atrip_Users set Favorite = %s where ID = %s',(account["Favorite"],content["id"]))
            mysql.connection.commit()
            return jsonify({"msg" : "success"})
        cursor.execute('Update Atrip_Users set Favorite = %s where ID = %s',(content['key'],content["id"]))
        mysql.connection.commit()
        return jsonify({"msg" : "success"})

@app.route("/likeTrip", methods = ['GET', 'POST'])
@cross_origin()
def likeTrip():
    if request.method == 'POST':
        content = request.get_json()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT Love from Atrip_Users where ID = %s",[content["id"]])
        account = cursor.fetchone()
        if (account["Love"]):
            favorite = account["Love"].split(",")
            if str(content['key']) in favorite:
                love = account["Love"].split(",")
                love.remove(str(content["key"]))
                love = ",".join(love)
                cursor.execute('Update Atrip_Users set Love = %s where ID = %s',(love,content["id"]))
                mysql.connection.commit()
                cursor.execute('Update Atrip_Trips set Love = Love-1 where keyID = %s',[content["key"]])
                mysql.connection.commit()
                return jsonify({"msg" : "success","love" : love.split(",")})
            account["Love"] = account["Love"] + "," + str(content['key'])
            cursor.execute('Update Atrip_Users set Love = %s where ID = %s',(account["Love"],content["id"]))
            mysql.connection.commit()
            cursor.execute('Update Atrip_Trips set Love = Love+1 where keyID = %s',[content["key"]])
            mysql.connection.commit()
            return jsonify({"msg" : "success","love" : account["Love"].split(",")})
        cursor.execute('Update Atrip_Users set Love = %s where ID = %s',(content['key'],content["id"]))
        mysql.connection.commit()
        cursor.execute('Update Atrip_Trips set Love = Love+1 where keyID = %s',[content["key"]])
        mysql.connection.commit()
        return jsonify({"msg" : "success","love" : [int(content['key'])]})



@app.route("/trip", methods = ['GET', 'POST'])
@cross_origin()
def trip():
    if request.method == 'POST':
        content = request.get_json()
        if content["query"] == "":
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT keyID,nameTH,numPlace,placeList,ownerID,provinceTH_List,Username,image,Atrip_Trips.Love FROM Atrip_Trips INNER JOIN Atrip_Users on Atrip_Trips.ownerID = Atrip_Users.ID where status = "สาธารณะ" ORDER BY keyID')
            account = cursor.fetchall()
            for i in range(0,len(account),1):
                account[i]["image"] = account[i]["image"].decode("utf-8")

    return jsonify(account)

@app.route("/province", methods = ['GET'])
@cross_origin()
def province():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Atrip_Provinces ORDER BY keyID')
        account = cursor.fetchall()
        # print(account)
    return jsonify(account)

@app.route("/tripInfo/<keyID>", methods = ['GET','POST'])
@cross_origin()
def tripInfo(keyID):
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT keyID,nameTH,numPlace,placeList,ownerID,provinceTH_List,Username,description,status FROM Atrip_Trips INNER JOIN Atrip_Users where (Atrip_Trips.ownerID = Atrip_Users.ID) and keyID = %s',[keyID])
        account = cursor.fetchall()
        return jsonify(account)
    elif request.method == 'POST':
        content = request.get_json()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('Update Atrip_Trips set description = %s,status = %s where keyID = %s',(content["description"],content["status"],keyID))
        mysql.connection.commit()
        return jsonify({"msg" : "success"})


@app.route("/placeInfo/<keyID>", methods = ['GET'])
@cross_origin()
def placeInfo(keyID):
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT keyID,nameTH,provinceTH,coordinate,latitude,longitude,typeTH,descriptionTH,pictureURL,phoneNumber,website,ownerID,isVerify,Username FROM Atrip_Places INNER JOIN Atrip_Users where (Atrip_Places.ownerID = Atrip_Users.ID) and (keyID = %s)',[keyID])
        account = cursor.fetchall()
        for i in range(0,len(account),1):
            account[i]["pictureURL"] = account[i]["pictureURL"].decode("utf-8")
        # print(account)
    return jsonify(account)


@app.route("/getPlace", methods = ['GET', 'POST'])
@cross_origin()
def getPlace():
    if request.method == 'POST':
        content = request.get_json()
        # print(content["place"])
        # print(len(content["place"]))
        if content["place"]:
            contentinput = content["place"].split(",")
            # print(contentinput)
            form = "SELECT keyID,nameTH,provinceTH,coordinate,latitude,longitude,typeTH,descriptionTH,pictureURL,phoneNumber,website,ownerID,isVerify,Username,CASE keyID "#FROM Atrip_Places INNER JOIN Atrip_Users where (Atrip_Places.ownerID = Atrip_Users.ID) and (keyID = " + " or keyID = ".join(contentinput) + ")" + " order by case keyID"
            for i in range(0,len(contentinput),1):
                form = form + " WHEN " + contentinput[i] + " THEN " + str(i+1)
            form = form + " END AS sortOrder FROM Atrip_Places INNER JOIN Atrip_Users where (Atrip_Places.ownerID = Atrip_Users.ID) and (keyID = " + " or keyID = ".join(contentinput) + ")" + " order by sortOrder"
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(form)
            account = cursor.fetchall()
            for i in range(0,len(account),1):
                account[i]["pictureURL"] = account[i]["pictureURL"].decode("utf-8")
            return jsonify(account)
        else:
            return jsonify(Testform)

@app.route("/getTrip", methods = ['GET', 'POST'])
@cross_origin()
def getTrip():
    if request.method == 'POST':
        content = request.get_json()
        # print(content["trip"])
        # print(len(content["trip"]))
        if content["trip"]:
            contentinput = content["trip"].split(",")
            form = "SELECT * FROM Atrip_Trips WHERE keyID = " + " or keyID = ".join(contentinput)
            # print(form)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(form)
            account = cursor.fetchall()
            return jsonify(account)
        else:
            return jsonify(Testform)

@app.route("/addLocation", methods = ['GET', 'POST'])
@cross_origin()
def addLocation():
    form = {"isSuccess" : False , "msg" : ""}
    if request.method == 'POST':
        content = request.get_json()
        # print(content)
        if content["placeName"]:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT nameTH FROM Atrip_Places WHERE nameTH = %s',[content["placeName"]])
            account = cursor.fetchone()
            if account:
                # print("enter")
                form["isSuccess"] = False
                form["msg"] = "Already have data"
            else:
                cursor.execute('INSERT INTO Atrip_Places (website,phoneNumber,nameTH,provinceTH,descriptionTH,pictureURL,latitude,longitude,coordinate,ownerID,typeTH) VALUES (%s, %s, %s, %s, %s ,%s,%s,%s,%s ,%s,%s)', (content["website"], content["phone"], content["placeName"],content["province"],content["description"],content["image"],content["latitude"],content["longtitude"],str(content["latitude"])+", "+str(content["longtitude"]),content["User"],content["type"]))
                mysql.connection.commit()
                form["isSuccess"] = True
                form["msg"] = "Successfully add to database"
            return jsonify(form)
        else:
            form["msg"] = "Error no PlaceName :d"
            return jsonify(form)

@app.route("/makeTrip", methods = ['GET', 'POST'])
@cross_origin()
def makeTrip():
    form = {"isSuccess" : False , "msg" : ""}
    if request.method == 'POST':
        content = request.get_json()
        # print(content)
        if content['userID'] and content["tripName"] and content["placesInTrip"]:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * from Atrip_Trips where nameTH = %s",[content['tripName']])
            check = cursor.fetchone()
            if (check):
                form["msg"] = "This name already exists"
                return jsonify(form)
            key = ""
            for i in range(0,len(content["placesInTrip"]),1):
                key = key + str(content["placesInTrip"][i]["keyID"]) + ","
            key = key[0:len(key)-1]
            qkey = key.split(",")
            sqlform = "SELECT DISTINCT provinceTH FROM Atrip_Places WHERE keyID = " + " or keyID = ".join(qkey)
            cursor.execute(sqlform)
            account = cursor.fetchall()
            # print(account)
            sqlprovince = ""
            for i in range(len(account)):
                sqlprovince = sqlprovince + account[i]["provinceTH"] + ","
            sqlprovince = sqlprovince[0:len(sqlprovince)-1]
            cursor.execute("SELECT pictureURL from Atrip_Places where keyID = %s",[qkey[0]])
            image = cursor.fetchone()
            cursor.execute('INSERT INTO Atrip_Trips (nameTH,placeList,provinceTH_List,ownerID,numPlace,image) VALUES (%s, %s, %s, %s,%s, %s)', (content['tripName'],key,sqlprovince,content["userID"],len(qkey),image["pictureURL"]))
            mysql.connection.commit()
            form["isSuccess"] = True
            form["msg"] = "Successfully add to database"
            return jsonify(form)
        else:
            form["msg"] = "Error"
            return jsonify(form)

@app.route("/myTrip", methods = ['GET', 'POST'])
@cross_origin()
def myTrip():
    if request.method == 'POST':
        content = request.get_json()
        # print(content)
        if content["query"] == "":
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT Favorite From Atrip_Users where id = %s",[content["id"]])
            account = cursor.fetchone()
            favorite = account["Favorite"].split(",")
            form = "SELECT keyID,nameTH,numPlace,placeList,ownerID,provinceTH_List,Username,image,status FROM Atrip_Trips INNER JOIN Atrip_Users On (Atrip_Trips.ownerID = Atrip_Users.ID) where (ownerID = " + str(content["id"]) + " or keyID = " + " or keyID = ".join(favorite) + ") ORDER BY keyID"
            print(form)
            cursor.execute(form)
            data = list(cursor.fetchall())
            for i in range(0,len(data),1):
                placeList = data[i]["placeList"].split(",")
                form = "SELECT nameTH FROM Atrip_Places WHERE keyID = " + " or keyID = ".join(placeList)
                cursor.execute(form)
                placeList = list(cursor.fetchall())
                placename = ""
                for j in placeList:
                    placename = placename + j["nameTH"] + ","
                placename = placename[0:len(placename)-1]
                data[i]["placeList"] = placename
                data[i]["image"] = data[i]["image"].decode("utf-8")
            # print(data)

    return jsonify(data)

@app.route("/deleteTrip", methods = ['GET', 'POST'])
@cross_origin()
def deleteTrip():
    if request.method == 'POST':
        content = request.get_json()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT ownerID from Atrip_Trips where keyID = %s",[content["keyID"]])
        check = cursor.fetchone()
        if (str(check["ownerID"]) == str(content["id"])):
            cursor.execute('Delete from Atrip_Trips where keyID = %s',[content["keyID"]])
            mysql.connection.commit()
            return jsonify({"msg" : "Success remove Trip"})
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT Favorite from Atrip_Users where ID = %s",[content["id"]])
            account = cursor.fetchone()
            favorite = account["Favorite"].split(",")
            favorite.remove(str(content["keyID"]))
            favorite = ",".join(favorite)
            cursor.execute('Update Atrip_Users set Favorite = %s where ID = %s',(favorite,content["id"]))
            mysql.connection.commit()
            return jsonify({"msg" : "Success remove from favorite"})

@app.route("/makeRoute", methods = ['GET', 'POST'])
@cross_origin()
def makeRoute():
    if request.method == 'POST':
        content = request.get_json()
        numPlace = len(content["placesInTrip"])
        placeIDList = list()
        coordinateList = list()
        for i in range(numPlace):
            placeIDList.append(content["placesInTrip"][i]["keyID"])
            coordinateList.append(content["placesInTrip"][i]["coordinate"])
        results = dict()
        x = gmaps.distance_matrix(coordinateList,coordinateList,mode='driving')
        temp = sortResult(allResults(placeIDList,x))
        results["results"] = temp[0]
        count = 0
        for i in temp:
            if i[0][0] == placeIDList[0]:
                break
            count += 1
        results["results1"] = temp[count]
        print(results)

    return jsonify(results)


@app.route("/forgotpassword", methods = ['GET', 'POST'])
@cross_origin()
def forgotpassword():
    if request.method == 'POST':
        content = request.get_json()
        print(content)
        if content["email"] and content["birthday"]:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('select Date,Username from Atrip_Users where email = %s',[content["email"]])
            account = cursor.fetchone()
            if (account):
                if (account["Date"] == content["birthday"]):
                    randompassword = ''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(8)))
                    print(randompassword)
                    salt = bcrypt.gensalt()
                    cursor.execute('Update Atrip_Users set Password = %s where Username = %s',(bcrypt.hashpw(randompassword.encode('utf8'), salt),account["Username"]))
                    mysql.connection.commit()
                    port = 587  # For starttls
                    msg = MIMEMultipart()
                    msg['From'] = 'softdevprojectsdp@gmail.com'
                    msg['To'] = content["email"]
                    msg['Subject'] = 'ATrip Forgetpassword'
                    smtp_server = "smtp.gmail.com"
                    sender_email = "softdevprojectsdp@gmail.com"
                    receiver_email = content["email"]
                    password = "SDP12345"
                    message = "Your Username is " + account["Username"] + """
Your Password is """ + randompassword
                    msg.attach(MIMEText(message,"plain"))
                    context = ssl.create_default_context()
                    with smtplib.SMTP(smtp_server, port) as server:
                        server.ehlo()  # Can be omitted
                        server.starttls(context=context)
                        server.ehlo()  # Can be omitted
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, msg.as_string())


    return jsonify({"msg" : "สำเร็จ กรุณาตรวจสอบ Email ของท่าน"})


if __name__ == '__main__':
    gmaps = googlemaps.Client(key='AIzaSyCIHRdrSY885ctMMj_cvL-Ga69IktvnLs0')
    app.run(host="0.0.0.0", port=34673, debug=True)
