from tkinter import *
from tkinter import ttk

import tkinter as tk

LARGE_FONT= ("Verdana", 16)
SMALL_FONT= ("Arial", 12)
current_tariff = None


def tariff_A():
    global current_tariff
    current_tariff= "A"

def tariff_B():
    global current_tariff
    current_tariff= "B"

def tariff_C():
    global current_tariff
    current_tariff= "C"

    
    
    
### IMPORTED LIBRARIES
import time
import datetime
import pandas as pd
pd.set_option('display.expand_frame_repr', False)
import matplotlib
import matplotlib.pyplot as pyplot
import calendar
import numpy as np
import shelve
matplotlib.use('TKagg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure 

##Part of the engine
categories = ['Automobile', 'Charges', 'Clothing', 'Education', 'Events', 'Food', 'Gift', 'Healthcare/Insurance', 'Household', 'Leisure', 'Pet', 'Utilities','Electronics']
months = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
max_allowance={'student':{'Automobile':2000, 'Charges':20, 'Clothing':20, 'Education':2, 'Events':1, 'Food':2000, 'Gift':200, 'Healthcare/Insurance':100, 'Household':2000, 'Leisure':200, 'Pet':50, 'Utilities':200,'Electronics':2000},'Working>50000':{'Automobile':0, 'Charges':0, 'Clothing':0, 'Education':0, 'Events':0, 'Food':0, 'Gift':0, 'Healthcare/Insurance':0, 'Household':0, 'Leisure':0, 'Pet':0, 'Utilities':0,'Electronics':0},'Working<50000':{'Automobile':0, 'Charges':0, 'Clothing':0, 'Education':0, 'Events':0, 'Food':0, 'Gift':0, 'Healthcare/Insurance':0, 'Household':0, 'Leisure':0, 'Pet':0, 'Utilities':0,'Electronics':0}}
"""
the input people is a list of objects of class User
the input payer is an object of class User
"""
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
        
def is_in_user_login(user):
    user_login = shelve.open('user_login')
    if user.name in user_login:
        return True
    else:
        return False
def update_user_login(user, password):
    user_login = shelve.open('user_login')
    user_login[user.name] = password
    user_login.close()
    
def update_user_database(user):
    user_database = shelve.open('user_database')
    user_database[user.name] = user
    user_database.close()

##

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
                                    "category": [np.nan],
                                    "Split": [np.nan]},
                                    dtype = 'object')
        self.balance = {user: 0 for user in users}
    
        
    def change_name(self, new_name):
        self._project_name = new_name
    
    def Name_project(self):
        return self.project_name
        
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
    
    def repr_ledger(self):
        rep = self.persoLedger.drop([0])
        return rep 
   
    def return_transactions(self):
        return self.persoLedger[["date", "total_amount", "description","category"]].copy().drop([0])

    


