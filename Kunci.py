class Kunci():

    def __init__(self,id,kunci,time):
        self.id=id
        self.kunci=kunci
        self.time=time


    def to_dict_set(self):
        return {"id": self.id, "sentence": self.kunci, "time": self.time}

    def display(self):
        print("id sentence = " + str(self.id))
        print("sentence = " + str(self.kunci))
        print("time = " + str(self.time))
        print("#########################")
