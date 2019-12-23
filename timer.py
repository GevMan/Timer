from app import app,db
from models import user ,days
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
from flask import Flask,redirect,render_template,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_admin import Admin,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from datetime import datetime,date,time
import xlwt 
from xlwt import Workbook
import pandas as pd
from pymysql import*
import pandas.io.sql as sql
import pyautogui
import random



app.secret_key='zzz'
#adminView
class MyModelView(ModelView):
    def is_accessible(self):
        return True

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return True

Admin = Admin(app, index_view=MyAdminIndexView())
Admin.add_view(MyModelView(user, db.session))
Admin.add_view(MyModelView(days, db.session))
time = 0

#view
@app.route("/")
def index():
    global user_name
    update = user.query.filter(user.username == user_name).first()
    day = days.query.filter(days.user_id == update.id).order_by(days.id.desc()).all()
    Dict=dict()
    users=[]
    work_hours=[]
    all_users = user.query.all()
    for us in all_users: 
        Dict={us.username:'us.work_hours'}
        users.append(Dict)

    all_days=days.query.all()
    for d in all_days:
        new_dict={d.day:d.work_hours}
        work_hours.append(new_dict)
    return render_template('index.html',work=users,days=day,hours=work_hours)

@app.route("/export")
def export():
    wb = Workbook() 
    con=connect(user="nnd7fl2rcgzmls5l",password="ex0isaorv23gefvw",host="thzz882efnak0xod.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",database="a9bwgfq691fo7jb9")
    user_table=sql.read_sql('select * from user',con)
    days_table=sql.read_sql('select * from days',con)
    writer= pd.ExcelWriter('timer.xlsx')
    user_table.to_excel(writer,"Sheet1")
    days_table.to_excel(writer,"Sheet2")
    writer.save()
    return redirect(url_for('index'))


global user_name
#Toplevel
class main:
    def __init__(self, master):
        self.master = master
        self.username = StringVar()
        self.password = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        self.repeat_pass = StringVar()
        self.work_hours = StringVar()
        self.widgets()
    
    def login(self):
        global user_name
        global timer
        user_name = self.username.get()
        find_user = user.query.filter( user.password == self.password.get() and user.username== self.username.get()).first()

        if find_user:
            now = datetime.now()
            current_day = now.strftime("%d/%b/%Y")
            name = self.username.get()
            name_label.config(text=name)
            root.deiconify()
            self.master.destroy()
            update = user.query.filter(user.username == user_name).first()
            day = days.query.filter(days.user_id == update.id).order_by(days.id.desc()).first()
            time = day.work_hours
            day_part=day.day.split('/')
            time_part = time.split(":")
            if int(now.day) == int(day_part[0]) :
                if len(time_part) == 3:
                    time_part[0] = int(time_part[0])
                    time_part[1] = int(time_part[1])
                    time_part[2] = int(time_part[2])
                    timer = time_part
                timeText.configure(text=time)
            else:
                timeText.configure(text="00:00:00")
                new_day = days(user_id = update.id, day= current_day, work_hours = "00:00:00")
                db.session.add(new_day)
                db.session.commit()
        else:
            messagebox.showerror('Oops!', 'User Not Found.')

    def new_user(self):
 
        if user.query.filter(user.username == self.n_username.get()).first():
            messagebox.showerror('Error!', 'Username Taken Try a Diffrent One.')
        elif self.n_password.get() != self.repeat_pass.get():
            messagebox.showerror('Error!', 'Passwords must match!.')
        else:
            messagebox.showinfo('Success!', 'Account Created!')
            self.log()
            new_user = user(username=self.n_username.get(),password=self.n_password.get())
            db.session.add(new_user)
            db.session.commit()

    def log(self):
        self.username.set('')
        self.password.set('')
        self.crf.pack_forget()
        self.head['text'] = 'LOGIN'
        self.logf.pack()

    def cr(self):
        self.n_username.set('')
        self.n_password.set('')
        self.repeat_pass.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Create Account'
        self.crf.pack()

    

    def widgets(self):
        self.head = ttk.Label(self.master, text='LOGIN', background='gray94', font=('helvetica', 25))
        self.head.pack(pady=15)
        self.logf = ttk.Frame(self.master)
        ttk.Label(self.logf, text='Username: ', font=('Helvetica', 15)).grid(sticky=E,padx=10)
        ttk.Entry(self.logf, textvariable=self.username, font=('', 15)).grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(self.logf, text='Password: ', font=('', 15)).grid(sticky=E,padx=10)
        ttk.Entry(self.logf, textvariable=self.password, font=('', 15), show='*').grid(row=1, column=1,padx=10, pady=5)
        ttk.Button(self.logf, text=' Login ', command=self.login).grid(padx=10, pady=10)
        ttk.Button(self.logf, text=' Create Account ', command=self.cr).grid(row=2, column=1)
        self.master.resizable(0, 0)
        self.logf.pack()

        self.crf = ttk.Frame(self.master)
        ttk.Label(self.crf, text='Username: ', font=('', 15)).grid(sticky=E,padx=10)
        ttk.Entry(self.crf, textvariable=self.n_username, font=('', 15)).grid(row=0, column=1,padx=10, pady=5)
        ttk.Label(self.crf, text='Password: ', font=('', 15)).grid(sticky=E,padx=10)
        ttk.Entry(self.crf, textvariable=self.n_password, font=('', 15), show='*').grid(row=1, column=1,padx=10, pady=5)
        ttk.Label(self.crf, text='Repeat Password: ', font=('', 15)).grid(sticky=E,padx=10)
        ttk.Entry(self.crf, textvariable=self.repeat_pass, font=('', 15), show='*').grid(row=2, column=1, padx=10, pady=5)
        ttk.Button(self.crf, text='Create Account', command=self.new_user).grid(padx=10, pady=10)
        ttk.Button(self.crf, text='Go to Login', command=self.log).grid(row=3, column=1)

