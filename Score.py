
class Score:

    def __init__(self, id_user, id_score, score, sub_time):
        self.id_user = id_user
        self.id_score = id_score
        self.score = score
        self.sub_time = sub_time

    def to_dict_set(self):
        return {"id_user": self.id_user, "id_score": self.id_score, "score": self.score, "sub_time": self.sub_time}
