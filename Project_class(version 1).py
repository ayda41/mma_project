# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
def create_transaction(project, amount, people, payer, method, description, category, *args):
    date = datetime.datetime.now().strftime("%m-%d-%y-%H-%M")
    #create the transac id using a hash function with the project id the date and the amount
    hash_id = str(project.id) + str(date) + str(amount)
    transac_id = hash(hash_id)
    people_id = []
    for i in people:
        people_id.append(i.id)
    transac = pd.DataFrame({"project_id": project.id, 
                            "transac_id": transac_id,
                            "date": date, 
                            "total_amount": amount, 
                            "people_id": people_id,
                            "payer_id": payer.id, 
                            "method": method, 
                            "description": description,
                            "category": category})
    t = transac#.drop(index = 1)
    project.add_transaction(t)
    if method == 'equal':
        balance = {}
        split = amount/len(people_id)
        for i in people:
            if i != payer:
                balance.update({i: split})
        balance.update({payer: -amount})
        project.update_balance(balance)
    if method == 'custom':  #still need work
        balance = args[0]
        del balance[payer]
        project.update_balance(balance)

class Project():
    def __init__(self, name, users):
        self.project_name = name
        self.project_users = users
        hash_id = name
        for i in users:
            hash_id += i.name
        self.id= hash(hash_id)
        self.ledger = pd.DataFrame({"project_id": self.id, 
                                    "transac_id": [np.nan],
                                    "date": [np.nan], 
                                    "total_amount": [np.nan],
                                    "people_name": [np.nan], 
                                    "payer_name": [np.nan], 
                                    "method": [np.nan],
                                    "description": [np.nan],
                                    "category": [np.nan]},
                                    dtype = 'object')
        self.balance = {user.name: 0 for user in users}
        
    def change_name(self, new_name):
        self._project_name = new_name
        
    def add_transaction(self, transac):
        self.ledger = pd.concat([self.ledger, transac], ignore_index = True)
        
    def update_balance(self, balance):
        for user, amount in balance.items():
            self.balance[user.name] = self.balance[user.name] + amount
    
class User():
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.balance = {}
        self.friends = []
        self.user_projects = []
        self.id = hash(name + email)
        
    
    def add_project(self, project : Project):
        self.user_projects.append(project)
        for user in project.project_users:
            if user not in self.friends and user.id != self.id:
                self.friends.append(user)
                self.balance[user.name] = 0

    def add_friends(self, friend):
        self.friends.append(friend)
