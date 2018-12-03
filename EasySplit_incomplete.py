"""
Welcome to EasySplit!

To use the app, please download the script of the app, and the data project_database.dat, user_database.dat and user_login.dat and put them inside a folder.

Please sign up if you don't have an existing account.

This app allows you to create project with your friends and track the expenses of each project.
It will give you the balance of each participant (negative amount means the user owe to the group, positive means the user is owed by the group)

Moreover, you can track your own expenses by accessing the My Ledger page. 

This version is still a work in progress. If you want to use it with several accounts, it must be run on the same machin. Due to the lack of time, the databases are stored locally and the application runs on a single machine.

"""
    
### IMPORTED LIBRARIES

import time
import datetime
import pandas as pd
import calendar
pd.set_option('display.expand_frame_repr', False)
import matplotlib.pyplot as pyplot
import numpy as np
import shelve

from tkinter import *
from tkinter import ttk
import tkinter as tk
import matplotlib
matplotlib.use('TKagg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure 

## APP DATA

categories = ['Automobile', 'Charges', 'Clothing', 'Education','Electronics', 'Events', 'Food', 'Gift', 'Healthcare/Insurance', 'Household', 'Leisure', 'Pet', 'Utilities']

months = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

max_allowance={'student':{'Automobile':2000, 'Charges':20, 'Clothing':20, 'Education':2, 'Events':1, 'Food':2000, 'Gift':200, 'Healthcare/Insurance':100, 'Household':2000, 'Leisure':200, 'Pet':50, 'Utilities':200,'Electronics':2000},'Working>50000':{'Automobile':0, 'Charges':0, 'Clothing':0, 'Education':0, 'Events':0, 'Food':0, 'Gift':0, 'Healthcare/Insurance':0, 'Household':0, 'Leisure':0, 'Pet':0, 'Utilities':0,'Electronics':0},'Working<50000':{'Automobile':0, 'Charges':0, 'Clothing':0, 'Education':0, 'Events':0, 'Food':0, 'Gift':0, 'Healthcare/Insurance':0, 'Household':0, 'Leisure':0, 'Pet':0, 'Utilities':0,'Electronics':0}}

LARGE_FONT= ("Verdana", 18)
SMALL_FONT= ("Arial", 12)


## ENGINE FUNCTIONS

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
        
    # for i in range((datetime.date(year,int(months[month]),1).isocalendar()[1]),(datetime.date(year,months[month],calendar.monthrange(year,months[month])[1]).isocalendar()[1])+1):
        # print(Weekly_graph_categories[i])
        # pyplot.pie([float(v) for v in Weekly_graph_categories[i].values()], labels=[str(k) for k in Weekly_graph_categories[i].keys()], autopct=None)
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
    return bud_sug


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
    

def update_friend(new_user):
    user_database = shelve.open('user_database')
    for name, user in user_database.items():
        user.add_friends(user_database[new_user.name])
        user_database[name] = user
        new_user.add_friends(user)
    user_database[new_user.name] = new_user
    user_database.close()


## CLASS STRUCTURE

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
        self.balance_name = {user.name: 0 for user in users}
        
    def change_name(self, new_name):
        self._project_name = new_name
        
    def add_transaction(self, transac):
        self.ledger = pd.concat([self.ledger, transac], ignore_index = True)
        
    def update_balance(self, balance):
        for user, amount in balance.items():
            print(user.name)
            self.balance[user] += amount
    
    def update_balance_name(self, balance):
        for user, amount in balance.items():
            self.balance_name[user.name] += amount
    
    def repr_ledger(self):
        rep = self.ledger.drop([0])
        return rep  
        
    def print_balance(self):
        balance_name = {}
        for f in self.balance:
            balance_name[f.name] = self.balance[f]
        return balance_name
        
    def return_transactions(self):
        return self.ledger[["date", "total_amount", "people_name", "payer_name", "description","category", "Split"]].copy().drop([0])
    

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
    
    def repr_ledger(self):
        rep = self.persoLedger.drop([0])
        return rep 


class User():
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.balance = {} 
        self.balance_name = {}
        self.friends = []
        self.user_projects = []
        self.id = hash(name + email)
        self.persoExp = PersonalLedger()
    
    
    def add_project(self, project : Project):
        self.user_projects.append(project)

    def add_friends(self, friend):
        if friend not in self.friends and friend.id != self.id:
            self.friends.append(friend)
            self.balance[friend] = 0
            self.balance_name[friend.name] = 0
        
    def update_balance(self, balance: dict):
        for friend, amount in balance.items():
            self.balance[friend] = self.balance[friend] + amount
    
    def update_balance_name(self, balance):
        for friend, amount in balance.items():
            self.balance_name[friend.name] += amount
            
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
        self.balance_name[friend.name] -= amount
        
    def receive(self, friend, amount):
        self.balance_name[friend] += amount

## ENGINE CLASSES

class EasySplit(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        self.user_name = 'default'
        self.user = User('default', 'default')
        self.project = Project('default', [])
    

        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Easy Split')
        
        self.geometry("900x700")
        
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MenuPage, MyLedgerPage, BalancePage, AnalyticPage, AccountPage, CreateProjectPage, LogIn, SignUpPage, CreatePersoTransac, ProjectListPage, ProjectPage, FriendsPage, CreateTransacPage, SavingPage):

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


class MenuPage(tk.Frame):
    
    def clear_canvas(self):
        self.canvas.destroy()
        self.canvas = Canvas(self, bg = 'SteelBlue2')
        self.canvas.pack(side = LEFT, anchor=N,  expand = YES, fill = BOTH)
    
    def show_user_info(self, controller):
        self.clear_canvas()
        sublabel = tk.Label(self.canvas, text="Username: " + controller.user.name, anchor="w", font=SMALL_FONT,  bg = 'SteelBlue2')
        sublabel.pack(pady=10,padx=10)
        
        sublabel1 = tk.Label(self.canvas, text="Email: " + controller.user.email, anchor="w", font=SMALL_FONT,  bg = 'SteelBlue2')
        sublabel1.pack(pady=10,padx=10)
        
        user_login = shelve.open('user_login')

        sublabel2 = tk.Label(self.canvas, text="Password: " + str(user_login[str(controller.user.name)]), anchor="w", font=SMALL_FONT,  bg = 'SteelBlue2')
        sublabel2.pack(pady=10,padx=10)
        
        user_login.close()
        
        button = tk.Button(self.canvas, text="Change information",
                            command=lambda: controller.show_frame(AccountPage), bg = 'light sky blue')
        button.pack(pady =5, padx = 5, side = TOP, anchor = N)
     

    def update(self, controller):
        self.clear_canvas()
        text_box = Text(self.canvas, state=DISABLED, bg = 'SteelBlue2')
        text_box.pack(side = TOP, fill = X, expand = YES)
        text_box.config(state=NORMAL)
        text_box.insert("end", 'Update in progress...')
        text_box.see("end")
        text_box.config(state=DISABLED)
        user_database = shelve.open('user_database')
        controller.user = user_database[controller.user_name]
        user_database.close()
        text_box.config(state=NORMAL)
        text_box.insert("end", '\nUpdated!')
        text_box.see("end")
        text_box.config(state=DISABLED)
    
    def show_friends(self, controller):
        controller.frames[FriendsPage].update_friends(controller)
        controller.show_frame(FriendsPage)
        
    def show_balance(self, controller):
        controller.frames[BalancePage].reveal(controller)
        controller.show_frame(BalancePage)
        
    def create_project(self, controller):
        controller.frames[CreateProjectPage].update(controller)
        controller.show_frame(CreateProjectPage)
    
    def project_list(self, controller):
        controller.frames[ProjectListPage].update(controller)
        controller.frames[ProjectListPage].show_list(controller)
        controller.show_frame(ProjectListPage)
    
    def show_analytics(self, controller):
        controller.frames[AnalyticPage].update(controller)
        controller.show_frame(AnalyticPage)
    
    def logout(self, controller):
        
        user_database = shelve.open('user_database')
        user_database[controller.user_name] = controller.user
        for name in user_database:
            user_database[name] = user_database[name]
        user_database.close()
        controller.user_name = 'default'
        controller.user = User('default', 'default')
        actEntry.delete(0, END)
        pinEntry.delete(0, END)
        controller.frames[LogIn].text_box.config(state=NORMAL)
        controller.frames[LogIn].text_box.delete('1.0', END)
        controller.frames[LogIn].text_box.see("end")
        controller.frames[LogIn].text_box.config(state=DISABLED)
        controller.show_frame(LogIn)
    

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self,parent, bg = 'SteelBlue1')
        
        label = tk.Label(self, text="MENU", font=LARGE_FONT, bg = 'SteelBlue1')
        label.pack(pady=10,padx=10, anchor=NW)
        
        canvas1 = Canvas(self, bg = 'SteelBlue1')
        canvas1.pack(side = LEFT, anchor=NW, fill = Y)
        
        self.canvas = Canvas(self, bg = 'SteelBlue2')
        self.canvas.pack(side = LEFT, anchor=N,  expand = YES, fill = BOTH)

        
        button1 = tk.Button(canvas1, text="Account\nInformation",
                            command=lambda: self.show_user_info(controller), bg='light sky blue')
        button1.pack(pady =3, padx = 5, side = TOP, anchor = NW, fill = X)
        
        button9 = tk.Button(canvas1, text="Other users",
                            command=lambda: self.show_friends(controller), bg='light sky blue')
        button9.pack(pady =3, padx = 5, side = TOP, anchor = NW, fill = X)
        
        button3 = tk.Button(canvas1, text="Create a Project",
                            command=lambda: self.create_project(controller), bg='light sky blue')
        button3.pack(pady =3, padx = 5, side = TOP, anchor = NW, fill = X)

        button4 = tk.Button(canvas1, text="My Projects",
                           command=lambda: self.project_list(controller), bg='light sky blue')
        button4.pack(pady =3, padx = 5, side = TOP, anchor = NW, fill = X)
        
        button2 = tk.Button(canvas1, text="My Balance",
                            command=lambda: self.show_balance(controller), bg='light sky blue')
        button2.pack(pady =3, padx = 5, side = TOP, anchor = NW, fill = X)

        button5 = tk.Button(canvas1, text="My Ledger",
                            command=lambda: controller.show_frame(MyLedgerPage), bg='light sky blue')
        button5.pack(pady =3, padx = 5, side = TOP, anchor = NW, fill = X)
        
        button6 = tk.Button(canvas1, text="My stats",
                            command=lambda: controller.show_frame(AnalyticPage), bg='light sky blue')
        button6.pack(pady =3, padx = 5, side = TOP, anchor = NW, fill = X)
        
        button7 = tk.Button(canvas1, text='Update', command=lambda: self.update(controller), bg='light sky blue')
        button7.pack(pady =3, padx = 5, side = TOP, anchor = NW, fill = X)
        
        
        button8 = tk.Button(canvas1, text='Log out', command=lambda: self.logout(controller), bg='light salmon')
        button8.pack(ipadx= 1, pady =3, padx = 5, side = BOTTOM, anchor = SW)


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
                
            emailLabel = tk.Label(canvas, text="Current Email: " + str(controller.user.email), anchor="w", font=SMALL_FONT,  bg = 'SteelBlue2')
            emailLabel.pack(pady=10,padx=10)
            
            newEmailEntry = Entry(canvas, width=50)
            newEmailEntry.pack(side = TOP)
            
            EmailButton = tk.Button(canvas, text="Change email",
                            command=lambda: self.change_email(newEmailEntry.get(), controller))
            EmailButton.pack(pady =5, padx = 5, side = TOP, anchor = N)
            
            self.email_text_box = Text(canvas, height = 1, state=DISABLED, bg='SteelBlue2')
            self.email_text_box.pack(pady =5, padx = 5, side = TOP, anchor = N, fill=X)
            
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


