import mysql.connector
from dbConnect import connect
from Kunci import Kunci
import json

class DatabaseKunci():

    @classmethod
    def getLastkunci(self):
        try:
            mydb =connect()
            mycursor = mydb.cursor()

            # fetch the sentence from database server
            mycursor.execute("SELECT * FROM kunci ORDER BY id_kunci desc LIMIT 1")
            myresult = mycursor.fetchall()

            for row in myresult:
                id = int(row[0])
                kunci = row[1]
                time = row[2]

            obj_kunci = Kunci(id, kunci, time)
            obj_kunci.display()
            jsondata = obj_kunci.to_dict_set()
            jsdata = json.dumps(jsondata, indent=4, sort_keys=True, default=str)
            js_data = json.loads(jsdata)
            return js_data

        except mysql.connector.Error as error:
            mydb.rollback()  # rollback if any exception occured
            print("Failed Selecting record from python_users table {}".format(error))
        finally:
            # closing database connection.
            if (mydb.is_connected()):
                mycursor.close()
                mydb.close()
               # print("MySQL connection is closed")


    @classmethod
    def getKunci(self,id):
        try:
            mydb =connect()
            mycursor = mydb.cursor()

            # fetch the sentence from database server
            mycursor.execute(f"SELECT jap_kunci FROM kunci where id_kunci={id}")
            myresult = mycursor.fetchall()

            for row in myresult:
                #id = int(row[0])
                kunci = row[0]
                #time = row[2]

            #obj_sentence = Sentence(id, sentence, time)
            #obj_sentence.display()
            #jsondata = obj_sentence.to_dict_set()
            #jsdata = json.dumps(jsondata, indent=4, sort_keys=True, default=str)
            #js_data = json.loads(jsdata)
            return kunci

        except mysql.connector.Error as error:
            mydb.rollback()  # rollback if any exception occured
            print("Failed Selecting record from python_users table {}".format(error))
        finally:
            # closing database connection.
            if (mydb.is_connected()):
                mycursor.close()
                mydb.close()
                print("MySQL connection is closed")


    @classmethod
    def addKunci(self,kunci):
        try:
            kunci
            mydb =connect()
            mycursor = mydb.cursor()

            # fetch the sentence from database server
            mycursor.execute(f"INSERT INTO kunci(jap_kunci) values (\"{kunci}\") ")

            mydb.commit()
            print("Record inserted successfully into python_users table")
            result = 'true'

        except mysql.connector.Error as error:
            mydb.rollback()  # rollback if any exception occured
            print("Failed inserting record into python_users table {}".format(error))
            result='false'
        finally:
            # closing database connection.
            if (mydb.is_connected()):
                mycursor.close()
                mydb.close()
                print("MySQL connection is closed")
            return result

    @classmethod
    def removeKunci(self, id_str):
        try:
            id = int(id_str)
            mydb =connect()
            mycursor = mydb.cursor()
            # fetch the sentence from database server
            mycursor.execute(f"DELETE FROM kunci WHERE  id_kunci=({id})")

            mydb.commit()
            print(f"Row with id={id} deleted successfully")
            result = 'true'

        except mysql.connector.Error as error:
            mydb.rollback()  # rollback if any exception occured
            print("Failed delete row from sentence table {}".format(error))
            result = 'false'
        finally:
            # closing database connection.
            if (mydb.is_connected()):
                mycursor.close()
                mydb.close()
                #print("MySQL connection is closed")
            return result

    @classmethod
    def getKuncis(self,number):
        try:
            list_kunci = []
            mydb =connect()
            mycursor = mydb.cursor()

            # fetch the sentence from database server
            mycursor.execute(f"SELECT id_kunci,jap_kunci,last_update FROM kunci ORDER BY id_kunci asc LIMIT {number} ")
            myresult = mycursor.fetchall()

            for row in myresult:
                list_kunci.append(Kunci(row[0], row[1], row[2]))

            json_listkunci = [obj.to_dict_set() for obj in list_kunci]
            jsdata = json.dumps({"list_sentence": json_listkunci}, indent=4, sort_keys=True, default=str)
            jsdataj = json.loads(jsdata)
            return jsdataj

        except mysql.connector.Error as error:
            mydb.rollback()  # rollback if any exception occured
            print("Failed Selecting record from python_users table {}".format(error))
            jsdataj = 'NULL'
        finally:
            # closing database connection.
            if (mydb.is_connected()):
                mycursor.close()
                mydb.close()
                #print("MySQL connection is closed")



