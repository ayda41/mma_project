
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
categories = ['Automobile', 'Charges', 'Clothing', 'Education', 'Events', 'Food', 'Gift', 'Healthcare/Insurance', 'Household', 'Leisure', 'Pet', 'Utilities']
def create_transaction(project, amount, people, payer, method, description, category, *args):
    date = datetime.datetime.now().strftime("%m-%d-%y-%H-%M")
    #create the transac id using a hash function with the project id the date and the amount
    hash_id = str(project.id) + str(date) + str(amount)
    transac_id = hash(hash_id)
    people_name = []
    for i in people:
        people_name.append(i.name)
    transac = pd.DataFrame({"project_id": project.id, 
                            "transac_id": transac_id,
                            "date": date, 
                            "total_amount": amount, 
                            "people_name": people_name,
                            "payer_name": payer.name, 
                            "method": method, 
                            "description": description,
                            "category": category})
    t = transac#.drop(index = 1)
    project.add_transaction(t)
    if method == 'equal':
        balance = {}
        split = amount/len(people_name)
        for i in people:
            balance.update({i: split})
        if payer in people:
            balance[payer] = balance[payer] - amount
        else:
            balance.update({payer: - amount})
        project.update_balance(balance)
    if method == 'unequal':  #still need work
        balance = args[0]
        del balance[payer]
        project.update_balance(balance)

#need a function that takes the balance of a project, computes which user owes who 
#and updates the owed balance of each user belonging to the project. 

def create_personal_transaction(user, amount, description, category):
    date = datetime.datetime.now().strftime("%m-%d-%y-%H-%M")
    #create the transac id using a hash function with the project id the date and the amount
    hash_id = str(user.id) + str(date) + str(amount)
    transac_id = hash(hash_id)
    transac = pd.DataFrame({"transac_id": transac_id,
                            "date": date, 
                            "total_amount": amount, 
                            "description": description,
                            "category": [category]})
    t = transac#.drop(index = 1)
    user.persoExp.add_transaction(t)
    
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
        #negative balance indicates money is owed to user by others

        self.friends = []
        self.user_projects = []
        
        self.id = hash(name + email)

        
 #adding a new project to the Project list through the engine:


        self.persoExp = PersonalLedger()
    

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
                                        dtype = 'object') #modify with index [year, nb of week in year]  datetime.date(2019, 1, 7).isocalendar()[1]
        #add a monthlyAmount
        
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
        
    def update_weeklyAmountPerCategory(self):
        current_date = datetime.datetime.now().strftime("%m-%d-%y-%H-%M")
        week_array = []
        for i in reversed(range(0,7)):
            day = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%m-%d-%y")
            week_array.append(day)
        week_amount = self.persoLedger[['date', 'total_amount', 'category']]
        week_amount.date = week_amount.date[0:8]
        week_amount.loc[week_amount['date'].isin(week_array)]
        amount_per_category = week_amount[['category', 'total_amount']]
        self.weeklyAmountPerCategory = amount_per_category
        
    def return_weekly_report(self):
        return self.weeklyAmountPerCategory.groupby(['category'])[['total_amount']].sum()
