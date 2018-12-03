## ENGINE CLASSES

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
        text_box.pack(side = TOP, fill = Y, expand = YES)
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
    
    def logout(self, controller):
        
        user_database = shelve.open('user_database')
        user_database[controller.user_name] = controller.user
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
        
        button2 = tk.Button(canvas1, text="My Balance",
                            command=lambda: self.show_balance(controller), bg='light sky blue')
        button2.pack(pady =3, padx = 5, side = TOP, anchor = NW, fill = X)
        
        button9 = tk.Button(canvas1, text="Other users",
                            command=lambda: self.show_friends(controller), bg='light sky blue')
        button9.pack(pady =3, padx = 5, side = TOP, anchor = NW, fill = X)
        
        button3 = tk.Button(canvas1, text="Create a Project",
                            command=lambda: self.create_project(controller), bg='light sky blue')
        button3.pack(pady =3, padx = 5, side = TOP, anchor = NW, fill = X)

        button4 = tk.Button(canvas1, text="My Projects",
                           command=lambda: self.project_list(controller), bg='light sky blue')
        button4.pack(pady =3, padx = 5, side = TOP, anchor = NW, fill = X)

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
    
    def add(self, controller, amount, description, category):
        create_personal_transaction(controller.user, amount, description, category)
        user_database = shelve.open('user_database')
        user_database[controller.user_name] =  controller.user
        user_database.close()
        controller.show_frame(MyLedgerPage)
        controller.frames[MyLedgerPage].transaction_list(controller)

    
    def __init__(self, parent, controller):
        
        global categories
        global amountEntry
        global descriptionEntry
        
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Add a new personal expense", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        descriptionrow = Frame(self, bg = 'white')
        descriptionLabel = Label(descriptionrow, text = 'Description: ', anchor='w')
        descriptionEntry = Entry(descriptionrow)
        descriptionrow.pack(side=TOP, fill=X, padx=5, pady=3)
        descriptionLabel.pack(side = LEFT, anchor = N)
        descriptionEntry.pack(side=RIGHT, expand=YES, fill=X)
        
        amountrow = Frame(self, bg='white')
        amountLabel = Label(amountrow, text = 'Amount: ', anchor='w')
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
        v.set("L") # initialize
    
        for text, mode in MODES:
            b = Radiobutton(self, text=text,
                            variable=v, value=mode)
            b.pack(side = TOP, anchor=W)
                    
        button1 = tk.Button(self, text="Add",
                            command=lambda: self.add(controller, float(amountEntry.get()), str(descriptionEntry.get()), str(v.get())))
        button1.pack()
        
        button2 = tk.Button(self, text="Return",
                            command=lambda: controller.show_frame(MyLedgerPage))
        button2.pack(pady=5, padx=5, side = BOTTOM, anchor=SW)
        


class BalancePage(tk.Frame):

    def reveal(self, controller):
        self.text_box.config(state=NORMAL)
        self.text_box.delete('1.0', END)
        status = False
        for friend, amount in controller.user.balance.items():
            if amount > 0:
                status = True
                self.text_box.config(state=NORMAL)
                self.text_box.insert("end", "You owe %s: %d \n" % (friend.name, amount))
                self.text_box.see("end")
                self.text_box.config(state=DISABLED)
            if amount < 0 :
                status = True
                self.text_box.config(state=NORMAL)
                self.text_box.insert("end", "%s owe you: %d \n" % (friend.name, -amount))
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
        
        button2 = tk.Button(self, text='Pay your friends back', command=lambda: controller.show_frame(PaybackPage))
        button2.pack()
        
        button3 = tk.Button(self, text="Back to Menu",
                           command=lambda: controller.show_frame(MenuPage))
        button3.pack(pady=5, padx=5, side = BOTTOM, anchor=SW)
        