class MyLedgerPage(tk.Frame):

    global amountEntry
    global descriptionEntry
    
    def transaction_list(self, controller):
        transactions = controller.user.persoExp.return_transactions()
        if not transactions.empty:
            self.text_box.config(state=NORMAL)
            self.text_box.delete('1.0', END)
            self.text_box.insert("end", str(transactions))
            self.text_box.see("end")
            self.text_box.config(state=DISABLED)
        else:
            self.text_box.config(state=NORMAL)
            self.text_box.delete('1.0', END)
            self.text_box.insert("end", 'You have not yet added any personal expense.')
            self.text_box.see("end")
            self.text_box.config(state=DISABLED)
    
    def weekly_balance(self, controller):
        weekly_balance = controller.user.persoExp.return_weekly_report()
        self.text_box.config(state=NORMAL)
        self.text_box.delete('1.0', END)
        self.text_box.insert("end", str(weekly_balance))
        self.text_box.see("end")
        self.text_box.config(state=DISABLED)
        
    def monthly_balance(self, controller):
        monthly_balance = controller.user.persoExp.return_monthly_report()
        self.text_box.config(state=NORMAL)
        self.text_box.delete('1.0', END)
        self.text_box.insert("end", str(monthly_balance))
        self.text_box.see("end")
        self.text_box.config(state=DISABLED)
        
    def add_expense(self, controller):
        amountEntry.delete(0, END)
        descriptionEntry.delete(0, END)
        controller.show_frame(CreatePersoTransac)
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent, bg = 'SteelBlue1')
        
        label = tk.Label(self, text="My Ledger", font=LARGE_FONT, bg = 'SteelBlue1')
        label.pack(pady=5,padx=10)
        
        output_canvas = Canvas(self, bg = 'SteelBlue1')
        output_canvas.pack()
        
        output_scrollbar = Scrollbar(output_canvas)    
        output_scrollbar.pack(side=RIGHT, fill=Y)
        
        self.text_box = Text(output_canvas, height = 20, width = 80, state=DISABLED, bg = 'SteelBlue1', yscrollcommand=output_scrollbar.set)
        self.text_box.pack(side = TOP, fill = BOTH, expand = YES)
           
        
        output_scrollbar.config(command=self.text_box.yview) 
        self.text_box.config(yscrollcommand=output_scrollbar.set)
        
        button0 = tk.Button(self, text="All expenses",
                           command=lambda: self.transaction_list(controller))
        button0.pack()
        
        button1 = tk.Button(self, text="Weekly balance",
                           command=lambda: self.weekly_balance(controller))
        button1.pack()
        
        button2 = tk.Button(self, text="Monthly balance",
                           command=lambda: self.monthly_balance(controller))
        button2.pack()
        
        button3 = tk.Button(self, text="Add a new transaction",
                           command=lambda: self.add_expense(controller))
        button3.pack()

        button4 = tk.Button(self, text="Back to Menu",
                           command=lambda: controller.show_frame(MenuPage))
        button4.pack(pady=5, padx=5, side = BOTTOM, anchor=SW)


