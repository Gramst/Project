import json

class Users:

    def __init__(self, path):
        self.users = {}
        if path == None:
            self.path = ''
        else:
            self.path = path
        try:
            with open(self.path + "know.id", "w") as f:
                self.users = json.load(f)
        except:
            pass


    def new_user(self, user_id):
            self.users[user_id] = {}


    def search(self, user_id):
        if user_id in self.users:
            return True
        else:
            return False

    def check_user(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = {}
            self.users[user_id]['map_dots'] = {}
            self.users[user_id]['states'] = {
                                            'geo' : False,
                                            'atm' : False,
                                            'money' : False,
                                            'sett' : False
                                            }

    def users_save(self):
        with open(self.path + "know.id", "w") as f:
            json.dump(self.know, f, indent=2)

    def set_state(self, user_id, name_state):
        self.reset_state(user_id)
        self.users[user_id]['states'][name_state] = True


    def get_state(self, user_id):
        self.check_user(user_id)
        result = 'Error'
        n = 0
        for state in self.users[user_id]['states']:
            if self.users[user_id]['states'][state]:
                result = state
                n +=1

        if n > 1 :
            self.reset_state(user_id)
            result = 'Error'

        return result


    def reset_state(self, user_id):
        self.check_user(user_id)
        for state in self.users[user_id]['states']:
            self.users[user_id]['states'][state] = False


    def add_searched_name(self, user_id, text):
        ...


    def get_searched_name(self, user_id)