class User():
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.balance = {}   #owed balance to the friends: if value is negative, means that the friend owes you money
        self.friends = []
        self.user_projects = []
        self.id = hash(name + email)
        self.persoExp = PersonalLedger()
    
    
    def add_project(self, project : Project):
        self.user_projects.append(project)
        for user in project.project_users:
            if user not in self.friends and user.id != self.id:
                self.friends.append(user)
                self.balance[user] = 0
    #the engine adds the project to the users' projects list

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
        
    def get_reports_monthly(user, month, year):
    user_name=user
    user_name_str=user.name
    Monthly_graph_categories= {element:0 for element in categories}
    for i in user_name.user_projects:
        Existing_ledg=i.repr_ledger()
        for index, row in Existing_ledg.iterrows():
            if  datetime.datetime.strptime(row['date'], '%m-%d-%y-%H-%M').month==months[month] and datetime.datetime.strptime(row['date'], '%m-%d-%y-%H-%M').year== year:
                if user_name_str in row['people_name']:
                    Monthly_graph_categories[(row['category'])]+= row['Split'][(row['people_name'].index(user_name_str))]
                else:
                    pass
            else:
                pass
    Pers_ledger=user_name.persoExp.repr_ledger()
    for index,row in Pers_ledger.iterrows():
        if  datetime.datetime.strptime(row['date'], '%m-%d-%y-%H-%M').month==months[month] and datetime.datetime.strptime(row['date'], '%m-%d-%y-%H-%M').year== year:
            Monthly_graph_categories[row['category']]+=row['total_amount']
    return Monthly_graph_categories
    
    def get_reports_weekly(user, month, year):
    user_name=user
    user_name_str=user.name
    Weekly_graph_categories={}
    for i in range(53):
        Weekly_graph_categories[i]={element:0 for element in categories}
    for i in user_name.user_projects:
        Existing_ledg=i.repr_ledger()
        for index, row in Existing_ledg.iterrows():
            if  datetime.datetime.strptime(row['date'], '%m-%d-%y-%H-%M').month==months[month] and datetime.datetime.strptime(row['date'], '%m-%d-%y-%H-%M').year== year:
                if user_name_str in row['people_name']:
                    Weekly_graph_categories[int(datetime.date(datetime.datetime.strptime(row['date'], '%m-%d-%y-%H-%M').year,datetime.datetime.strptime(row['date'], '%m-%d-%y-%H-%M').month,datetime.datetime.strptime(row['date'], '%m-%d-%y-%H-%M').day).isocalendar()[1])][(row['category'])]+= row['Split'][(row['people_name'].index(user_name_str))]
                else:
                    pass
                
            else:
                pass
    Pers_ledger=user_name.persoExp.repr_ledger()
    for index,row in Pers_ledger.iterrows():
        if  datetime.datetime.strptime(row['date'], '%m-%d-%y-%H-%M').month==months[month] and datetime.datetime.strptime(row['date'], '%m-%d-%y-%H-%M').year== year:
            Weekly_graph_categories[int(datetime.date(datetime.datetime.strptime(row['date'], '%m-%d-%y-%H-%M').year,datetime.datetime.strptime(row['date'], '%m-%d-%y-%H-%M').month,datetime.datetime.strptime(row['date'], '%m-%d-%y-%H-%M').day).isocalendar()[1])][(row['category'])]+= row['total_amount']
        else:
            pass
        
    for i in range((datetime.date(year,int(months[month]),1).isocalendar()[1]),(datetime.date(year,months[month],calendar.monthrange(year,months[month])[1]).isocalendar()[1])+1):
        print(Weekly_graph_categories[i])
        pyplot.pie([float(v) for v in Weekly_graph_categories[i].values()], labels=[str(k) for k in Weekly_graph_categories[i].keys()],
           autopct=None)
    return Weekly_graph_categories

def track_expense(user, month, year,class_existence):
    expense=get_reports_monthly(user,month, year)
    expense_left={}
    g_list=[]
    q_list=[]
    critical_expense_list={}
    for i in categories:
        expense_left[i]=max_allowance[class_existence][i]-expense[i]
        g_list.append(expense[i])
        q_list.append(expense_left[i])
        y=((expense_left[i]/max_allowance[class_existence][i]))*100
        if expense[i]>max_allowance[class_existence][i]:
            critical_expense_list[i]=f'you have surpassed the allowance by:${-expense_left[i]} of {max_allowance[class_existence][i]}'
        else:
            critical_expense_list[i]=f'you have about {y}% of allowance remaining:${expense_left[i]} of {max_allowance[class_existence][i]}'
    ind = np.arange(1,1+len(categories))
    pyplot.bar(ind, g_list, .35)
    pyplot.bar(ind, q_list, .35, bottom=g_list)
    return critical_expense_list
    
   def save_suggestions(user,month, year,class_existence,amount_save):
    prev_month=[k for k,v in months.items() if v == (months[month]-1)]
    Exp_prevmonth=get_reports_monthly(user,prev_month[0], year)
    curr_exp_over_class={element:0 for element in categories}
    percent_exp={element:0 for element in categories}
    bud_sug={element:0 for element in categories}
    for i in categories:
        if Exp_prevmonth[i]-max_allowance[class_existence][i]>0:
            curr_exp_over_class[i]= Exp_prevmonth[i]-max_allowance[class_existence][i]
        percent_exp[i]=Exp_prevmonth[i]/sum(Exp_prevmonth.values())
    for i in categories:    
        bud_sug[i]=curr_exp_over_class[i]/sum(curr_exp_over_class.values())*amount_save
        bud_sug [i]=f'you can reduce expenditure by: ${bud_sug[i]}'
        