class CreatePersoTransac(tk.Frame):
    
    def create_personal_transaction(self, user, amount, description, category):
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
    
    def add(self, controller, amount, description, category):
        self.create_personal_transaction(controller.user, amount, description, category)
        user_database = shelve.open('user_database')
        user_database[controller.user_name] =  controller.user
        user_database.close()
        controller.show_frame(MyLedgerPage)
        controller.frames[MyLedgerPage].transaction_list(controller)

    
    def __init__(self, parent, controller):
        
        global categories
        global amountEntry
        global descriptionEntry
        
        tk.Frame.__init__(self, parent, bg = 'SteelBlue1')
        
        label = tk.Label(self, text="Add a new personal expense", font=LARGE_FONT, bg = 'SteelBlue1')
        label.pack(pady=10,padx=10)
        
        descriptionrow = Frame(self, bg = 'SteelBlue1')
        descriptionLabel = Label(descriptionrow, text = 'Description: ', anchor='w', bg = 'SteelBlue1')
        descriptionEntry = Entry(descriptionrow)
        descriptionrow.pack(side=TOP, fill=X, padx=5, pady=3)
        descriptionLabel.pack(side = LEFT, anchor = N)
        descriptionEntry.pack(side=RIGHT, expand=YES, fill=X)
        
        amountrow = Frame(self, bg = 'SteelBlue1')
        amountLabel = Label(amountrow, text = 'Amount: ', anchor='w', bg = 'SteelBlue1')
        amountEntry = Entry(amountrow)
        amountrow.pack(side=TOP, fill=X, padx=5, pady=3)
        amountLabel.pack(side = LEFT)
        amountEntry.pack(side=RIGHT, expand=YES, fill=X)
        
        amountEntry.delete(0, END)
        descriptionEntry.delete(0, END)
        
        MODES = []
        for cat in categories:
            MODES.append((cat, cat))
    
        v = StringVar()
        v.set("0")
    
        for text, mode in MODES:
            b = Radiobutton(self, text=text,
                            variable=v, value=mode, bg = 'SteelBlue1')
            b.pack(side = TOP, anchor=W, padx = 30)
                    
        button1 = tk.Button(self, text="Add",
                            command=lambda: self.add(controller, float(amountEntry.get()), str(descriptionEntry.get()), str(v.get())))
        button1.pack()
        
        button2 = tk.Button(self, text="Return",
                            command=lambda: controller.show_frame(MyLedgerPage))
        button2.pack(pady=5, padx=5, side = BOTTOM, anchor=SW) 


class BalancePage(tk.Frame):
    
    def compute_balance(self, controller):
        balance_name = {friend.name: 0 for friend in controller.user.friends}
        project_database = shelve.open('project_database')
        for project_name, project in project_database.items():
            if project.balance_name[controller.user.name] < 0:
                myamount = - project.balance_name[controller.user.name]
                owed = {}
                for person_name, amount in project.balance_name.items():
                    if amount > 0 :
                        owed[person_name] = amount
                while myamount > 0:
                    for owed_person, owed_amount in owed.items() :
                        if owed_amount > myamount :
                            balance_name[owed_person] += myamount
                            myamount = 0
                        if owed_amount <= myamount :
                            balance_name[owed_person] += owed_amount
                            myamount -= owed_amount
                            owed_amount = 0
            if project.balance_name[controller.user.name] > 0:
                myamount = project.balance_name[controller.user.name]
                owers = {}
                user_database = shelve.open('user_database')
                for person_name, amount in project.balance_name.items():
                    if amount < 0 :
                        owers[person_name] = -amount
                while myamount > 0:
                    for owers_person, owers_amount in owers.items() :
                        if owers_amount < myamount :
                            balance_name[owers_person] -= owers_amount
                            myamount -= owers_amount
                        else:
                            balance_name[owed_person] -= myamount
                            myamount = 0
                user_database.close()
        project_database.close()
        controller.user.balance_name = balance_name
        return balance_name
    
    
    def reveal(self, controller):
        self.text_box.config(state=NORMAL)
        self.text_box.delete('1.0', END)
        status = False
        print (self.compute_balance(controller))
        for friend, amount in self.compute_balance(controller).items():
            if amount > 0:
                status = True
                self.text_box.config(state=NORMAL)
                self.text_box.insert("end", "You owe %s: %d \n" % (friend, amount))
                self.text_box.see("end")
                self.text_box.config(state=DISABLED)
            if amount < 0 :
                status = True
                self.text_box.config(state=NORMAL)
                self.text_box.insert("end", "%s owe you: %d \n" % (friend, -amount))
                self.text_box.see("end")
                self.text_box.config(state=DISABLED)
        if not status:
            self.text_box.config(state=NORMAL)
            self.text_box.insert("end", "You owe nothing. \n")
            self.text_box.see("end")
            self.text_box.config(state=DISABLED)
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent, bg = 'SteelBlue1')
        
        self.text_box = Text(self, height = 20, width = 80, state=DISABLED, bg = 'SteelBlue1')
        self.text_box.pack(pady =10, side = TOP, fill = Y, expand = False)
        
        button1 = tk.Button(self, text='Update my balance', command=lambda: self.reveal(controller))
        button1.pack()
        
        button3 = tk.Button(self, text="Back to Menu",
                           command=lambda: controller.show_frame(MenuPage))
        button3.pack(pady=5, padx=5, side = BOTTOM, anchor=SW)


