#---PYTHON LIBRARIES FOR IMPORT--------------------------------------
import uuid, sys, logging, math, time, os, re
from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify
from flask_cors import CORS #Needs to be installed to allow cross origin
from databaseinterface import Database
from datetime import datetime
import requests #needed for an external API
import globalvars
import helpers

#---CONFIGURE APP---------------------------------------------------#
sys.tracebacklimit = 2 #Level of python traceback - useful for reducing error text
app = Flask(__name__) #Creates the Flask Server Object
app.config.from_object('config.Config')
CORS(app) #enables cross domain scripting protection

#---CONFIGURE DATABASE-----------------------------------------#
DATABASE = Database('/home/nielbrad/mysite/test.sqlite', app.logger)
#DATABASE = Database('test.sqlite', app.logger)
globalvars.DATABASE = DATABASE #store DATABASE globally

#---VIEW FUNCTIONS---------------------------------------------#
@app.route('/externalapi', methods=['GET','POST'])
def externalweatherapi():
    data = None
    #INSERT PYTHON REQUESTS CODE TO GET API DATA
    return jsonify(data)

# get a list of the recent users
@app.route('/getactiveusers', methods=['GET','POST'])
def getactiveusers():
    activeusers = None
    if 'userid' in session:
        helpers.update_access(session['userid']) #calls my custom helper function
    fmt = "%d/%m/%Y %H:%M:%S"
    users = DATABASE.ViewQuery("SELECT username, lastaccess from users")
    activeusers = [] #blank list
    for user in users:
        if user['lastaccess']:
            td = datetime.now() - datetime.strptime(user['lastaccess'],fmt)
            if td.seconds < 120:
                activeusers.append(user['username']) #makes a list of names
    return jsonify({'activeusers':activeusers}) #list of users

# login
@app.route('/ajaxlogin', methods=['GET','POST'])
def ajaxlogin():
    data = {}
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        userdetails = DATABASE.ViewQuery("SELECT * FROM users WHERE email = ? AND password = ?",(email,password))
        app.logger.info(userdetails) #log the user details to check its working
        if userdetails:
            row = userdetails[0] #userdetails is a list of dictionaries
            helpers.update_access(row['userid']) #calls my custom helper function
            data['success'] = True
            data['userid'] = row['userid']
            data['username'] = row['username']
            data['permission'] = row['permission']
        else:
            data['success'] = False
    return jsonify(data)

#main method called web server application
if __name__ == '__main__':
    app.run() #PYTHON ANYTWHERE!!! will decide the port
    #app.run(host='0.0.0.0', port=5000) #runs a local server on port 5000