### ENGINE CLASSES 
class EasySplit(tk.Tk):    
    
    def __init__(self, *args, **kwargs):
        
        self.user_name = 'default'
        self.user = User('default', 'default')
        self.project = Project('default', [])

        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Easy Split')
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MenuPage, MyLedgerPage, BalancePage, AnalyticPage, AccountPage, CreateProjectPage, LogIn, SignUpPage, CreatePersoTransac, PaybackPage, ProjectListPage, ProjectPage, FriendsPage, CreateTransacPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LogIn)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        
    def set_user(self, user_name):
        user_database = shelve.open('user_database')
        if user_name in user_database:
            self.user = user_database[user_name]
            self.user_name = user_name
        else:
            raise ValueError('The user does not exists.')
        user_database.close()

    def set_project(self, project_name):
        project_database = shelve.open('project_database')
        if project_name in project_database:
            self.project = project_database[project_name]
        else:
            raise ValueError('The project does not exist.')
        project_database.close()



class SignUpPage(tk.Frame):
    
    def create_user(self):
        
        global idEntry
        global emailEntry
        global passwordEntry
        
        id = idEntry.get()
        email = emailEntry.get()
        password = passwordEntry.get()
        new_user = User(id, email)
        if not is_in_user_login(new_user):
            update_user_login(new_user, password)
            update_user_database(new_user)
            update_friend(new_user)
            self.controller.show_frame(LogIn)

        else:
            print("Username already exists")
            idEntry.delete(0, END)
            passwordEntry.delete(0, END)
            emailEntry.delete(0, END)
    
    def __init__(self, parent, controller):
        
        global idEntry
        global passwordEntry
        global emailEntry
        
        self.controller = controller

        tk.Frame.__init__(self, parent, bg='steel blue')

        label = tk.Label(self, text="Sign up", font=LARGE_FONT, bg='steel blue')
        label.pack(pady=10,padx=10)        

        idLabel = Label(self, text = 'Username:', bg='steel blue')
        idEntry = Entry(self, width=40)
        
        emailLabel = Label(self, text = 'Email:', bg='steel blue')
        emailEntry = Entry(self, width=40)

        passwordLabel = Label(self, text = 'Password: ', bg='steel blue')
        passwordEntry = Entry(self, width=40, show ="*")

        idLabel.pack(pady =10, padx = 10, side = TOP, anchor = N)
        idEntry.pack(pady =5, padx = 10, side = TOP, anchor = N)
        
        emailLabel.pack(pady =10, padx = 10, side = TOP, anchor = N)
        emailEntry.pack(pady =5, padx = 10, side = TOP, anchor = N)
        
        passwordLabel.pack(pady =10, padx = 10, side = TOP, anchor  = S)
        passwordEntry.pack(pady =5, padx = 10, side = TOP, anchor  = S)
        
        button1 = tk.Button(self, text="Create Account", command= self.create_user, bg = 'SteelBlue3')
        button1.pack(pady =10, side = TOP, anchor = S)
        
        button2 = tk.Button(self, text="Back to Log In", command=lambda: controller.show_frame(LogIn), bg = 'SteelBlue3')
        button2.pack(pady =10, side = BOTTOM, anchor = S)