class FriendsPage(tk.Frame):
    
    def update_list_friends(self, controller):
        user_database = shelve.open('user_database')
        friends_name = [friend.name for friend in controller.user.friends]
        for name,friend in user_database.items():
            if name not in friends_name:
                controller.user.add_friends(friend)
        user_database.close()
        self.update_friends(controller)
        
    def update_friends(self, controller):
        self.frame.destroy()
        self.frame = tk.Frame(self.canvas, relief=SUNKEN, bg = 'SteelBlue1')
        self.frame.pack()
        for friend in controller.user.friends:
            label = tk.Label(self.frame, text=friend.name, font=('Verdana', 12), bg = 'SteelBlue1')
            label.pack(pady=5,padx=10)
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent, bg = 'SteelBlue1')
        
        label = tk.Label(self, text="Other users", font=LARGE_FONT, bg = 'SteelBlue1')
        label.pack(pady=5,padx=10)
        
        sublabel = tk.Label(self, text="You are not alone", font=('Arial', 10), bg = 'SteelBlue1')
        sublabel.pack(pady=10,padx=10)
        
        self.canvas = Canvas(self, relief=SUNKEN, bg = 'SteelBlue1')
        self.canvas.pack()
        self.frame = tk.Frame(self.canvas, bg = 'SteelBlue1')
        self.frame.pack()
        
        button4 = tk.Button(self, text="Back to Menu",
                           command=lambda: controller.show_frame(MenuPage))
        button4.pack(padx=5, pady=5, side = BOTTOM, anchor=SW)
        
        button5 = tk.Button(self, text="Update friends",
                           command=lambda: self.update_list_friends(controller))
        button5.pack(padx=5, pady=5, side = BOTTOM, anchor=SW)


class AnalyticPage(tk.Frame):

    global categories
    
    def update(self, controller):
        self.plotcanvas.destroy()
        self.plotcanvas = Canvas(self.reportcanvas, height = 15, bg = 'SteelBlue1')
        self.plotcanvas.pack() 
    
    
    def month(self, controller, month, year):
        self.update(controller)
        M=get_reports_monthly(controller.user, month, year)
        user_database = shelve.open('user_database')
        user_database[controller.user_name] =  controller.user
        f=Figure(figsize=(5,5),dpi=100)
        a=f.add_subplot(111)
        user_database.close()
        lists = sorted(M.items()) 
        x, y = zip(*lists)
        width=.25
        a.bar(x,y)
        a.set_xticklabels(x, rotation= 45, fontsize=6)
        canvas=FigureCanvasTkAgg(f,self.plotcanvas)
        canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH, expand=True)
    
    def week(self, controller,month,year):
        self.update(controller)
        (ywe, week, dwe) = datetime.datetime.now().isocalendar()
        transactions=get_reports_weekly(controller.user, month, year)
        user_database = shelve.open('user_database')
        user_database[controller.user_name] =  controller.user
        f=Figure(figsize=(5,4),dpi=100)
        a=f.add_subplot(111)
        user_database.close()  
        y = []
        for i in transactions.values():
            y.append(sum(i.values()))
        x = []    
        for i in transactions.keys():
            x.append(i)
        print(x)    
        width=.25
        a.bar(x,y)
        a.set_xticklabels(x, rotation= 45 )     
        canvas=FigureCanvasTkAgg(f,self.plotcanvas)
        canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH, expand=True)    
        

    def __init__(self, parent, controller):
        
        global categories
        global months
        global MonthEntry
        global YearEntry
        
        months_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        years_list = [2017, 2018, 2019]
        tk.Frame.__init__(self, parent, bg = 'SteelBlue1')
        
        label = tk.Label(self, text="Analytics", font=LARGE_FONT, bg = 'SteelBlue1')
        label.pack(pady=10,padx=10)
        
        label = tk.Label(self, text="Get Expenditure report", font=SMALL_FONT, bg = 'SteelBlue1')
        label.pack(pady=10,padx=10)
        
        buttoncanvas = Canvas(self, bg = 'SteelBlue1')
        buttoncanvas.pack()
        
        button3 = tk.Button(buttoncanvas, text="Return",
                            command=lambda: controller.show_frame(MenuPage))
        button3.pack(side=LEFT, anchor=NW)

        button1 = tk.Button(buttoncanvas, text="Get Monthly",
                            command=lambda: self.month(controller, MonthEntry.get(), int(YearEntry.get())))
        button1.pack(padx=5, side=LEFT)
        
        button2 = tk.Button(buttoncanvas, text="Get Weekly",
                            command=lambda: self.week(controller, str(MonthEntry.get()), int(YearEntry.get())))
        button2.pack(padx=5, side=LEFT)
        
        button2 = tk.Button(buttoncanvas, text="Saving suggestions",
                            command=lambda: controller.show_frame(SavingPage))
        button2.pack(padx=5, side=LEFT)
        
        Monthrow = Frame(self, width = 25, bg = 'SteelBlue1')
        MonthLabel = Label(Monthrow, text = 'Choose Month', anchor='w', bg = 'SteelBlue1')
        Monthrow.pack(side=TOP, padx=5, pady=3)
        MonthLabel.pack(side = LEFT, anchor = N, fill=Y)
        
        MonthEntry = StringVar()
        MonthEntry.set("Jan")
        
        m = OptionMenu(Monthrow, MonthEntry, *months_list)
        m.pack(ipadx=5, side=LEFT)
        
        YearLabel = Label(Monthrow, text = 'Choose Year', anchor='e', bg = 'SteelBlue1')
        YearLabel.pack(ipadx = 10, side = LEFT, fill=Y)
        
        YearEntry = IntVar()
        YearEntry.set(2018)
        year = OptionMenu(Monthrow, YearEntry, *years_list)
        year.pack(ipadx=5, side=LEFT)
        
        self.reportcanvas = Canvas(self, bg = 'SteelBlue1')
        self.reportcanvas.pack()
        
        self.plotcanvas = Canvas(self.reportcanvas, height = 15, bg = 'SteelBlue1')
        self.plotcanvas.pack()        
        
        button3 = tk.Button(self, text="Return",
                            command=lambda: controller.show_frame(MenuPage))
        button3.pack()