#updateTime 
def update_time():
    if state:
        global timer
        global user_name
        timer[2] += 1
        if timer[2] > 59:
            timer[2] = 0
            timer[1] += 1
        if timer[1] > 59:
            timer[0] += 1
            timer[1] = 0
            
    
        time_string = pattern.format(timer[0], timer[1], timer[2])     
        timeText.configure(text=time_string)
        autosave(timer[2])
    root.after(1000, update_time)
   
    
#autosave into db
def autosave(seconds):
    if seconds != 59:
        return  True
    now=datetime.now()
    time = timeFormat(timer[0])+':'+timeFormat(timer[1])+':'+timeFormat(timer[2])
        
    update = user.query.filter(user.username == user_name).first()
    day = days.query.filter(db.and_(days.user_id == update.id, days.day == now.day)).first()
    day.work_hours = time
    db.session.commit()
    
#Start
def start(event=''):
    global state
    state = True
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_day = now.strftime("%d/%b/%Y")
    update = user.query.filter(user.username == user_name).first()
    day = days.query.filter(days.user_id == update.id).first()
    if  day is None: 
        new_day = days(user_id = update.id, day= current_day, work_hours = "00:00:00" )
        db.session.add(new_day)
        db.session.commit()
    if start:
        btn_start.configure(text='Pause', command=pause)
    


time = None
#Pause
def pause():
    global state
    global time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if messagebox.askokcancel("Pause", "Do You want to pause timer?"):
        state = False
        
        time = timeFormat(timer[0])+':'+timeFormat(timer[1])+':'+timeFormat(timer[2])
        
        update = user.query.filter(user.username == user_name).first()
        day = days.query.filter(db.and_(days.user_id == update.id, days.day == now.day)).first()
        day.work_hours = time
        db.session.commit()
    if state == False:
        btn_start.configure(text='Start', command=start)

        
def timeFormat(time):
    if time < 10:
        return '0' + str(time)
    else:
        return str(time)
    
# reset      
def reset():
    global timer
    if messagebox.askokcancel("Reset", "Do You want to reset timer?"):
        timer = [0, 0, 0]
        timeText.configure(text='00:00:00')

# exit
def exit():
    if messagebox.askokcancel("Exit", "Are You sure?"):
        root.destroy()

# about
def about_program():
    messagebox.showinfo(title='About Timer', message='Time Tracker Version 1.0.1')

# export into excel
def export_user():
    update = user.query.filter(user.username == user_name).first()
    wb = Workbook() 
    con=connect(user="mfeyq8tq95ldf7g3",password="ld1ic4nbalv55wv4",host="f8ogy1hm9ubgfv2s.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",database="j962xvujyevc1gxk")
    days_table=sql.read_sql ('select * from days WHERE user_id ='+str(update.id),con)
    writer= pd.ExcelWriter('work_hours.xlsx')
    days_table.to_excel(writer,"Sheet1")
    writer.save()

#take a screenshot
def takeScreenshot ():
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(r'C:\projects\timer_prtsc\screenshot.png')
    random_time = random.randint(5000, 100000)
    root.after(random_time, takeScreenshot)

state = False

root = ThemedTk(theme='arc')
root.title('Timer')
# root.iconbitmap('python.ico')
root.geometry("400x300+500+150")
root.resizable(False, False)
main_menu = Menu(root)
root.config(menu=main_menu)
timer = [0, 0, 0]
pattern = '{0:02d}:{1:02d}:{2:02d}'

top_frame = ttk.Frame(root)
top_frame.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.1, anchor='n')

btn_start = ttk.Button(top_frame, text='Start', command=start)
btn_start.place(relx=0.40, relwidth=0.25, relheight=1)

lower_frame = ttk.Frame(root)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.9, relheight=0.6, anchor='n')

name_label = ttk.Label(lower_frame, text="", font=("Helvetica", 12))
name_label.pack()

timeText = ttk.Label(lower_frame, text="", font=("Helvetica", 30))
timeText.pack()


# File
file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label="Reset" , command=reset)
file_menu.add_command(label="Export" , command=export_user)
file_menu.add_separator()
file_menu.add_command(label="Exit",command=exit)
main_menu.add_cascade(label="File", menu=file_menu)

# About
help_menu = Menu(main_menu, tearoff=0)
help_menu.add_command(label="About", command=about_program)
main_menu.add_cascade(label="Help", menu=help_menu)

main(Toplevel())
update_time()
takeScreenshot()
root.withdraw()
root.mainloop()
