class User:

    def __init__(self, id, role, name, username, password, time):
        self.id = id
        self.role = role
        self.name = name
        self.username = username
        self.password = password
        self.time = time

    def to_dict_set(self):
        return {"id_user": self.id, "role": self.role,"name": self.name,  "username": self.username, "password": self.password, "time": self.time}
