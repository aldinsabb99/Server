import mysql.connector
from dbConnect import connect
from Sentence import Sentence
import json

class DatabaseSentence():

    @classmethod
    def getLastsentence(self):
        try:
            mydb =connect()
            mycursor = mydb.cursor()

            # fetch the sentence from database server
            mycursor.execute("SELECT * FROM sentence ORDER BY id_sentence desc LIMIT 1")
            myresult = mycursor.fetchall()

            for row in myresult:
                id = int(row[0])
                sentence = row[1]
                time = row[2]

            obj_sentence = Sentence(id, sentence, time)
            obj_sentence.display()
            jsondata = obj_sentence.to_dict_set()
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
    def getSentence(self,id):
        try:
            mydb =connect()
            mycursor = mydb.cursor()

            # fetch the sentence from database server
            mycursor.execute(f"SELECT jap_sentence FROM sentence where id_sentence={id}")
            myresult = mycursor.fetchall()

            for row in myresult:
                #id = int(row[0])
                sentence = row[0]
                #time = row[2]

            #obj_sentence = Sentence(id, sentence, time)
            #obj_sentence.display()
            #jsondata = obj_sentence.to_dict_set()
            #jsdata = json.dumps(jsondata, indent=4, sort_keys=True, default=str)
            #js_data = json.loads(jsdata)
            return sentence

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
    def addSentences(self,sentence):
        try:
            sentence
            mydb =connect()
            mycursor = mydb.cursor()

            # fetch the sentence from database server
            mycursor.execute(f"INSERT INTO sentence(jap_sentence) values (\"{sentence}\") ")

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
    def removeSentences(self, id_str):
        try:
            id = int(id_str)
            mydb =connect()
            mycursor = mydb.cursor()
            # fetch the sentence from database server
            mycursor.execute(f"DELETE FROM sentence WHERE  id_sentence=({id})")

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
    def getSentences(self,number):
        try:
            list_sentences = []
            mydb =connect()
            mycursor = mydb.cursor()

            # fetch the sentence from database server
            mycursor.execute(f"SELECT id_sentence,jap_sentence,last_update FROM sentence ORDER BY id_sentence asc LIMIT {number} ")
            myresult = mycursor.fetchall()

            for row in myresult:
                list_sentences.append(Sentence(row[0], row[1], row[2]))

            json_listsentence = [obj.to_dict_set() for obj in list_sentences]
            jsdata = json.dumps({"list_sentence": json_listsentence}, indent=4, sort_keys=True, default=str)
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



