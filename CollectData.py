import mysql.connector
from dbConnect import connect

class CollectData:
    @classmethod
    def collect(self,id_data,id_sentence,id_user,sen_res,token_res_sur,token_res_pro,au_size,ex_time,sum_token_res,score):
        try:
            status = 'false'
            mydb = mysql.connector.connect()
            mycursor = mydb.cursor()

            # fetch the sentence from database server
            mycursor.execute("INSERT INTO collect_data(id_data,id_sentence,id_user,sen_res,token_res_sur,token_res_pro,au_size,ex_time,sum_token_res,score) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(id_data,id_sentence,id_user,sen_res,token_res_sur,token_res_pro,au_size,ex_time,sum_token_res,score))
            mydb.commit()
            status = 'true'

        except mysql.connector.Error as error:
            mydb.rollback()  # rollback if any exception occured
            print("Failed insert record to collect_data table {}".format(error))
        finally:
            # closing database connection.
            if (mydb.is_connected()):
                mycursor.close()
                mydb.close()
                #print("MySQL connection is closed")
            return status


    @classmethod
    def getLastID(self):
        try:
            id = ""
            mydb =  mysql.connector.connect()
            mycursor = mydb.cursor()

            # fetch the sentence from database server
            mycursor.execute("SELECT id_data FROM collect_data ORDER BY id_data desc LIMIT 1")
            myresult = mycursor.fetchall()

            for row in myresult:
                id = int(row[0])

            if (id ==""):
                id=0

        except mysql.connector.Error as error:
            mydb.rollback()  # rollback if any exception occured
            print("Failed Selecting record from collect_data table {}".format(error))
        finally:
            # closing database connection.
            if (mydb.is_connected()):
                mycursor.close()
                mydb.close()
                #print("MySQL connection is closed")
            return id

#INSERT INTO collect_data VALUES(1,"委員を選ぶことです","委員を選ぶことです","[委員,を,選ぶ,こと,です]","[委員,を,選ぶ,こと,です]",300000,2000,5,5,1)


#CollectData.collect(CollectData.getLastID()+1,"委員を選ぶことです","委員を選ぶことです","[委員,を,選ぶ,こと,です]","[委員,を,選ぶ,こと,です]",300000,2000,5,5,1)