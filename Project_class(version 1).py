
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import time
import datetime

######################

#The engine manages the creation of new users, new projects, new transactions and uses built-in functions to do so.

#In a project, transactions are handled as a dataset.
#Transaction = (id, date, total amount, people, payer, splitting method, description)

#The id can be generated through a hash function using the project id, the date and the amount.
#The date is "%m-%d-%y-%H-%M"


class Project():
    def __init__(self, name, users):
        self.project_name = name
        self.project_users = users
        self.ledger = []
        self.balance = {user.name: 0 for user in users}
        hash_id = name
        for i in users:
            hash_id += i.name
        self.project_id = hash(hash_id)
    
    # @property
    # def project_id(self):
    #     return self._project_id
    # 
    # @property
    # def ledger(self):
    #     return self._ledger
    # 
    # @property
    # def balance(self):
    #     return self._balance
    #     
    # # @balance.setter
    # # def balance(self, transaction):
        
    def change_name(self, new_name):
        self._project_name = new_name
        
    def add_transaction(self, transac):
        self.ledger.append(transac)
        
    def update_ledger(self, balance: dict):
        for user, amount in balance.items():
            self.balance[user.name] = self.balance[user.name] + amount
    
    #The project ledger is updated through the engine.
    
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
   
    def update_balance(self, balance: dict):
        for friend, amount in balance.items():
            self.balance[friend] = self.balance[friend] + amount
            
    def print_projects(self):
        l = []
        for i in self.user_projects:
            l.append(i.project_name)
        return l 
    
    def print_friends(self):
        l = []
        for i in self.friends:
            l.append(i.name)
        return l 

class PersonalLedger():
    def __init__(self):
        self.persoLedger = pd.DataFrame({"transac_id": [np.nan],
                                        "date": [np.nan], 
                                        "total_amount": [np.nan],
                                        "description": [np.nan],
                                        "category": [np.nan]},
                                        dtype = 'object')
        self.weeklyAmount = 0
        self.weeklyAmountPerCategory = pd.DataFrame({"total_amount": [np.nan],
                                        "category": [np.nan]},
                                        dtype = 'object')

        
    def add_transaction(self, mytransac):
        self.persoLedger = pd.concat([self.persoLedger, mytransac], ignore_index = True)
    
    def update_weeklyAmount(self):
        current_date = datetime.datetime.now().strftime("%m-%d-%y-%H-%M")
        week_array = []
        for i in reversed(range(0,7)):
            day = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%m-%d-%y")
            week_array.append(day)
        week_amount = self.persoLedger[['date', 'total_amount']]
        week_amount.date = week_amount.date[0:8]
        week_amount.loc[week_amount['date'].isin(week_array)]
        amount = week_amount['total_amount'].sum()
        self.weeklyAmount = amount
