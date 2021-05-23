import hashlib, socket
import uuid, sys, logging, math, time, os, re
import globalvars
from datetime import datetime

#-------------Hashing----------------------------#
#for encrypting the password in the database
def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

#for decrypting the password in the database - returns True if correct
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

# updates the users lastaccess in database
def update_access(userid):
    fmt = "%d/%m/%Y %H:%M:%S"
    datenow = datetime.now().strftime(fmt)
    globalvars.DATABASE.ModifyQuery("UPDATE users SET lastaccess = ?, active = 1 where userid = ?",(datenow, userid))
    return