class SavingPage(tk.Frame):
    
    
    def reveal(self, controller):
        sug = save_suggestions(controller.user, str(MonthEntry.get()), int(YearEntry.get()), profileEntry.get(), int(amountSaveEntry.get()))
        print (sug)
        self.text_box.config(state=NORMAL)
        self.text_box.delete('1.0', END)
        self.text_box.insert("end", str(sug))
        self.text_box.see("end")
        self.text_box.config(state=DISABLED)
    
    
    def __init__(self, parent, controller):
        
        profiles_list = ['student', 'Working>50000', 'Working<50000']
        
        global profileEntry
        global amountSaveEntry
        
        tk.Frame.__init__(self, parent, bg = 'SteelBlue1')
        
        amountSaverow = Frame(self, bg = 'SteelBlue1')
        amountSaveLabel = Label(amountSaverow, text = 'Amount: ', anchor='w', bg = 'SteelBlue1')
        amountSaveEntry = Entry(amountSaverow)
        amountSaverow.pack(side=TOP, fill=X, padx=5, pady=3)
        amountSaveLabel.pack(side = LEFT)
        amountSaveEntry.pack(side=RIGHT, expand=YES, fill=X)
        
        profilerow = Frame(self, width = 25, bg = 'SteelBlue1')
        profileLabel = Label(profilerow, text = 'Choose profile', anchor='w', bg = 'SteelBlue1')
        profilerow.pack(side=TOP, padx=5, pady=3)
        profileLabel.pack(side = LEFT, anchor = N, fill=Y)
        
        profileEntry = StringVar()
        profileEntry.set("student")
        
        m = OptionMenu(profilerow, profileEntry, *profiles_list)
        m.pack(ipadx=5, side=LEFT)
        
        self.text_box = Text(self, height = 20, width = 80, state=DISABLED, bg = 'SteelBlue1')
        self.text_box.pack(pady =10, side = TOP, fill = Y, expand = False)
        
        button1 = tk.Button(self, text='Give me suggestions', command=lambda: self.reveal(controller))
        button1.pack()
        
        button3 = tk.Button(self, text="Back to Menu",
                           command=lambda: controller.show_frame(MenuPage))
        button3.pack(pady=5, padx=5, side = BOTTOM, anchor=SW)


class Checkbar(tk.Frame):
   
   def __init__(self, parent, picks=[], side=LEFT, anchor=W):
      tk.Frame.__init__(self, parent, bg = 'SteelBlue2')
      self.vars = []
      for pick in picks:
         var = StringVar()
         var.set('0')
         chk = Checkbutton(self, text=pick, variable=var, onvalue = pick, offvalue = '0', bg = 'SteelBlue2')
         chk.pack(side=TOP, anchor=anchor, expand=YES)
         self.vars.append(var)
   
   def state(self):
      return list(map((lambda var: var.get()), self.vars))


class CreateProjectPage(tk.Frame):

    def add(self, controller, project_name, friends_name_list):
        if friends_name_list == ['0' for i in range(len(friends_name_list))]:
            self.text_box.config(state=NORMAL)
            self.text_box.delete('1.0', END)
            self.text_box.insert("end", "Please select a friend.")
            self.text_box.see("end")
            self.text_box.config(state=DISABLED)
        
        if project_name == '' :
            self.text_box.config(state=NORMAL)
            self.text_box.delete('1.0', END)
            self.text_box.insert("end", "Please name your project.")
            self.text_box.see("end")
            self.text_box.config(state=DISABLED)
        
        if friends_name_list != ['0' for i in range(len(friends_name_list))] and project_name != '' :
            friends_list = []
            user_database = shelve.open('user_database')
            for name in friends_name_list:
                if name != '0' :
                    friends_list.append(user_database[str(name)])
            user_database.close()
            friends_list.append(controller.user)
            
            project = Project(project_name, friends_list)
            project_database = shelve.open('project_database')
            
            if project_name in project_database:
                self.text_box.config(state=NORMAL)
                self.text_box.delete('1.0', END)
                self.text_box.insert("end", "The name is taken.")
                self.text_box.see("end")
                self.text_box.config(state=DISABLED)
                
            else:
                project_database = shelve.open('project_database')
                project_database[project.project_name] = project
                project_database.close()
        
                print('Project created')
                
                user_database = shelve.open('user_database')
                
                for friend in friends_list:
                    friend.add_project(project)
                    user_database[friend.name] = friend
                
                print('Project added to users')
    
            user_database.close()
            project_database.close()
            
            controller.set_project(project.project_name)
            controller.frames[ProjectPage].update_label(controller)
            controller.show_frame(ProjectPage)

    def update(self, controller):
        projectNameEntry.delete(0, END)
        self.friendCanvas.destroy()
        self.friendCanvas = Canvas(self.canvas, bg = 'SteelBlue2')
        self.friendCanvas.pack(side = TOP)
        self.status = False
        self.choose_friends(controller)
    
    def choose_friends(self, controller):
        if not self.status:
            BFF = []
            friend_name_list = []
            for friend in controller.user.friends:
                BFF.append((friend.name, friend.name))
                friend_name_list.append(friend.name)

            self.checkboxList = Checkbar(self.friendCanvas, friend_name_list)
            self.checkboxList.pack()

            self.status = True
    
    def __init__(self, parent, controller):
        
        global projectNameEntry
        
        self.status = False
        
        tk.Frame.__init__(self, parent, bg = 'SteelBlue2')
        
        label = tk.Label(self, text="Create new project", font=LARGE_FONT, bg = 'SteelBlue2')
        label.pack(pady=10,padx=10)
        
        projectNameRow = Frame(self, bg = 'SteelBlue2')
        projectNameLabel = Label(projectNameRow, text = 'Project name: ', anchor='w', bg = 'SteelBlue2')
        projectNameEntry = Entry(projectNameRow)
        projectNameRow.pack(side=TOP, fill=X, padx=5, pady=3)
        projectNameLabel.pack(side = LEFT, anchor = N)
        projectNameEntry.pack(side=RIGHT, expand=YES, fill=X)
        
        projectNameEntry.delete(0, END)
        
        label = tk.Label(self, text="Choose friends", font=SMALL_FONT, bg = 'SteelBlue2')
        label.pack(pady=10,padx=10)
        
        self.canvas = Canvas(self, bg = 'SteelBlue2')
        self.canvas.pack(side=TOP)
        
        self.friendCanvas = Canvas(self.canvas, bg = 'SteelBlue2')
        self.friendCanvas.pack(side = TOP)
        
        button2 = tk.Button(self, text="Create the project",
                            command=lambda: self.add(controller, projectNameEntry.get(), self.checkboxList.state()))
        button2.pack(pady=10)
        
        self.text_box = Text(self, height = 1, width = 30, state=DISABLED, bg='SteelBlue2')
        self.text_box.pack(pady =10, side = TOP, fill = Y, expand = False)
        
        button3 = tk.Button(self, text="Return",
                            command=lambda: controller.show_frame(MenuPage))
        button3.pack(pady=5, padx=5, side = BOTTOM, anchor=SW)