class PaybackPage(tk.Frame):
    
    def pay(self, controller, amount, friend_name):
        user_database = shelve.open('user_database')
        friend = user_database[friend_name]
        if controller.user.balance[friend] == 0:
            raise ValueError('You do not owe that person.')
        if amount <= controller.user.balance[friend]:
            controller.user.payback(friend, amount)
            friend.receive(user, amount)
        else:
            raise ValueError('You can not pay back more than what you owe.')
        user_database.close()
        
    def choose_friend(self, controller, canvas1):
        if not self.status:
            BFF = []
            for friend, amount in controller.user.balance.items():
                BFF.append((friend.name, friend.name))
        
            self.v = StringVar()
            self.v.set("")
            
            for text, mode in BFF:
                c = Radiobutton(canvas1, text=text,
                                variable=self.v, value=mode)
                c.pack(side = TOP, anchor=W)
            self.status = True
    
    def __init__(self, parent, controller):
        
        self.status = False
        
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Pay a friend back", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        sublabel = tk.Label(self, text="Choose a friend", font=SMALL_FONT)
        sublabel.pack(pady=10,padx=10)
                
        button = tk.Button(self, text="Choose",
                            command=lambda: self.choose_friend(controller, canvas1))
        button.pack(side = TOP, anchor = N)
        
        canvas1 = Canvas(self, height = 25)
        canvas1.pack(side=TOP)
        
        canvas2 = Canvas(self, height = 5)
        canvas2.pack(side=TOP)
        
        amountFriendLabel = Label(canvas2, text = 'Amount: ', anchor='w')
        amountFriendEntry = Entry(canvas2)
        amountFriendLabel.pack(side = TOP)
        amountFriendEntry.pack(side=RIGHT, expand=YES, fill=X)
        
        button1 = tk.Button(self, text="Pay",
                            command=lambda: self.pay(controller, amountFriendEntry.get(), self.v.get()))
        button1.pack(side = TOP, anchor = N)
        
        button2 = tk.Button(self, text="Return",
                            command=lambda: controller.show_frame(BalancePage))
        button2.pack(pady=5, padx=5, side = BOTTOM, anchor=SW)


class FriendsPage(tk.Frame):
    
    def update_friends(self, controller):
        self.frame.destroy()
        self.frame = tk.Frame(self.canvas, relief=SUNKEN)
        self.frame.pack()
        for friend in controller.user.friends:
            label = tk.Label(self.frame, text=friend.name, font=('Verdana', 12))
            label.pack(pady=5,padx=10)
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Other users", font=LARGE_FONT)
        label.pack(pady=5,padx=10)
        
        sublabel = tk.Label(self, text="You are not alone", font=('Arial', 10))
        sublabel.pack(pady=10,padx=10)
        
        self.canvas = Canvas(self, relief=SUNKEN)
        self.canvas.pack()
        self.frame = tk.Frame(self.canvas)
        self.frame.pack()
        
        
        button4 = tk.Button(self, text="Back to Menu",
                           command=lambda: controller.show_frame(MenuPage))
        button4.pack(padx=5, pady=5, side = BOTTOM, anchor=SW)


class AnalyticPage(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Analytics", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        button4 = tk.Button(self, text="Back to Menu",
                           command=lambda: controller.show_frame(MenuPage))
        button4.pack(padx=5, pady=5, side = BOTTOM, anchor=SW)


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
                    friends_list.append(user_database[name])
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
                project_database[project.project_name] = project
        
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
                print(friend.name)
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
        self.balanceLabel = tk.Label(self.canvas1, text=str(controller.project.print_balance()), font=('Arial', 10), bg = 'SteelBlue2')
        self.balanceLabel.pack(side = TOP, fill=Y)
    
    def back(self, controller):
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
        
        self.ledger_box = Text(self.canvas2, height=15, state=DISABLED, bg = 'SteelBlue2')
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
    
    def add(self, controller):
        people_names = self.checkboxList.state()
        payer_name = self.payer.get()
        method = self.method.get()
        category_name = self.category.get()
        print(method)
        
        
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
            
            create_transaction(controller.project, float(amount2Entry.get()), people, payer, method, description2Entry.get(), category)
            project_database = shelve.open('project_name')
            project_database[controller.project.project_name] = controller.project
            project_database.close()
            
            print('Transac added')
            controller.show_frame(ProjectPage)    
            controller.frames[ProjectPage].transaction_list(controller)
        
        if method == 'unequal':
            self.show_splitcanvas(controller)
    
    def update(self, controller):
        self.update_entries(controller)
        self.update_userscanvas(controller)
    
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
    
    def show_splitcanvas(self, controller):
        if not self.splitstatus:
            people_name = self.checkboxList.state()
            splitEntry = []
            for name in people_name:
                if name != '0':
                    splitrow = Frame(self.splitcanvas, bg = 'SteelBlue2')
                    splitLabel = Label(description2row, text = str(name) + ': ', anchor='w', bg = 'SteelBlue2')
                    splitEntry.append(Entry(splitrow))
                    splitrow.pack(side=TOP, fill=X, padx=5, pady=3)
                    splitLabel.pack(side = LEFT, anchor = N)
                    splitEntry[-1].pack(side=RIGHT, expand=YES, fill=X)
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
        
        button1 = tk.Button(self, text="Add",
                            command=lambda: self.add(controller))
        button1.pack()
        
        button2 = tk.Button(self, text="Return",
                            command=lambda: controller.show_frame(ProjectPage))
        button2.pack(pady=5, padx=5, side = BOTTOM, anchor=SW)




## MAIN

if __name__ == "__main__":
    app = EasySplit()
    app.mainloop()
