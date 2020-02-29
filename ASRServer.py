### configure ###########
JULIUS_HOME = "A:\\Skripsi\\dictation-kit\\bin\\windows"
JULIUS_EXEC = "julius -C ..\\..\\am-gmm.jconf -C ..\\..\\main.jconf -input file -outfile"
SERVER_PORT = 8000
ASR_FILEPATH = 'C:\\Users\\User\\Documents\\asr\\'
DATA_FILEPATH = 'C:\\Users\\User\\Documents\\asr\\'
ASR_IN = 'ch_asr.wav'
ASR_RESULT = 'ch_asr.out'
OUT_CHKNUM = 5  # for avoid that the output file is empty
limit = 0

### import ##############
import cherrypy
import subprocess
import os
import time
import socket
import json
import re
import shutil
from DatabaseSentence import DatabaseSentence
from DatabaseUser import DatabaseUser
from DatabaseScore import DatabaseScore
from CollectData import CollectData
from Winnowing import Winnowing
from DatabaseKunci import DatabaseKunci




### class define ########
class ASRServer(object):

    #Julius execution -> subprocess
    p = subprocess.Popen(JULIUS_EXEC, shell=True, cwd=JULIUS_HOME,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         close_fds=True)
    (stdouterr, stdin) = (p.stdout, p.stdin)


    # access to database


    # main task
    @cherrypy.expose
    def index(self):
        return """
			<html><body>
				<h2>Julius Server</h2>
				USAGE:<br />
				- 16000Hz, wav(or raw)-file, big-endian, mono<br />
				<br />
				<form action="asr_julius" method="post" enctype="multipart/form-data">
				filename: <input type="file" name="myFile" /><br />
				<input type="submit" />
				</form>
			</body></html>
			"""

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def collect_data(self):
        input_json = cherrypy.request.json
        id_sentence = input_json["id_sentence"]
        id_user = input_json["id_user"]
        sen_res = input_json["sen_res"]
        token_res_sur = input_json["token_res_sur"]
        token_res_pro = input_json["token_res_pro"]
        au_size = input_json["au_size"]
        ex_time = input_json["ex_time"]
        sum_token_res = input_json["sum_token_res"]
        score = input_json["score"]
        id = CollectData.getLastID()+1
        print(id)
        CollectData.collect(id, id_sentence,id_user, sen_res,token_res_sur,token_res_pro,au_size, ex_time,sum_token_res,score)
        FILEPATH = "file_" +str(id) + ".wav"
        shutil.copy2(ASR_FILEPATH + ASR_IN,DATA_FILEPATH + FILEPATH)
        result = json.dumps({"success": {"code": 200, "message": "successfully collect data"}})
        result2 = json.loads(result)
        return result2


    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def test_conn(self):
        input_json = cherrypy.request.json
        time = input_json["testing"]
        result = json.dumps({"success": {"code": 201, "message": "successfully connect server", "time" : time }})
        result2 = json.loads(result)
        return result2

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_sentences(self):
        result = DatabaseSentence.getSentences(5)
        return result

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def add_sentence(self):
        input_json = cherrypy.request.json
        sentence = input_json["sentence"]
        turn = DatabaseSentence.addSentences(sentence)
        print(turn)
        result = DatabaseSentence.getLastsentence()
        print(result)
        return result

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def remove_sentence(self):
        input_json = cherrypy.request.json
        id = int (input_json["id"])
        try:
            result = DatabaseSentence.getSentence(id)
        except Exception:
            result = json.dumps({"error": {"code": 404, "message": "Id Sentence Not Found"}})
            result2 = json.loads(result)
            return result2
        DatabaseSentence.removeSentences(id)
        return result

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def userval(self):
        input_json = cherrypy.request.json
        username = input_json["username"]
        passw = input_json["password"]
        print(username)
        print(passw)
        try:
            verify = DatabaseUser.getuser(username,passw)
            print(verify)
            id = verify["id_user"]
            DatabaseUser.updateTime(id)
            print(id)
        except Exception :
            result = json.dumps({"error": {"code": 404, "message": "Get User Failed"}})
            result2= json.loads(result)
            return result2
        return verify

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def getuserbyid(self):
        input_json = cherrypy.request.json
        id = input_json["id_user"]
        try:
            verify = DatabaseUser.getuserid(id)
        except Exception :
            result = json.dumps({"error": {"code": 404, "message": "Get User Failed"}})
            result2= json.loads(result)
            return result2
        return verify

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def useradd(self):
        print("udah sampe sini")
        input_json = cherrypy.request.json
        surename = input_json["surename"]
        username = input_json["username"]
        passw = input_json["password"]
        try:
            DatabaseUser.adduser(surename, username, passw)
            user = DatabaseUser.getuser(username,passw)
        except Exception:
            result = json.dumps({"error": {"code": 404, "message": "Get User Failed"}})
            result2 = json.loads(result)
            return result2
        return user

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def get_scores(self):
        input_json = cherrypy.request.json
        id_user = input_json["id_user"]
        try:
            result = DatabaseScore.getscores(id_user)
            print(result)
            return result
        except Exception:
            result_f = json.dumps({"error": {"code": 404, "message": "Get Scores Failed"}})
            result = json.loads(result_f)
        return result

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def set_score(self):
        input_json = cherrypy.request.json
        id_user = input_json["id_user"]
        score = input_json["score"]
        try:
            DatabaseScore.setscore(id_user,score)
            result = DatabaseScore.getLastscore(id_user)
        except Exception:
            result_f = json.dumps({"error": {"code": 404, "message": "Set Score Failed"}})
            result = json.loads(result_f)
        return result



    @cherrypy.expose
    def asr_julius(self,myFile,paramstring):
        body2 = paramstring
        sen = DatabaseKunci.getKunci(body2)
        # receive WAV file from client & write WAV file

        with open(ASR_FILEPATH + ASR_IN, 'wb') as f:
            f.write(myFile.file.read())
        f.close()

        # ASR using Julius
        if os.path.exists(ASR_FILEPATH + ASR_RESULT):
            os.remove(ASR_FILEPATH + ASR_RESULT)  # delete a previous result file

        file = ASR_FILEPATH + ASR_IN + '\n'
        bytes = file.encode(encoding='UTF-8')
        p = subprocess.Popen(JULIUS_EXEC, shell=True, cwd=JULIUS_HOME,
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             close_fds=True)
        p.communicate(input=bytes)

        # wait for result file creation & result writing (avoid the file empty)
        while not (os.path.exists(ASR_FILEPATH + ASR_RESULT) and len(
                open(ASR_FILEPATH + ASR_RESULT, encoding='UTF-8').readlines()) == OUT_CHKNUM):
            time.sleep(1)

        # read result file & send it to client
        outlines = open(ASR_FILEPATH + ASR_RESULT, encoding='UTF-8').read()
        print(outlines)
        m = re.search('sentence1:(.+?)\n', outlines)
        #n = re.search()
        if m:
            found = m.group(1)
        #sen = teks asli
        #found = teks hasil julius
        print("ini loh sen")
        print(sen)
        score = Winnowing.accuracy_single(found,sen)
        print(score)
        result_f = json.dumps({"asr_result": found, "winnowing_score":score})
        return result_f


if __name__ == '__main__':
    server_config={
        'server.socket_host': '8.8.8.8',
        'serve'
        'r.socket_port': SERVER_PORT
        }
    cherrypy.config.update(server_config)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    server_ip = s.getsockname()[0]
    cherrypy.config.update({'server.socket_host': server_ip, })
    cherrypy.quickstart(ASRServer())
