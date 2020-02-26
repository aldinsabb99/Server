class Sentence():

    def __init__(self,id,sentence,time):
        self.id=id
        self.sentence=sentence
        self.time=time


    def to_dict_set(self):
        return {"id": self.id, "sentence": self.sentence, "time": self.time}

    def display(self):
        print("id sentence = " + str(self.id))
        print("sentence = " + str(self.sentence))
        print("time = " + str(self.time))
        print("#########################")



#obj= Sentence(1,"Test1",0)
#obj.display()
#obj.set_score(100)
#obj.display()

# sentencee = ["AA","BB","CC","DD","EE"]
# list_sentences = []
#
# for i in range(5):
#     list_sentences.append(Sentence(i,sentencee[i],0))
#
#
# for obj in list_sentences:
#     obj.display()
#
#
# list_sentences[1].set_score(100)
# list_sentences[4].set_score(90)
#
# for obj in list_sentences:
#     obj.display()
