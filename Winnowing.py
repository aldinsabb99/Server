import mysql.connector
from dbConnect import connect
import pykakasi
import re

class Winnowing:
    # run preprocessing
    @classmethod
    def preprocessing(self,text):
        text_f = text.replace('、', '')
        text_f = text_f.replace('ー', '')
        text_f = text_f.replace('。', '')
        text_f = text_f.replace(' ', '')
        romaji = Winnowing.to_romaji(text_f)
        filtering = Winnowing.filter_text(romaji)
        print("\n======================================================")
        print("PREPROCESSING")
        print("======================================================")
        print("TEXT: ")
        print(text)
        print("\nROMAJI: ")
        print(romaji)
        print("\nFILTERING : ")
        print(filtering)
        return filtering


    @classmethod
    def winnow(self,text, n, p, w):
        ngram = Winnowing.nGram(text, n)
        roll_hash = Winnowing.hashing(ngram, p)
        window = Winnowing.windowing(roll_hash, w)
        fingerprinting = Winnowing.fingerprint(window, w)
        print("\n======================================================")
        print("WINNOWING")
        print("======================================================")
        print("NGRAM: ")
        print(ngram)
        print("\nHASHING: ")
        print(roll_hash)
        print("\nWINDOWING : ")
        print(window)
        print("\nFINGERPRINTING : ")
        print(fingerprinting)
        return fingerprinting

    @classmethod
    def accuracy_single(self,text_b,text_a):
        prep = Winnowing.preprocessing(text_b)
        print ("ini kunci jawabannya : ")
        print (text_a)
        prep2 = Winnowing.preprocessing(text_a)
        winnowing = Winnowing.winnow(prep, 2, 2, 2)
        winnowing2 = Winnowing.winnow(prep2, 2, 2, 2)
        cosine_measure = Winnowing.cosine(winnowing, winnowing2)
        return cosine_measure



    @classmethod
    def to_romaji(self,text_question):
        kakasi = pykakasi.kakasi()
        kakasi.setMode("H","a") # Hiragana to ascii, default: no conversion
        kakasi.setMode("K","a") # Katakana to ascii, default: no conversion
        kakasi.setMode("J","a") # Japanese
        # to ascii, default: no conversion
        kakasi.setMode("r","Hepburn") # default: use Hepburn Roman table
        kakasi.setMode("s", False) # add space, default: no separator
        kakasi.setMode("C", False) # capitalize, default: no capitalize
        conv = kakasi.getConverter()
        result_q = conv.do(text_question)
        #conv = wakati.getConverter()
        #result = conv.do()
        #print("Teks Soal :" + result_q)
        #print("Teks Hasil:" + result_r)
        #print(result)
        return (result_q)

    @classmethod
    def filter_text(self,text_result):
        #filtering = re.sub("\n", "", text_result).casefold()
        filtering = re.sub("[^A-Za-z0-9]+", "", text_result)
        return filtering

    @classmethod
    def nGram(self,text, n):
        ngram = [text[i:i + n] for i in range(len(text) - n + 1)]
        return ngram

    @classmethod
    def to_hash(self,text, p):
        result = 0
        length = len(text)
        ascii_code = [ord(i) for i in text]  # mengubah ke ascii
        for i in range(length):
            result = result + (ascii_code[i] * pow(p, length - 1))  # rumus rolling hash
            length = length - 1
        return result

    @classmethod
    def hashing(self,ngram, p):
        roll_hash = [Winnowing.to_hash(ngram[i], p) for i in range(len(ngram))]
        return roll_hash

    # windowing
    @classmethod
    def windowing(self,roll_hash, w):
        window = [roll_hash[i:i + w] for i in range(len(roll_hash) - w + 1)]
        return window

    # fingerprint
    @classmethod
    def fingerprint(self,window, w):
        fingers = []
        current_min = None
        # untuk tiap window
        for i in range(0, len(window)):
            minimum = window[i][0]
            # untuk window sepanjang w
            for j in range(1, w):
                if window[i][j] <= minimum:
                    minimum = window[i][j]
            # menyimpan nilai minimum tiap window ke list
            if current_min != minimum:
                fingers.append(minimum)
            elif minimum == window[i][w - 1]:
                fingers.append(minimum)
            current_min = minimum
        return fingers

    # selesai winnowing

    '''
    mulai similarity measurement, mencari tingkat kesamaan fingerprint
    1. jaccard similarity
    2. dice coefficient
    3. cosine similarity
    '''

    # jaccard similarity
    # @classmethod
    # def jaccard(self,fingerprint1, fingerprint2):
    #    num = len(set(fingerprint1).intersection(set(fingerprint2)))
    #    denum = len(set(fingerprint1).union(set(fingerprint2)))
    #    if denum == 0:
    #        jaccard = 0.0
    #    else:
    #        jaccard = float(num / denum) * 100
    #    return jaccard

    # # dice coefficient
    # @classmethod
    # def dice(self,fingerprint1, fingerprint2):
    #     num = 2 * (len(set(fingerprint1).intersection(set(fingerprint2))))
    #     denum = len(set(fingerprint1)) + len(set(fingerprint2))
    #     if denum == 0:
    #         dice = 0.0
    #     else:
    #         dice = float(num / denum) * 100
    #     return dice
    #
    # cosine similarity
    @classmethod
    def cosine(self,fingerprint1, fingerprint2):
        num = len(set(fingerprint1).intersection(set(fingerprint2))) # mencari banyaknya irisan
        denum = (len(set(fingerprint1)) ** .5) * (len(set(fingerprint2)) ** .5) # di akar 5
        if denum == 0:
            cosine = 0.0
        else:
            cosine = float(num / denum) * 100 # tadinya 100
            if cosine > 100:
                cosine = 100.0
        return cosine

    # selesai similarity measurement


