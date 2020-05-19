import mysql.connector
from dbConnect import connect
from Score import Score
import json

class DatabaseScore:

    @classmethod
    def getscores(self,id_user):
        try:
            list_score = []
            mydb =connect()
            mycursor = mydb.cursor()

            # fetch the sentence from database server
            mycursor.execute("SELECT * FROM score WHERE id_user=%s ORDER BY submitted asc" % id_user)
            myresult = mycursor.fetchall()

            for row in myresult:
                list_score.append(Score(id_user, int(row[1]),int(row[2]),(row[3])))

            json_score = [obj.to_dict_set() for obj in list_score]
            jsdata = json.dumps({"list_score": json_score}, indent=4, sort_keys=True, default=str)
            jsdataj = json.loads(jsdata)

        except mysql.connector.Error as error:
            mydb.rollback()  # rollback if any exception occured
            print("Failed Selecting record from python_users table {}".format(error))
        finally:
            # closing database connection.
            if (mydb.is_connected()):
                mycursor.close()
                mydb.close()
                #print("MySQL connection is closed")
                return jsdataj

    @classmethod
    def setscore(self,id_user, score):
        try:
            status = 'false'
            mydb =connect()
            mycursor = mydb.cursor()

            # fetch the sentence from database server
            mycursor.execute("INSERT INTO score(id_user,score) VALUES(%s,%s) ",(id_user,score))
            mydb.commit()
            status = 'true'

        except mysql.connector.Error as error:
            mydb.rollback()  # rollback if any exception occured
            print("Failed Selecting record from python_users table {}".format(error))
        finally:
            # closing database connection.
            if (mydb.is_connected()):
                mycursor.close()
                mydb.close()
                #print("MySQL connection is closed")
                return status

    @classmethod
    def getLastscore(self, id_user):
        try:
            mydb =connect()
            mycursor = mydb.cursor()

            # fetch the sentence from database server
            mycursor.execute("SELECT * FROM score WHERE id_user=%s ORDER BY submitted desc LIMIT 1" % id_user)
            myresult = mycursor.fetchall()

            for row in myresult:
                score_obj = Score(id_user, int(row[1]), int(row[2]), (row[3]))

            json_score = score_obj.to_dict_set()
            jsdata = json.dumps(json_score, indent=4, sort_keys=True, default=str)
            jsdataj = json.loads(jsdata)

        except mysql.connector.Error as error:
            mydb.rollback()  # rollback if any exception occured
            print("Failed Selecting record from python_users table {}".format(error))
        finally:
            # closing database connection.
            if (mydb.is_connected()):
                mycursor.close()
                mydb.close()
                #print("MySQL connection is closed")
                return jsdataj
#print(DatabaseScore.getscores(1))
#print(DatabaseScore.setscore(1,100))
#print(DatabaseScore.getLastscore(2))