from flask import Flask, render_template, request, session,redirect, url_for, flash
from datetime import datetime
import sqlite3
import requests
from sqlalchemy import create_engine, text
from checkAccess import checkAccess  # this has a decorate function come from the file checkAccess. It is responsible to check if the user loged in  -sherman

app = Flask(__name__)

# this key is for session -sherman
app.secret_key="skji34n9*&^&"
# this url is for database  -sherman
DATABASE_URL="postgresql://neondb_owner:npg_19ZgXruOMpIP@ep-ancient-shape-ahwx4plg-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"


# create the engine -sherman
engine = create_engine(DATABASE_URL)





#route for Home/main page -Tess
@app.route("/")
def home():
    return render_template("home.html")


# route for dashbboard page -Sherman
@app.route("/dashboard")
@checkAccess # this is a decorate function come from the file checkAccess. It is responsible to check if the user loged in  -sherman
def dashboard():
    with engine.begin() as conn:
        respons = conn.execute(text("""
SELECT * FROM files WHERE user_id = :user_id
"""),{
    "user_id":session["id"]
})
    data = list(respons.mappings().fetchall())
    

    return render_template("dashboard.html", data = data)



#route for login page -Tess
@app.route("/login", methods=["GET", "POST"])
def login(message = ""):
    if request.method == "POST":
        email = request.form["email"] 
        password = request.form["password"]
        # store the email and password in a list to check if they are empty or not
        datalist = [email, password]
        # check if the email is valid or not
        if  "@" not in email or "." not in email.split("@")[1]:
                datalist.append("invalidEmail...")
        # check if the email and password are the only two items in the list without any other messages and also check if they are not empty, if all these conditions are true then we will check the database for the user
        if len(datalist) == 2 and email.strip()!= "" and password.strip() !="":
            with engine.begin() as conn:
                response = conn.execute(text("""
    SELECT * FROM users WHERE email= :email AND password= :password
    """),{
        "email":email,
        "password":password
    })      
                

            row = response.mappings().first()


            # here we check if the row is not empty,which means the user exist in the database and the email and password are correct
            if row:
                data = dict(row)
                session["username"] = data["username"]
                session["id"] = data["id"]
                # here should return dashboard route - sherman
                return redirect(url_for('dashboard'))
            
            # if the row is empty, which means the user does not exist in the database or the email and password are incorrect,
            else:
                # if the email and password are not empty but the the email and password are incorrect, we will add a message to the list to shows the user that the email or password is incorrect
                datalist.append("wrongEntry")
                return render_template("login.html", message=datalist)
            

        # if email or password are empty or if the email is invalid we will pass a message 
        else:
            return render_template("login.html", message=datalist)

    else:
        return render_template("login.html")

#route for signup page -Tess
@app.route("/signup", methods = ["GET", "POST"])
def signup(message = ""):
    
    if request.method == "POST":
        email = request.form["email"] 
        username = request.form["username"]
        password = request.form["password"]
        confirmpassword = request.form["confirmpassword"]

         # ## INPUT VALIDAION CODES STARTS ###
        # chech if all inputs are not empty
        dataList = [email, username, password, confirmpassword]

        if email.strip() !="" or username.strip()!= "":

            with engine.begin() as conn:
                response = conn.execute(text("""
SELECT * FROM users WHERE email= :email OR username= :username
"""),{
    "email": email,
    "username": username
                })
            rows = response.mappings().all()
            data = [dict(row) for row in rows]
            # Here I ask if any of the emails in the rows equals to the email that the user just entered to sign up, so if True eamil already exist

            if any(rowData["email"] == email for rowData in data):
                dataList.append("existedEmail")
            # the same thing here
            if any(rowData["username"] == username for rowData in data):
                dataList.append("existedUsername")
            
       
        if "@" not in email or "." not in email.split("@")[1]:
            dataList.append("invalidEmail")
        if password != confirmpassword:
            dataList.append("wrongConfirm")


        # here i am checking if all fields in the form is not empty (empty string return false), so if one is false so don't continue
        # also I added checking for the length of the datalist if it is more than 4 (which is the number of the fields in the form) so that means there is at least one message for the user
        if not all(inputs.strip() for inputs in dataList) or len(dataList) > 4:
            # if one is empty return the dataList to the the sinup page 
            return render_template("signup.html", message=dataList)
        

        # ## INPUT VALIDAION CODES ENDED ###
        
        with engine.begin() as conn:
            conn.execute(text("""
        INSERT INTO users (email, username, password) VALUES (:email, :username, :password)
        """), {
            "email":email,
            "username":username, 
            "password":password
        })
        session["username"] = username
        print(email, username, password) 

        with engine.begin() as conn:
            response = conn.execute(text("""
SELECT * FROM users WHERE username= :username and email= :email
"""),{
        "username" :username,
        "email" : email
            })
            session["id"] = dict(response.mappings().all()[0])["id"]
        # here should return dashboard route - sherman
        return redirect(url_for("dashboard"))

    else:
        return render_template("signup.html")



#this route leads to the file page where you can write a note or read it -sherman
# run the code and add to the link /file/4 or 5 or 6 or 7 or 8 (each number is the id of a file) -sherman
@app.route("/file/<int:id>")
@checkAccess
def file(id):
    # this sessions should be in login or sign in route , we will remove it later


    if"username" in session:
        # open the connection 
        with engine.begin() as conn:
            response = conn.execute(text("""
            SELECT * FROM files WHERE id= :id AND user_id= :user_id
            """), {
                "id" : id,
                "user_id": session["id"]
            })
            row = response.mappings().first()
            if row:
                data = dict(row)
                return render_template("file.html", file_data = data)
            else:
                return "No data" # I will update this later
        

    else:
        return "Not" # I will update this later
    
listR = ['<', '>' ,':', '"', '/', '\\', '|', '?', '*']


#create new File
@app.route("/createFile", methods=["POST"])
def createFile():
    fileName = request.form["fileName"]
    if fileName.strip() == "":
        flash("File name cannot be empty. File creation failed.", "error")
        return redirect(url_for("dashboard"))
    if len(fileName) > 25:
        flash("File name cannot exceed 25 characters. File creation failed.", "error")
        return redirect(url_for("dashboard"))
    if any(char  in listR for char in fileName) :
        flash("File name cannot contain any of the following characters: < > : \" / \\ | ? * . File creation failed.", "error")
        return redirect(url_for("dashboard"))
    nowDate = datetime.now()
    with engine.begin() as conn:
        conn.execute(text("""
INSERT INTO files (file_name, user_id, created_at) VALUES (:file_name, :user_id, :created_at)
"""),{
    "file_name":fileName,
    "user_id" : session["id"],
    "created_at": nowDate
})
    flash("File created successfully.", "success")
    return redirect(url_for("dashboard"))






# this route is for saving the changes that the user made on their file -sherman
@app.route("/updateFile", methods=["POST"])
@checkAccess
def updateFile():

    file_content = request.form["file_content"]
    file_id = request.form["file_id"]
    
    with engine.begin() as conn:
        conn.execute(text("""
UPDATE files SET file_content= :file_content WHERE id= :id
"""), {
    "file_content": file_content,
    "id": file_id
})
    return redirect(f"/file/{file_id}")


@app.route("/delete/<int:id>")
def delete(id):
    with engine.begin() as conn:
        conn.execute(text("""
DELETE FROM files WHERE id= :id
"""),{
    "id" :id
})  
    flash("File deleted successfully.", "success")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug = True)

