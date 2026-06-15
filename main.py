from flask import Flask, render_template, request, session,redirect, url_for
from datetime import datetime
import sqlite3
import requests
from requests.auth import HTTPBasicAuth
import psycopg2
import os
app = Flask(__name__)

#route for Home/main page -Tess
@app.route("/")
def home():
    return render_template("home.html")

#route for login page -Tess
@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

#route for signup page -Tess
@app.route("/signup")
def signup():
    return render_template("signup.html")

# this key is for session
app.secret_key="skji34n9*&^&"
# this url is for database 
DATABASE_URL="postgresql://postgres.wleqkhsiftorujqponph:CproProjectJklonme@aws-1-us-west-2.pooler.supabase.com:5432/postgres"

# this is the function that create the connection with data
# we should call this function each time we want to fetch data or store or update or delete data
def cursor_():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    return conn, cursor

#this route leads to the file page where you can write a note or read it
# run the code and add to the link /file/4 or 5 or 6 or 7 or 8 (each number is the id of a file)
@app.route("/file/<int:id>")
def file(id):
    # this sessions should be in login or sign in route , we will remove it later
    session["user_name"] = "userName" # usually we will add here the user name
    session["id"] = 7 # also here we will add the user id but I put 7 since the only user we have has id 7


    if"user_name" in session:
        # Here I called the connection function to fetch data
        conn, cursor = cursor_()

        cursor.execute("""
        SELECT * FROM files WHERE id=%s
        """, (id,))
        data = cursor.fetchone()

        # here we confirm the changes and close the connection
        conn.commit()
        conn.close()
        if data:
            return render_template("file.html", file_data = data)
        else:
            return "No data" # I will update this later
    else:
        return "Not" # I will update this later
    

# this route is for saving the changes that the user made on their file
@app.route("/save", methods=["POST"])
def save():
    conn, cursor = cursor_()

    file_content = request.form["file_content"]
    file_id = request.form["file_id"]
    cursor.execute("""
    UPDATE files SET file_content = %s WHERE id = %s
    """,(file_content, file_id))
    
    conn.commit()
    conn.close()

    return redirect(f"/file/{file_id}")

if __name__ == "__main__":
    app.run(debug = True)

