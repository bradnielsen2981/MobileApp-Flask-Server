#---PYTHON LIBRARIES FOR IMPORT--------------------------------------
import uuid, sys, logging, math, time, os, re
from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify
from flask_cors import CORS #Needs to be installed to allow cross origin
#from databaseinterface import Database
from datetime import datetime
import requests #needed for an external API
#import globalvars
#import helpers

#---CONFIGURE APP---------------------------------------------------#
sys.tracebacklimit = 2 #Level of python traceback - useful for reducing error text
app = Flask(__name__) #Creates the Flask Server Object
#DELETE config from object
CORS(app) #enables cross domain scripting protection

@app.route('/', methods=['GET','POST'])
def login():
    return "Hello from Flask"

#main method called web server application
if __name__ == '__main__':
    app.run() #PYTHON ANYTWHERE!!! will decide the port
    #app.run(host='0.0.0.0', port=5000) #runs a local server on port 5000