# romaji = Winnowing.to_romaji("都会で大学を卒業した人が地元で就職します","都会 で 大学 を 卒業 し た 人 が 地元 です 食し ます 、 ふー 。")
# results = Winnowing.filter_text(romaji)
# print("Hasil Filter " + results)
#print(Winnowing.accuracy_single("委員を選ぶことです","委員の選ぶことです"))
# Winnowing.accuracy()
#Winnowing.winnow("departemen",4,3,3)
# current_score = 0
# current_akurasi = 0
# score = 0
# selisih = 0
# question = 1
# m1 = [100]
# nilai_mahasiswa = [m1]
# var = 1
#
# for q in range (1,question+1):
#     prep = "tokaidedaigakuwosotsugyoushitaningajimotodesushokushimasufu"
#     current_score = 0
#     current_akurasi = 0
#     score = 0
#     selisih = 0
#     #looping untuk tiap kunci
#     prep2 = "tokaidedaigakuwosotsugyoushitaningajimotodeshuushokushimasu"
#     #looping untuk tiap parameter p, n, dan w
#     for p in range (2, 6):
#         if p == 2 or p % 2 == 1:
#             for n in range (2, 8):
#                 for w in range (2, 8):
#                     winnowing = Winnowing.winnow(prep, p, n, w)
#                     winnowing2 = Winnowing.winnow(prep2, p, n, w)
#                     cosine_measure = Winnowing.cosine(winnowing, winnowing2)
#                     # jac_measure = Winnowing.jaccard(winnowing, winnowing2)
#                     # dice_measure = Winnowing.dice(winnowing, winnowing2)
#                     #score = max(jac_measure, dice_measure, cosine_measure)
#                     score = cosine_measure
#                     # if(score==cosine_measure):
#                     #     method = "cosine"
#                     # elif(score==jac_measure):
#                     #     method = "jac"
#                     # elif(score==dice_measure):
#                     #     method = "dice"
#                     selisih = abs(score - nilai_mahasiswa[0][q-1])
#                     akurasi = abs(100 - ((selisih/100)*100))
#                     #akurasi terbesar dipilih, ditampilkan nilai dan parameternya
#                     temp_akurasi = akurasi
#                     print("NOMOR " + str(q))
#                     print("Nilai : " + str(score))
#                     print("Akurasi : " + str(akurasi))
#                     #print("Metode : " + method)
#                     print("Parameter (pnw) : " + (str(p) + str(n) + str(w)))
#                     print("--------------------------------------")
#                     if current_akurasi < temp_akurasi:
#                         current_akurasi = temp_akurasi
#                         current_score = score
#                         px = p
#                         nx = n
#                         wx = w
#                     else:
#                         continue
#     #print hasil untuk tiap nomor
#     print("NOMOR " + str(q))
#     print("Nilai : " + str(current_score))
#     print("Akurasi : " + str(current_akurasi))
#     print("Parameter (pnw) : " + (str(px) + str(nx) + str(wx)))
#     print("--------------------------------------")

