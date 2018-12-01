# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
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
