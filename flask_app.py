#---PYTHON LIBRARIES FOR IMPORT--------------------------------------
import uuid, sys, logging, math, time, os, re
from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify
from flask_cors import CORS #Needs to be installed to allow cross origin
from databaseinterface import Database
from datetime import datetime
import requests #needed for an external API
import helpers

#---CONFIGURE APP---------------------------------------------------#
sys.tracebacklimit = 2 #Level of python traceback - useful for reducing error text
app = Flask(__name__) #Creates the Flask Server Object
#DELETE config from object
CORS(app) #enables cross domain scripting protection

# LOGIN SCRIPT
@app.route('/login', methods=['GET','POST'])
def login():
    log("Login")
    data = { "success":False, "message":"Login unsuccessful"}
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        userdetails = DATABASE.ViewQuery("SELECT * FROM users WHERE email = ?", (email,))
        app.logger.info(userdetails)
        if userdetails:
            user = userdetails[0]
            data = { "success":True, "message":"Login successful"}
            data['userid'] = user['userid']
            # session['userid'] = user['userid']
            data['permission'] = user['permission']
            data['name'] = user['name']
    return jsonify(data) #returns the data to the app

#main method called web server application
if __name__ == '__main__':
    app.run() #PYTHON ANYTWHERE!!! will decide the port
    #app.run(host='0.0.0.0', port=5000) #runs a local server on port 5000