class ProjectListPage(tk.Frame):
    
    def clear_canvas(self):
        self.main_canvas.destroy()
        self.main_canvas = Canvas(self.canvas, bg = 'SteelBlue2')
        self.main_canvas.pack(fill=X, expand=YES)
    
    def update(self, controller):
        self.clear_canvas()
        self.status = False
        self.show_list(controller)
        
    def show_project(self, controller, project):
        controller.set_project(project.project_name)
        controller.frames[ProjectPage].update_label(controller)
        controller.frames[ProjectPage].transaction_list(controller)
        controller.show_frame(ProjectPage)
    
    def show_list(self, controller):
        if not self.status:
            if controller.user.user_projects != []:
                self.buttons = []
                for project in controller.user.user_projects :
                    row = tk.Frame(self.main_canvas, height = 30, bg = 'SteelBlue2', relief=RIDGE)
                    row.pack(fill = X, side=TOP, pady=2)
                    self.buttons.append(tk.Button(row, text=str(project.project_name),
                                command=lambda c=controller, p=project: self.show_project(c, p), width = 25, bg = 'SteelBlue3'))
                    self.buttons[-1].pack(side = LEFT)
                    user_list_text = ' |  '
                    for user in project.project_users:
                        user_list_text += str(user.name) + '  |  '
                    label = tk.Label(row, text=str(user_list_text), font=("Arial", 9), width = 40, bg = 'SteelBlue2', relief=RIDGE)
                    label.pack(ipady=2, side = LEFT, fill=X, expand=YES)
            else:
                row = tk.Frame(self.main_canvas, height = 30, relief=RIDGE, bg = 'SteelBlue2')
                row.pack(fill = X, side=TOP)
                label = tk.Label(row, text='You currently have no project.', font=("Arial", 9), width = 40, bg = 'SteelBlue2', relief=RIDGE)
                label.pack(ipady=2, side = TOP, fill=X, expand=YES)
            self.status = True

    def __init__(self, parent, controller):
        
        self.status = False
        
        tk.Frame.__init__(self, parent, bg = 'SteelBlue2')
        
        label = tk.Label(self, text="Choose a project", font=LARGE_FONT, bg = 'SteelBlue2')
        label.pack(pady=8,padx=10)

        sublabel = tk.Label(self, text="click on name", font=("Arial", 10), bg = 'SteelBlue2')
        sublabel.pack(pady=7,padx=10)
        
        self.canvas = Canvas(self, bg = 'SteelBlue2')
        self.canvas.pack()
        
        self.main_canvas = Canvas(self.canvas, bg = 'SteelBlue2')
        self.main_canvas.pack(fill=X, expand=YES)
        
        scrollbar = Scrollbar(self.main_canvas)    
        scrollbar.pack(side=RIGHT, fill=Y) 
        
        scrollbar.config(command=self.main_canvas.yview) 
        self.main_canvas.config(yscrollcommand=scrollbar.set) 
                    
        button2 = tk.Button(self, text="Return",
                            command=lambda: controller.show_frame(MenuPage))
        button2.pack(pady=5, padx=5, side = BOTTOM, anchor=SW)


class ProjectPage(tk.Frame):
    
    def update_label(self, controller):
        text1 = str(controller.project.project_name)
        user_list_text = ' |  '
        for user in controller.project.project_users:
            user_list_text += str(user.name) + '  |  '
        self.label.destroy()
        self.sublabel.destroy()
        self.balanceLabel.destroy()
        self.label = tk.Label(self.label_row, text=text1, font=LARGE_FONT, bg = 'SteelBlue2')
        self.label.pack(pady=8,padx=10)
        self.sublabel = tk.Label(self.label_row, text= user_list_text, font=('Arial', 10), bg = 'SteelBlue2')
        self.sublabel.pack(pady=1,padx=10)
        self.balanceLabel = tk.Label(self.canvas1, text=str(controller.project.balance_name), font=('Arial', 10), bg = 'SteelBlue2')
        self.balanceLabel.pack(side = TOP, fill=Y)
    
    def back(self, controller):
        project_database = shelve.open('project_database')
        project_database[controller.project.project_name] = controller.project
        project_database.close()
        controller.project  = Project('default', [])
        controller.show_frame(ProjectListPage)
        
    def add_transac(self, controller):
        controller.frames[CreateTransacPage].update(controller)
        controller.show_frame(CreateTransacPage)
    
    def transaction_list(self, controller):
        transactions = controller.project.return_transactions()
        if not transactions.empty:
            self.ledger_box.config(state=NORMAL)
            self.ledger_box.delete('1.0', END)
            self.ledger_box.insert("end", str(transactions))
            self.ledger_box.see("end")
            self.ledger_box.config(state=DISABLED)
        else:
            self.ledger_box.config(state=NORMAL)
            self.ledger_box.delete('1.0', END)
            self.ledger_box.insert("end", 'You have not yet added any personal expense.')
            self.ledger_box.see("end")
            self.ledger_box.config(state=DISABLED)
    
    def __init__(self, parent, controller):
        
        self.status = False
        
        tk.Frame.__init__(self, parent, bg = 'SteelBlue2')
        
        self.label_row = Canvas(self, bg = 'SteelBlue2')
        self.label_row.pack(fill=X, ipady=5)
        
        self.label = tk.Label(self.label_row, text= 'default', font=LARGE_FONT, bg = 'SteelBlue2')
        self.label.pack(pady=8,padx=10)
        
        self.sublabel = tk.Label(self.label_row, text= 'default', font=LARGE_FONT, bg = 'SteelBlue2')
        self.sublabel.pack(pady=5,padx=10)

        sublabel1 = tk.Label(self, text="Balance of the project", font=SMALL_FONT, bg = 'SteelBlue2')
        sublabel1.pack(pady=3,padx=10)

        self.canvas1 = Canvas(self, height = 30, bg = 'SteelBlue2')
        self.canvas1.pack(pady=5, side=TOP, fill=X, ipadx=8)
        
        self.balanceLabel = tk.Label(self.canvas1, text=" ", font=SMALL_FONT, bg = 'SteelBlue2')
        self.balanceLabel.pack(side = TOP, fill=Y, expand=YES)
        
        sublabel2 = tk.Label(self, text="Project Ledger", font=SMALL_FONT, bg = 'SteelBlue2')
        sublabel2.pack(pady=7,padx=10)
        
        self.canvas2 = Canvas(self, height = 12, bg = 'SteelBlue2')
        self.canvas2.pack(side=TOP, fill=X)

        scrollbar = Scrollbar(self.canvas2)    
        scrollbar.pack(side=RIGHT, fill=Y) 
        
        scrollbar.config(command=self.canvas2.yview) 
        self.canvas2.config(yscrollcommand=scrollbar.set) 
        
        self.ledger_box = Text(self.canvas2, height=15, width=110, state=DISABLED, bg = 'SteelBlue2')
        self.ledger_box.pack(fill=Y, expand=YES)
        
        button = tk.Button(self, text="See transactions",
                            command=lambda: self.transaction_list(controller))
        button.pack(pady=5, padx=5, side = TOP, anchor=N)
        
        button1 = tk.Button(self, text="Add transaction",
                            command=lambda: self.add_transac(controller))
        button1.pack(pady=5, padx=5, side = TOP, anchor=N)
                    
        button2 = tk.Button(self, text="Return",
                            command=lambda: self.back(controller))
        button2.pack(pady=5, padx=5, side = BOTTOM, anchor=SW)
    

