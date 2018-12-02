
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
categories = ['Automobile', 'Charges', 'Clothing', 'Education','Electronics', 'Events', 'Food', 'Gift', 'Healthcare/Insurance', 'Household', 'Leisure', 'Pet', 'Utilities']

months = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

max_allowance={'student':{'Automobile':2000, 'Charges':20, 'Clothing':20, 'Education':2, 'Events':1, 'Food':2000, 'Gift':200, 'Healthcare/Insurance':100, 'Household':2000, 'Leisure':200, 'Pet':50, 'Utilities':200,'Electronics':2000},'Working>50000':{'Automobile':0, 'Charges':0, 'Clothing':0, 'Education':0, 'Events':0, 'Food':0, 'Gift':0, 'Healthcare/Insurance':0, 'Household':0, 'Leisure':0, 'Pet':0, 'Utilities':0,'Electronics':0},'Working<50000':{'Automobile':0, 'Charges':0, 'Clothing':0, 'Education':0, 'Events':0, 'Food':0, 'Gift':0, 'Healthcare/Insurance':0, 'Household':0, 'Leisure':0, 'Pet':0, 'Utilities':0,'Electronics':0}}

LARGE_FONT= ("Verdana", 18)
SMALL_FONT= ("Arial", 12)
def create_transaction(project, amount, people, payer, method, description, category, *args):
    date = datetime.datetime.now().strftime("%m-%d-%y-%H-%M")
    hash_id = str(project.id) + str(date) + str(amount)
    transac_id = hash(hash_id)
    people_name = []
    S=[]
    for i in args:
        S.append(float(i))
    for i in people:
        people_name.append(i.name)

    if method == 'equal':
        balance = {}
        split = amount/len(people_name)
        #Split=list(args)
        Split = np.array([split]*len(people_name))
        for i in people:
            balance.update({i: split})
        if payer in people:
            balance[payer] = balance[payer] - amount
        else:
            balance.update({payer: - amount})
        project.update_balance(balance)
        
    if method == 'unequal':  #still need work
        balance = {}
        Split=S
        balance.update({payer: -amount})
        for i in people:
            balance.update({i: Split[people.index(i)]})
        if payer in people:
            balance[payer] = balance[payer] - Split[people.index(i)]
        else:
            balance.update({payer: - amount})
        project.update_balance(balance)
    push_balance_project_user(balance)
    
    transac = pd.DataFrame({"project_id": project.id, 
                            "transac_id": transac_id,
                            "date": date, 
                            "total_amount": amount, 
                            "people_name": [people_name],
                            "payer_name": payer.name, 
                            "method": method, 
                            "description": description,
                            "category": category,
                            "Split": [Split]})
    project.add_transaction(transac)

    push_balance_project_user(balance)
#need a function that takes the balance of a project, computes which user owes who 
#and updates the owed balance of each user belonging to the project. 
def create_personal_transaction(user, amount, description, category):
    date = datetime.datetime.now()
    date_string = date.strftime("%m-%d-%y-%H-%M")
    hash_id = str(user.id) + str(date) + str(amount)
    transac_id = hash(hash_id)
    transac = pd.DataFrame({"transac_id": transac_id,
                            "date": date_string, 
                            "total_amount": amount, 
                            "description": description,
                            "category": [category]})
    user.persoExp.add_transaction(transac)
    user.persoExp.update_transac_weekly_report(transac, date)
    user.persoExp.update_transac_monthly_report(transac, date)
    
def push_balance_project_user(balance):
    owed = {}
    owers = {}
    neutral = {}
    for person, amount in balance.items():
        if amount > 0 :
            owers[person] = amount
        if amount < 0 :
            owed[person] = -amount
        else:
            neutral[person] = 0
    for owed_person, owed_amount in owed.items() :
        while owed_amount > 0:
            for owers_person, owers_amount in owers.items() : 
                if owed_amount > owers_amount :
                    owed_person.balance[owers_person] -= owers_amount
                    owers_person.balance[owed_person] += owers_amount
                    owed_amount -= owers_amount
                    owers_amount = 0
                else:
                    owed_person.balance[owers_person] -= owed_amount
                    owers_person.balance[owed_person] += owed_amount
                    owers_amount -= owed_amount
                    owed_amount = 0
def payback(user, friend, amount):
    if user.balance[friend] == 0:
        raise ValueError('You do not owe that person.')
    if amount <= user.balance[friend]:
        user.payback(friend, amount)
        friend.receive(user, amount)
    else:
        raise ValueError('You can not pay back more than what you owe.')
    
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
        self.balance = {user: 0 for user in users}
    
        
    def change_name(self, new_name):
        self._project_name = new_name
        
    def add_transaction(self, transac):
        self.ledger = pd.concat([self.ledger, transac], ignore_index = True)
        
    def update_balance(self, balance):
        for user, amount in balance.items():
            self.balance[user] = self.balance[user] + amount
    
    def repr_ledger(self):
        rep = self.ledger.drop([0])
        return rep  
        
    def print_balance(self):
        balance_name = {}
        for f in self.balance:
            balance_name[f.name] = self.balance[f]
        return balance_name

