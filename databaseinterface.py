#----------------------------------------------------------------------------
# This Database class provides an interface to the database
# It's therefore easier to simply inherit the code..
# Created by Brad Nielsen 2019
#-----------------------------------------------------------------------#
import sqlite3
import logging
import sys

class Database:

    def __init__(self, location="", log = logging.getLogger(__name__)):
        self.location = location
        self.logger = log
        return

    # Returns a handle to the Database connection
    def connect(self):
        connection = sqlite3.connect(self.location)
        connection.row_factory = sqlite3.Row #configures database queries to return a list of dictionaries (each row/record) [{"field1":value1,"field2":value2...},{etc},{} ]
        return connection

    # A helper function to save time and also log sql errors
    # Write your Select Query, and pass in a Tuple (a,b,c etc) representing any parameters
    def ViewQuery(self, query, params=None):
        connection = self.connect()
        result = None
        try:
            if params:
                cursor = connection.execute(query, params)
            else:
                cursor = connection.execute(query)
            result = cursor.fetchall() #returns a list of dictionaries
        except (sqlite3.OperationalError, sqlite3.Warning, sqlite3.Error) as e:
            self.logger.error("DATABASE ERROR: %s" % e)
            self.logger.error(query)
        connection.close()
        if result:
            return ([dict(row) for row in result]) #a list of dictionaries
        else:
            return False

    # Created a helper function so to save time and also log results
    # Write your DELETE, INSERT, UPDATE Query, and pass in a Tuple(a,b,c etc ) representing any parameters
    def ModifyQuery(self, query, params=None):
        connection = self.connect()
        result = None
        try:
            if params:
                connection.execute(query, params)
            else:
                connection.execute(query)
            result = True
        except (sqlite3.OperationalError, sqlite3.Warning, sqlite3.Error) as e:
            self.logger.error("DATABASE ERROR: %s" % e)
            self.logger.error(query)
            result = False
        connection.commit()
        connection.close()
        return result #Should be a true or false depending on success??

    def log(self, message):
        self.logger.info(message)
        return

    def log_error(self, error):
        self.logger.error(error)
        return

#only execute the below block if this is the execution point
if __name__ == '__main__':
    database = Database("test.sqlite")
    results = database.ViewQuery("SELECT * FROM users")
    print(results)