class CreateTransacPage(tk.Frame):
    
    def create_transaction(self, controller, amount, people, payer, method, description, category, *args):
        date = datetime.datetime.now().strftime("%m-%d-%y-%H-%M")
        hash_ident = str(date) + str(amount)
        transac_id = hash(hash_ident)
        people_name = []
        S=[]
        for i in args:
            print(i)
            for j in i:
                print(j)
                S.append(float(j))
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
            self.balance = balance
            
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
            self.balance = balance
        
        controller.project.update_balance_name(self.balance)
                
        transac = pd.DataFrame({"project_id": controller.project.id, 
                                "transac_id": transac_id,
                                "date": date, 
                                "total_amount": amount, 
                                "people_name": [people_name],
                                "payer_name": payer.name, 
                                "method": method, 
                                "description": description,
                                "category": category,
                                "Split": [Split]})
        controller.project.add_transaction(transac)
        project_database = shelve.open('project_database')
        project_database[controller.project.project_name] = controller.project
        project_database.close()  
        
    def add_unequal(self, controller):
        people_names = self.checkboxList.state()
        payer_name = self.payer.get()
        method = self.method.get()
        category_name = self.category.get()        
        
        if method == 'unequal':
            if people_names != ['0' for i in range(len(people_names))]:
                people = []
                user_database = shelve.open('user_database')
                for name in people_names:
                    if name != '0' :
                        people.append(user_database[name])
                user_database.close()
            
            if payer_name != '0':
                user_database = shelve.open('user_database')
                payer = user_database[payer_name]
                user_database.close()
                
            if category_name != '0':
                category = category_name
            
            if self.checksplit():
                split = ()
                for i in self.splitEntry:
                    if float(i.get()) != 0 :
                        split += (float(i.get()),)
                print(split)
                
                self.create_transaction(controller, float(amount2Entry.get()), people, payer, method, description2Entry.get(), category, split)
                project_database = shelve.open('project_database')
                project_database[controller.project.project_name] = controller.project
                project_database.close()
                
                print('Transac added')
                controller.show_frame(ProjectPage)    
                controller.frames[ProjectPage].transaction_list(controller)
                controller.frames[ProjectPage].update_label(controller)

    def checksplit(self):
        sum = 0
        for i in self.splitEntry:
            sum += float(i.get())
        if sum == float(amount2Entry.get()):
            return True
        else:
            for i in self.splitEntry:
                i.delete(0, END)
            return False
    
    def add_equal(self, controller):
        people_names = self.checkboxList.state()
        payer_name = self.payer.get()
        method = self.method.get()
        category_name = self.category.get()        
        
        if method == 'equal':
            if people_names != ['0' for i in range(len(people_names))]:
                people = []
                user_database = shelve.open('user_database')
                for name in people_names:
                    if name != '0' :
                        people.append(user_database[name])
                user_database.close()
            
            if payer_name != '0':
                user_database = shelve.open('user_database')
                payer = user_database[payer_name]
                user_database.close()
                
            if category_name != '0':
                category = category_name
            
            self.create_transaction(controller, float(amount2Entry.get()), people, payer, method, description2Entry.get(), category)
            project_database = shelve.open('project_database')
            project_database[controller.project.project_name] = controller.project
            project_database.close()
            
            print('Transac added')
            controller.show_frame(ProjectPage)    
            controller.frames[ProjectPage].transaction_list(controller)
            controller.frames[ProjectPage].update_label(controller)
        
        if method == 'unequal':
            self.show_splitcanvas(controller)
            self.show_unequalbutton(controller)
    
    def update(self, controller):
        self.update_entries(controller)
        self.update_userscanvas(controller)
        self.show_equalbutton(controller)
    
    def update_entries(self, controller):
        amount2Entry.delete(0, END)
        description2Entry.delete(0, END)
    
    def update_userscanvas(self, controller):
        self.peoplecanvas.destroy()
        self.payercanvas.destroy()
        self.methodcanvas.destroy()
        self.splitcanvas.destroy()
        
        self.peoplecanvas = Canvas(self.userscanvas, height =8, bg = 'SteelBlue2')
        self.peoplecanvas.pack(side=TOP, fill=X, ipady=2, ipadx=2, anchor=N)
        
        self.peoplestatus = False
        
        self.payercanvas = Canvas(self.userscanvas, height = 3, bg = 'SteelBlue2')
        self.payercanvas.pack(side=TOP, fill=X, ipady=2, ipadx=2, anchor=N)
        
        self.payerstatus = False
        
        self.methodcanvas = Canvas(self.userscanvas, height = 3, bg = 'SteelBlue2')
        self.methodcanvas.pack(side=TOP, fill=X, ipady=2, ipadx=2, anchor=N)
        
        self.methodstatus = False
        
        self.splitcanvas = Canvas(self.userscanvas, height = 8, bg = 'SteelBlue2')
        self.splitcanvas.pack(side=TOP, fill=X, ipady=2, ipadx=2, anchor=N)
        
        self.splitstatus = False
        
        self.show_userscanvas(controller)
    
    def show_unequalbutton(self, controller):
        self.button1.destroy()
        self.button1 = tk.Button(self.buttoncanvas, text="Confirm",
                            command=lambda: self.add_unequal(controller))
        self.button1.pack()
        
    def show_equalbutton(self, controller):
        self.button1.destroy()
        self.button1 = tk.Button(self.buttoncanvas, text="Add",
                            command=lambda: self.add_equal(controller))
        self.button1.pack()
    
    def show_splitcanvas(self, controller):
        if not self.splitstatus:
            people_name = self.checkboxList.state()
            self.splitEntry = []
            for name in people_name:
                if name != '0':
                    splitrow = Frame(self.splitcanvas, bg = 'SteelBlue2')
                    splitLabel = Label(splitrow, text = str(name) + ': ', anchor='w', bg = 'SteelBlue2')
                    self.splitEntry.append(Entry(splitrow))
                    splitrow.pack(side=TOP, fill=X, padx=5, pady=3)
                    splitLabel.pack(side = LEFT, anchor = N)
                    self.splitEntry[-1].pack(side=RIGHT, expand=YES, fill=X)
            self.splitstatus = True
    
    def show_userscanvas(self, controller):
        self.show_people(controller)
        self.show_payer(controller)
        self.show_method(controller)
    
    def show_people(self, controller):
        if not self.peoplestatus:
            label = Label(self.peoplecanvas, text='Select the involved users', font=SMALL_FONT, bg = 'SteelBlue2')
            label.pack(pady=5, side=TOP)
            sharers = []
            users_name_list = []
            for user in controller.project.project_users:
                sharers.append((user.name, user.name))
                users_name_list.append(user.name)

            self.checkboxList = Checkbar(self.peoplecanvas, users_name_list)
            self.checkboxList.pack(side=TOP)
            self.peoplestatus = True
    
    def show_payer(self, controller):
        if not self.payerstatus:
            label = Label(self.payercanvas, text='Select the payer', font=SMALL_FONT, bg = 'SteelBlue2')
            label.pack(pady=5, side=TOP)
            payers = []
            for user in controller.project.project_users:
                payers.append((user.name, user.name))
        
            self.payer = StringVar()
            self.payer.set("0")
            
            for text, mode in payers:
                c = Radiobutton(self.payercanvas, text=text,
                                variable=self.payer, value=mode, bg = 'SteelBlue2')
                c.pack(side = TOP)
            self.payerstatus = True
    
    def show_method(self, controller):
        if not self.methodstatus:
            label = Label(self.methodcanvas, text='Select the split method', font=SMALL_FONT, bg = 'SteelBlue2')
            label.pack(pady=5, side=TOP)
            methods = [('equal', 'equal'),('unequal', 'unequal')]
            
            self.method = StringVar()
            self.method.set("0")
            
            for text, mode in methods:
                c = Radiobutton(self.methodcanvas, text=text,
                                variable=self.method, value=mode, bg = 'SteelBlue2')
                c.pack(side = TOP)
            self.methodstatus = True
    
    def __init__(self, parent, controller):
        
        global categories
        global amount2Entry
        global description2Entry
        
        
        tk.Frame.__init__(self, parent, bg = 'SteelBlue2')
        
        label = tk.Label(self, text="Add a new transaction", font=LARGE_FONT, bg = 'SteelBlue2')
        label.pack(pady=10,padx=10)
        
        description2row = Frame(self, bg = 'SteelBlue2')
        description2Label = Label(description2row, text = 'Description: ', anchor='w', bg = 'SteelBlue2')
        description2Entry = Entry(description2row)
        description2row.pack(side=TOP, fill=X, padx=5, pady=3)
        description2Label.pack(side = LEFT, anchor = N)
        description2Entry.pack(side=RIGHT, expand=YES, fill=X)
        
        amount2row = Frame(self, bg = 'SteelBlue2')
        amount2Label = Label(amount2row, text = 'Amount: ', anchor='e', bg = 'SteelBlue2')
        amount2Entry = Entry(amount2row)
        amount2row.pack(side=TOP, fill=X, padx=5, pady=3)
        amount2Label.pack(ipadx= 8, side = LEFT)
        amount2Entry.pack(side=RIGHT, expand=YES, fill=X)
        
        amount2Entry.delete(0, END)
        description2Entry.delete(0, END)
        
        categorycanvas = Canvas(self, height = 8, bg = 'SteelBlue2')
        categorycanvas.pack(pady=5)
    
        frame = tk.Frame(categorycanvas, bg = 'SteelBlue2')
        frame.pack()
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        
        
        radiocanvas = Canvas(frame, bg = 'SteelBlue2')
        radiocanvas.grid(row=0, column=0, ipady=2, ipadx=2)
        
        catLabel = Label(radiocanvas, text = 'Category:', bg = 'SteelBlue2')
        catLabel.pack(side = TOP, anchor = W)
        
        MODES = []
        for cat in categories:
            MODES.append((cat, cat))
    
        self.category = StringVar()
        self.category.set("0") # initialize
    
        for text, mode in MODES:
            b = Radiobutton(radiocanvas, text=text,
                            variable=self.category, value=mode, bg = 'SteelBlue2')
            b.pack(side = TOP, anchor=W)
                    
        
        self.balance = {}
        
        self.userscanvas = Canvas(frame, bg = 'SteelBlue2')
        self.userscanvas.grid(row=0, column=1)
        
        self.peoplecanvas = Canvas(self.userscanvas, height =8, bg = 'SteelBlue2')
        self.peoplecanvas.pack(side=TOP)
        
        self.peoplestatus = False
        
        self.payercanvas = Canvas(self.userscanvas, height = 3, bg = 'SteelBlue2')
        self.payercanvas.pack(side=TOP)
        
        self.payerstatus = False
        
        self.methodcanvas = Canvas(self.userscanvas, height = 3, bg = 'SteelBlue2')
        self.methodcanvas.pack(side=TOP)
        
        self.methodstatus = False
        
        self.splitcanvas = Canvas(self.userscanvas, height = 8, bg = 'SteelBlue2')
        self.splitcanvas.pack(side=TOP)
        
        self.splitstatus = False
        
        
        self.buttoncanvas = Canvas(self)
        self.buttoncanvas.pack()
        
        self.button1 = tk.Button(self.buttoncanvas, text="Add",
                            command=lambda: self.add_equal(controller))
        self.button1.pack()
        
        button2 = tk.Button(self, text="Return",
                            command=lambda: controller.show_frame(ProjectPage))
        button2.pack(pady=5, padx=5, side = BOTTOM, anchor=SW)


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
        

## MAIN

if __name__ == "__main__":
    app = EasySplit()
    app.mainloop()

