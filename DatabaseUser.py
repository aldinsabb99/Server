import mysql.connector
from dbConnect import connect
from User import User
import json
import datetime

class DatabaseUser:

    @classmethod
    def getuser(self, username, passw):
        try:
            mydb = connect()
            mycursor = mydb.cursor()

            # fetch the sentence from database server
            mycursor.execute("SELECT * FROM user where username=%s AND password=%s",(username, passw))
            myresult = mycursor.fetchall()

            for row in myresult:
                id = int(row[0])
                roles = row[1]
                name = row[2]
                username = row[3]
                passw = row[4]
                time = row[5]


            obj_user = User(id, roles, name, username, passw, time)
            jsondata = obj_user.to_dict_set()
            jsdata = json.dumps(jsondata, indent=4, sort_keys=True, default=str)
            js_data = json.loads(jsdata)

        except Exception as error:
            mydb.rollback()  # rollback if any exception occured
            print("Failed Selecting record from python_users table {}".format(error))
        finally:
            # closing database connection.
            if (mydb.is_connected()):
                mycursor.close()
                mydb.close()
                #print("MySQL connection is closed")
                return (js_data)

    @classmethod
    def getuserid(self, id):
        try:
            username=""
            passw=""
            roles = ""
            time = ""
            js_data = ""
            name = ""
            mydb =connect()
            mycursor = mydb.cursor()

            # fetch the sentence from database server
            mycursor.execute("SELECT * FROM user where id_user= %s" % id)
            myresult = mycursor.fetchall()

            for row in myresult:
                id = int(row[0])
                roles = row[1]
                name = row [2]
                username = row[3]
                passw = row[4]
                time = row[5]

            obj_user = User(id, roles, name, username, passw, time)
            jsondata = obj_user.to_dict_set()
            jsdata = json.dumps(jsondata, indent=4, sort_keys=True, default=str)
            js_data = json.loads(jsdata)

        except mysql.connector.Error as error:
            mydb.rollback()  # rollback if any exception occured
            print("Failed Selecting record from python_users table {}".format(error))
        finally:
            # closing database connection.
            if (mydb.is_connected()):
                mycursor.close()
                mydb.close()
                #print("MySQL connection is closed")
                return (js_data)

    @classmethod
    def adduser(self,name, username, password):
        try:
            status="false"
            mydb =connect()
            mycursor = mydb.cursor()

            # fetch the sentence from database server
            mycursor.execute("INSERT INTO `user`(`name`, `username`, `password`) values ('%s', '%s', MD5('%s'))",(name, username, password))
            print("udah sampe sini")
            mydb.commit()
            status="true"

        except mysql.connector.Error as error:
            mydb.rollback()  # rollback if any exception occured
            print("Failed Adding record from user table {}".format(error))
        finally:
            # closing database connection.
            if (mydb.is_connected()):
                mycursor.close()
                mydb.close()
                #print("MySQL connection is closed")
                return (status)

    @classmethod
    def updateTime(self,id):
        try:
            time = datetime.datetime.now()
            status="false"
            mydb =connect()
            mycursor = mydb.cursor()

            # fetch the sentence from database server
            mycursor.execute(f"UPDATE user SET last_login=%s WHERE id_user=%s",(time,id))
            mydb.commit()
            status="true"

        except mysql.connector.Error as error:
            mydb.rollback()  # rollback if any exception occured
            print("Failed Updating record from user table {}".format(error))
        finally:
            # closing database connection.
            if (mydb.is_connected()):
                mycursor.close()
                mydb.close()
                #print("MySQL connection is closed")
                return (status)


#print(DatabaseUser.getuser("Gifari","12345"))