class User():
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.balance = {} 
        #negative balance indicates money is owed to user by others

        self.friends = []
        self.user_projects = []
        
        self.id = hash(name + email)
        self.persoExp = PersonalLedger()
    
#adding a new project to the Project list through the engine:
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
    
    def print_balance(self):
        balance_name = {}
        for f in self.balance:
            balance_name[f.name] = self.balance[f]
        return balance_name
    
    def payback(self, friend, amount):
        self.balance[friend] -= amount
    
     def receive(self, friend, amount):
        self.balance[friend] += amount

class PersonalLedger():
    def __init__(self):
        self.persoLedger = pd.DataFrame({"transac_id": [np.nan],
                                        "date": [np.nan], 
                                        "total_amount": [np.nan],
                                        "description": [np.nan],
                                        "category": [np.nan]},
                                        dtype = 'object')
        (year, nb_week, day) = datetime.datetime.now().isocalendar()
        self.weekly_report = pd.DataFrame({"year": year, "week": nb_week,
                                                    "category": [np.nan], 
                                                    "total_amount": [np.nan]},
                                        dtype = 'object') 
        nb_month = datetime.datetime.now().month
        self.monthly_report = pd.DataFrame({"year": year, "month": nb_month,
                                                    "category": [np.nan], 
                                                    "total_amount": [np.nan]},
                                        dtype = 'object')
        
    def add_transaction(self, mytransac):
        self.persoLedger = pd.concat([self.persoLedger, mytransac], ignore_index = True)

  
    def total_weeklyAmount(self):
        (year, week, day) = datetime.datetime.now().isocalendar()
        self.weekly_report.loc[self.weekly_report['week'] == week].loc[self.weekly_report['year'] == year]
        amount = self.weekly_report['total_amount'].sum()
        return amount

    def update_transac_weekly_report(self, transac, date):
        (year, week, day) = date.isocalendar()
        transac_amount = transac.at[0, 'total_amount']
        transac_category = transac.at[0, 'category']
        if((self.weekly_report['year'] == year) & (self.weekly_report['week'] == week) & (self.weekly_report['category'] == transac_category)).any():
            category_sum = self.weekly_report.loc[(self.weekly_report['year'] == year) & (self.weekly_report['week'] == week) & (self.weekly_report['category'] == transac_category)]['total_amount'].sum() + transac_amount
            i = self.weekly_report[(self.weekly_report['year'] == year) & (self.weekly_report['week'] == week) & (self.weekly_report['category'] == transac_category)].index
            self.weekly_report.loc[i, 'total_amount'] = category_sum
        else:
            new_weekly_report = pd.DataFrame({"year": year, "week": week, 
                                                    "category": transac_category, 
                                                    "total_amount": [transac_amount]}) 
            self.weekly_report = pd.concat([self.weekly_report, new_weekly_report], ignore_index = True)
        
    def return_weekly_report(self):
        (year, week, day) = datetime.datetime.now().isocalendar()
        return self.weekly_report.loc[(self.weekly_report['year'] == year) & (self.weekly_report['week'] == week)].drop([0])
        
    
    
    def total_monthlyAmount(self):
        (year, month) = (datetime.datetime.now().year, datetime.datetime.now().month)
        self.monthly_report.loc[self.monthly_report['month'] == month].loc[self.monthly_report['year'] == year]
        amount = self.monthly_report['total_amount'].sum()
        return amount

    def update_transac_monthly_report(self, transac, date):
        (year, month) = (date.year, date.month)
        transac_amount = transac.at[0, 'total_amount']
        transac_category = transac.at[0, 'category']
        if((self.monthly_report['year'] == year) & (self.monthly_report['month'] == month) & (self.monthly_report['category'] == transac_category)).any():
            category_sum = self.monthly_report.loc[(self.monthly_report['year'] == year) & (self.monthly_report['month'] == month) & (self.monthly_report['category'] == transac_category)]['total_amount'].sum() + transac_amount
            i = self.monthly_report[(self.monthly_report['year'] == year) & (self.monthly_report['month'] == month) & (self.monthly_report['category'] == transac_category)].index
            self.monthly_report.loc[i, 'total_amount'] = category_sum
        else:
            new_monthly_report = pd.DataFrame({"year": year, "month": month, 
                                                    "category": transac_category, 
                                                    "total_amount": [transac_amount]}) 
            self.monthly_report = pd.concat([self.monthly_report, new_monthly_report], ignore_index = True)

    def return_monthly_report(self):
        (year, month) = (datetime.datetime.now().year, datetime.datetime.now().month)
        return self.monthly_report.loc[(self.monthly_report['year'] == year) & (self.monthly_report['month'] == month)].drop([0])

    def return_transactions(self):
        return self.persoLedger[["date", "total_amount", "description","category"]].copy().drop([0])