class LogIn(tk.Frame):

    def LogInCheck(self):
        
        global actEntry
        global pinEntry
        
        user_login = shelve.open('user_login')
        user_database = shelve.open('user_database')

        actNum = actEntry.get()
        pinNum = pinEntry.get()

        if actNum in user_login and pinNum == user_login[actNum]:
            self.controller.set_user(actNum)
            self.controller.show_frame(MenuPage)
        elif actNum not in user_login or pinNum != user_login[actNum]: 
            self.text_box.config(state=NORMAL)
            self.text_box.delete('1.0', END)
            self.text_box.insert("end", 'INCORRECT')
            self.text_box.see("end")
            self.text_box.config(state=DISABLED)
            actEntry.delete(0, END)
            pinEntry.delete(0, END)
            self.controller.show_frame(LogIn)
        
        user_login.close()
        user_database.close()
        
    def signUp(self):
        idEntry.delete(0, END)
        passwordEntry.delete(0, END)
        emailEntry.delete(0, END)
        self.controller.show_frame(SignUpPage)
    
    def onclick(self, event):
        self.LogInCheck()
    
    def __init__(self, parent, controller):

        global actEntry
        global pinEntry
        
        self.controller = controller

        tk.Frame.__init__(self, parent, bg='medium turquoise')

        welcomeLabel = Label(self, text = "Easy split", font = LARGE_FONT, bg='medium turquoise',fg='royal blue')
        welcomeLabel.pack(pady =10, padx = 10, side = TOP, anchor = N)
        
        logLabel = Label(self, text = "Login With Your Username and Password", font = SMALL_FONT, bg='medium turquoise',fg='green4')
        logLabel.pack(pady =10, padx = 10, side = TOP, anchor = N)


        actLabel = Label(self, text = 'Username:', bg='medium turquoise')
        actEntry = Entry(self, width=40)

        pinLabel = Label(self, text = 'Password: ', bg='medium turquoise')
        pinEntry = Entry(self, width=40, show ="*")

        actLabel.pack(pady =5, padx = 10, side = TOP, anchor = N)
        actEntry.pack(pady =5, padx = 10, side = TOP, anchor = N)
        
        pinLabel.pack(pady =10, padx = 10, side = TOP, anchor  = N)
        pinEntry.pack(pady =5, padx = 10, side = TOP, anchor  = N)
        
        self.text_box = Text(self, height = 1, width = 30, state=DISABLED, bg='medium turquoise')

        logInButton = tk.Button(self, text = "Login", command = self.LogInCheck, bg = 'turquoise3')
        self.controller.bind('<Return>', self.onclick)
        logInButton.pack(pady =5, side = TOP)
        
        self.text_box.pack(pady =10, side = TOP, fill = Y, expand = False)
        
        bottomframe = Frame(self, bg='medium turquoise')
        bottomframe.pack( side = BOTTOM, anchor=N, fill=X)
        
        signUpButton = tk.Button(bottomframe, text = "Sign up", command = self.signUp, bg = 'turquoise3')
        signUpButton.pack(pady =5, side = TOP)

        quitButton = tk.Button(bottomframe, text = "Quit", command = quit, bg = 'light salmon')
        quitButton.pack(pady =10, padx = 10, side = RIGHT, anchor = SE)
        
