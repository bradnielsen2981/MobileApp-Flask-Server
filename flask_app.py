#---PYTHON LIBRARIES FOR IMPORT--------------------------------------
import uuid, sys, logging, math, time, os, re
from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from databaseinterface import Database
from datetime import datetime
import requests #needed for an external API
#import helpers
#from bs4 import BeautifulSoup #web scraping - i think this will only work if you have a paid PythonAnywhere account
#from flask_cors import CORS #----------NEEDS TO BE INSTALLED to allow cross origin pip install flask-cors

#THINK ABOUT SECURITY PRECAUTIONS - multifactor authentication, password length, 
# password hashing, CORS, POST vs GET, HTTPS, Restricting upload file types, checking session id, permission

#---CONFIGURE APP---------------------------------------------------#
sys.tracebacklimit = 2 #Level of python traceback - useful for reducing error text
app = Flask(__name__) #Creates the Flask Server Object
DATABASE = Database('/home/nielbrad/mysite/test.sqlite', app.logger)
#CORS(app) #enables cross domain scripting protection - necessary when communicating with the app

# LOGIN SCRIPT
@app.route('/login', methods=['GET','POST'])
def login():
    log("Login")
    data = { "success":False, "message":"Login unsuccessful"}
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        userdetails = DATABASE.ViewQuery("SELECT * FROM users WHERE email = ?", (email,))
        app.logger.info(userdetails) #Log the results 
        if userdetails:
            user = userdetails[0] #only get the first row
            session['userid'] = user['userid'] #save in session
            session['permission'] = user['permission']
            data = { "success":True, "message":"Login successful"}
            data['userid'] = user['userid']
            data['name'] = user['name']
    return jsonify(data) #returns the data to the app in JSON 

#main method called web server application
if __name__ == '__main__':
    app.run() #PYTHON ANYTWHERE!!! will decide the port
    #app.run(host='0.0.0.0', port=5000) #runs a local server on port 5000