class AccountPage(tk.Frame):
    
    def back_home(self, controller):
        controller.show_frame(MenuPage)
        controller.frames[MenuPage].show_user_info(controller)
    
    def change_email(self, new_email, controller):
        if new_email != '':
            name = str(controller.user.name)
            controller.user.email = new_email
            user_database = shelve.open('user_database')
            user_database[name] = controller.user
            user_database.close()
            self.email_text_box.config(state=NORMAL)
            self.email_text_box.delete('1.0', END)
            self.email_text_box.insert("end", 'Email changed to ' + str(new_email))
            self.email_text_box.see("end")
            self.email_text_box.config(state=DISABLED)
            newEmailEntry.delete(0, END)
    
    def reveal_email(self, canvas, controller):
        if not self.emailStatus:
            
            global newEmailEntry
            
            user_database = shelve.open('user_database')
    
            emailLabel = tk.Label(canvas, text="Current Email: " + str(controller.user.email), anchor="w", font=SMALL_FONT,  bg = 'SteelBlue2')
            emailLabel.pack(pady=10,padx=10)
            
            newEmailEntry = Entry(canvas, width=50)
            newEmailEntry.pack(side = TOP)
            
            EmailButton = tk.Button(canvas, text="Change email",
                            command=lambda: self.change_email(newEmailEntry.get(), controller))
            EmailButton.pack(pady =5, padx = 5, side = TOP, anchor = N)
            
            self.email_text_box = Text(canvas, height = 1, state=DISABLED, bg='SteelBlue2')
            self.email_text_box.pack(pady =5, padx = 5, side = TOP, anchor = N, fill=X)
            
            user_database.close()
            self.emailStatus = True
        
    def change_password(self, new_password, controller):
        if new_password != '':
            user_login_database = shelve.open('user_login')
            user_login_database[controller.user.name] = new_password
            user_login_database.close()
            self.password_text_box.config(state=NORMAL)
            self.password_text_box.delete('1.0', END)
            self.password_text_box.insert("end", 'Password changed!')
            self.password_text_box.see("end")
            self.password_text_box.config(state=DISABLED)
            newPasswordEntry.delete(0, END)
        
    def reveal_password(self, canvas, controller):
        if not self.passwordStatus:
            
            global newPasswordEntry
            
            user_login = shelve.open('user_login')
    
            passwordLabel = tk.Label(canvas, text="Current Password: " + str(user_login[str(controller.user.name)]), anchor="w", font=SMALL_FONT,  bg = 'SteelBlue2')
            passwordLabel.pack(pady=10,padx=10)
            
            newPasswordEntry = Entry(canvas, width=50, show="*")
            newPasswordEntry.pack(side = TOP)
            
            passwordButton = tk.Button(canvas, text="Change password",
                            command=lambda: self.change_password(newPasswordEntry.get(), controller))
            passwordButton.pack(pady =5, padx = 5, side = TOP, anchor = N)
            
            self.password_text_box = Text(canvas, height = 1, state=DISABLED, bg='SteelBlue2')
            self.password_text_box.pack(pady =5, padx = 5, side = TOP, anchor = NW, fill = X)
            
            user_login.close()
            self.passwordStatus = True
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent,  bg = 'SteelBlue1')
        
        self.passwordStatus = False
        self.emailStatus = False
        
        label = tk.Label(self, text="User Account", font=LARGE_FONT,  bg = 'SteelBlue1')
        label.pack(pady=10,padx=10)
        
        spaceCanvas0 = Canvas(self, height = 3, bg = 'black')
        spaceCanvas0.pack(fill=X)
        
        emailCanvas = Canvas(self, height = 1,  bg = 'SteelBlue2')
        emailCanvas.pack(pady=5, fill=X)
        
        button1 = tk.Button(self, text='Email', command=lambda: self.reveal_email(emailCanvas, controller))
        button1.pack()
        
        spaceCanvas = Canvas(self, height = 3, bg = 'black')
        spaceCanvas.pack(pady=5, fill=X)
        
        passwordCanvas = Canvas(self, height = 1,  bg = 'SteelBlue2')
        passwordCanvas.pack(pady=5, fill=X)
        
        button2 = tk.Button(self, text='Password', command=lambda: self.reveal_password(passwordCanvas, controller))
        button2.pack()
        
        spaceCanvas2 = Canvas(self, height = 3, bg = 'black')
        spaceCanvas2.pack(pady=5, fill=X)
        
        button3 = tk.Button(self, text="Back to Home",
                           command=lambda: self.back_home(controller))
        button3.pack(pady=5, padx=5, side = BOTTOM, anchor=SW)



        

## MAIN

if __name__ == "__main__":
    app = EasySplit()
    app.mainloop()

