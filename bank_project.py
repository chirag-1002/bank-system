from tkinter import*
from PIL import Image, ImageTk
from tkinter import messagebox
from tkcalendar import DateEntry
import sqlite3
import random
import datetime
from tkinter import ttk

con=sqlite3.connect("dbbank.db")
win=Tk()
win.title("Bank Profile")
win.state("zoomed")
win.geometry("400x450")
win.iconbitmap('desktop_logo.ico')

heading_label=Label(win,text="Punjab National Bank",bg="red4",fg="yellow",font=('times new roman',29,'bold'),height=2)
heading_label.pack(fill=X)
l2=Label(bg="yellow")
l2.pack(fill=X)
name_label=Label(win,text="Designed By :- CHIRAG BANSAL ",font="arial",fg="green")
name_label.place(x=1050,y=650)

img=Image.open("pnblogo.png")
img=img.resize((45,43))
img=ImageTk.PhotoImage(img)
labeling1=Label(win,image=img,bg="red4")
labeling1.place(x=440,y=25)

img2=Image.open("pnbbank.jpg")
img2=img2.resize((500,450))
img2=ImageTk.PhotoImage(img2)
labeling2=Label(win,image=img2)
labeling2.place(x=50,y=150)

def transactions(acno):
    def getbalance():
        data=(acno,)
        q='SELECT SUM (amount) AS deposit_balance from transactiondata where accountno=? and type="deposit"'
        res=con.execute(q,data)
        row=res.fetchone()
        if row[0]==None:
            depositamt=0
        else:
            depositamt=row[0]
        print("deposit value:",depositamt)
 
        q='SELECT SUM (amount) AS withdraw_balance from transactiondata where accountno=? and type="withdraw"'
        result=con.execute(q,data)
        cal=result.fetchone()
        if cal[0]==None:
            withdrawamt=0
        else:
            withdrawamt=cal[0]
        print("withdraw value",withdrawamt)

        balance=depositamt-withdrawamt
        print("current balance:",balance)
        return balance
    x=Toplevel()
    x.state("zoomed")
    x.title("Process")

    heading_label=Label(x,text="Punjab National Bank",bg="red4",fg="yellow",font=('times new roman',29,'bold'),height=2)
    heading_label.pack(fill=X)
    l2=Label(x,bg="yellow")
    l2.pack(fill=X)

    img5=Image.open("pnblogo.png")
    img5=img5.resize((45,43))
    img5=ImageTk.PhotoImage(img5)
    labeling6=Label(x,image=img5,bg="red4")
    labeling6.place(x=440,y=25)

    frame=Frame(x, height=350, width=850, bd=3, relief="raised")
    frame.place(x=50,y=180)
    
    def clear_frame():
            for widgets in frame.winfo_children():
                widgets.destroy()
        
    def withdr():
        clear_frame()
        balance=getbalance()
        
        def withdr_now():
            a=with_entry.get()
            if int(balance)<int(a):
                messagebox.showerror("error","INSUFFICENT BALANCE",parent=x)
            else:
                withdraw=with_entry.get()
                
                date=datetime.datetime.now()
                #date=date.strftime("%Y-%m-%d")
                type="withdraw"
                data=(acno,withdraw,type,date)
                try:
                    q="insert into transactiondata(accountno,amount,type,date) values(?,?,?,?)  "
                    con.execute(q,data)
                    con.commit()
                    messagebox.showinfo("succcess","Withdraw successfully ",parent=x)
                except Exception as e:
                    print(e)
                    messagebox.showerror("error","the data is not stored",parent=x)
        
        with_label=Label(frame,text="Enter The Amount Of Withdraw:-",font=('arial',20,'bold'))
        with_label.place(x=10,y=10)
        with_entry=Entry(frame,bg="yellow",font=("bold",19))
        with_entry.place(x=10,y=70,height=35,width=300)
        confirm_button=Button(frame,text="Confirm",fg="yellow",bg="red4",font=('arial',27,'bold'),border=8,relief=RAISED,command=withdr_now)
        confirm_button.place(x=60,y=160,height=50,width=180)  
    

    def deposit(): 
        clear_frame()
        def deposit_now():

            depst=depo_entry.get()
            date=datetime.datetime.now()
            type="deposit"
            data=(acno,depst,type,date) 
            try:
                q="insert into transactiondata(accountno,amount,type,date) values(?,?,?,?)  "
                con.execute(q,data)
                con.commit()
                messagebox.showinfo("succcess","Your amount successfully deposit",parent=x)
            except Exception as e:
                print(e)
                messagebox.showerror("error","the data is not stored",parent=x)
        depo_entry=StringVar()
        depo_label=Label(frame,text="Enter The Amount Of Deposit:-",font=('arial',20,'bold'))
        depo_label.place(x=10,y=10)
        depo_entry=Entry(frame,bg="yellow",font=("bold",19),textvariable=depo_entry)
        depo_entry.place(x=10,y=70,height=35,width=300)
        
        confirm_button=Button(frame,text="Confirm",fg="yellow",bg="red4",font=('arial',27,'bold'),border=8,relief=RAISED,command=deposit_now)
        confirm_button.place(x=60,y=160,height=50,width=180)   

    def check_balance():
        clear_frame() 
        balance=getbalance()
        check_balance_label=Label(frame,text="Current Balance:-",font=('arial',20,'bold'))
        check_balance_label.place(x=10,y=10)
        check_balance_entry=Label(frame,bg="yellow",font=("bold",19), text=balance)
        check_balance_entry.place(x=10,y=70,height=35,width=300)

    def passbook():
        clear_frame()
        scrollbar=Scrollbar(frame,orient=VERTICAL)
        scrollbar.pack(side=RIGHT,fill=Y)
        scrollbar1=Scrollbar(frame,orient=HORIZONTAL)
        scrollbar1.pack(side=BOTTOM,fill=X)
        textarea=Text(frame, height=20, width=115, bd=3, relief="raised",yscrollcommand=scrollbar.set,xscrollcommand=scrollbar1.set)
        textarea.pack()
        scrollbar.config(command=textarea.yview)
        scrollbar1.config(command=textarea.xview)

        global currentbalance
        currentbalance=0
        data=(acno,)   
        q='SELECT * from transactiondata where accountno=?'   
        result=con.execute(q,data)
        cal=result.fetchall()      
        textarea.insert(END,"Transactions")
        textarea.insert(END,'\n \n Date and Time')
        textarea.insert(END,'\t \t \t\tType of Transaction')
        textarea.insert(END,'\t \t\tAmount')
        textarea.insert(END,'\t  Current Balance')
        textarea.insert(END,'\n===================================================================================================================')
        for row in cal:
            print(row[2])
            amt=row[2]
            dt=row[4]
            tp=row[3]

            if(tp=='deposit'):
                currentbalance=currentbalance+int(amt)
            if(tp=='withdraw'):
                currentbalance=currentbalance-int(amt)

            textarea.insert(END,f'\n')
            textarea.insert(END,f'{dt} ')
            textarea.insert(END,f'\t \t\t \t{tp}')
            textarea.insert(END, f'\t\t  \t{amt}')
            textarea.insert(END,f'\t\t{currentbalance}')

    def pin_change():
        clear_frame()
        def pin_check():
            data=(acno,)
            
            q='SELECT pin from accounts where accountno=?'
            res=con.execute(q,data)
            cal=res.fetchone()
            print(cal[0])
   
            old_entry=old_pin_entry.get()
            new_entry=new_pin_entry.get()
            confirm_entry=confirm_pin_entry.get()
            print(old_entry)
            if str(cal[0])==str(old_entry): 
                 
                if old_entry==new_entry:
                    messagebox.showerror("error","password is same",parent=x)
                elif new_entry==confirm_entry:
                   data=(new_entry,acno,)
                   try: 
                    q="UPDATE accounts  set pin=? where accountno=? "
                    con.execute(q,data)
                    con.commit()
                    messagebox.showinfo("success","pin change succesfully")
                   except Exception as e:
                       print(e)
                else:
                    messagebox.showerror("Error","PINs do not match",parent=x)
            else:
                messagebox.showerror("Error","Old PIN is wrong", parent=x)
        def pin_check1(e):
          pin_check()            

        old_pin=Label(frame,text="Old pin-",font=('arial',20,'bold'))
        old_pin.place(x=10,y=10)
        old_pin_entry=Entry(frame,bg="yellow",font=("bold",19))
        old_pin_entry.place(x=10,y=50,height=35,width=300)

        new_pin=Label(frame,text="New pin-",font=('arial',20,'bold'))
        new_pin.place(x=10,y=100)
        new_pin_entry=Entry(frame,bg="yellow",font=("bold",19))
        new_pin_entry.place(x=10,y=140,height=35,width=300)

        confirm_pin=Label(frame,text="confirm pin-",font=('arial',20,'bold'))
        confirm_pin.place(x=10,y=190)
        confirm_pin_entry=Entry(frame,bg="yellow",font=("bold",19))
        confirm_pin_entry.place(x=10,y=230,height=35,width=300)
        confirm_pin_entry.bind("<Return>",pin_check1)
                


        confirm_button=Button(frame,text="Confirm",fg="yellow",bg="red4",font=('arial',27,'bold'),border=8,relief=RAISED,command=pin_check)
        confirm_button.place(x=80,y=290,height=50,width=180)   

    def viewall():
            clear_frame()
            def gettransactions():
                for c in trv.get_children():
                    trv.delete(c)
                
                a=from_entry.get_date()
                b=to_entry.get_date() 

                print(a,b)
                data=(acno,a,b,)
                q="select * from transactiondata where accountno=? and Date(date) between ? and ?"
                result=con.execute(q,data)
                counter=1
                for x in result :
                    trv.insert("",'end',iid=x[0],values=(counter,x[2],x[3],x[4]))
                    counter=counter+1
            def getansaction1(e):
                gettransactions()
     
            def deletetransaction():
                select=trv.focus()
                data=(acno,select,)
                try:
                    q='DELETE from transactiondata where accountno=? and ID=? '
                    con.execute(q,data)
                    con.commit()
                    messagebox.showinfo("succcess","data is successfully deleted  ",parent=w)
                    gettransactions()
                except Exception as e:
                    print(e)
                    messagebox.showerror("error","the data is not deleted",parent=w)    
                
            w=Toplevel() 
            w.title("Login")
            w.state("zoomed")
            
            heading_label=Label(w,text="Punjab National Bank",bg="red4",fg="yellow",font=('times new roman',29,'bold'),height=2)
            heading_label.pack(fill=X)
            l2=Label(w,bg="yellow")
            l2.pack(fill=X)

            img4=Image.open("pnblogo.png")
            img4=img4.resize((70,70))
            img4=ImageTk.PhotoImage(img4)
            imglabeling=Label(w,image=img,bg="red4")
            imglabeling.place(x=440,y=25)

     
            name_label=Label(w,text="Designed By :- CHIRAG BANSAL ",font="arial",fg="green")
            name_label.place(x=1050,y=650)
            
            from_label=Label(w,text="From",fg='red4',font=('arial',27,'bold'))
            from_label.place(x=60,y=150)
            from_entry=DateEntry(w,)
            from_entry.place(x=60,y=200,height=40,width=250)

            to_label=Label(w,text="To",fg="red4",font=('arial',27,'bold'))
            to_label.place(x=500,y=150)
            to_entry=DateEntry(w,)
            to_entry.place(x=500,y=200,height=40,width=250)
            to_entry.bind("<Return>",getansaction1)
       
            button_submit=Button(w,text="Submit",fg="yellow",bg="red4",font=('arial',20,'bold'),border=8,relief=RAISED,command=gettransactions)
            button_submit.place(x=920,y=250,height=60,width=250) 
            button_delete=Button(w,text="Delete",fg="yellow",bg="red4",font=('arial',20,'bold'),border=8,relief=RAISED,command=deletetransaction)
            button_delete.place(x=920,y=320,height=60,width=250)  
            allentryframe= Frame(w,height=430, width=450, bd=3, relief="raised")
            allentryframe.place(x=50,y=270)
            with_label=Label(allentryframe,text="TRANSACTIONS:-",font=('arial',20,'bold'))
            with_label.place(x=10,y=10)       
            trv=ttk.Treeview(allentryframe)
            trv.pack()
            scrlbr=ttk.Scrollbar(allentryframe,orient='vertical', command=trv.yview)
            scrlbr.pack(side=RIGHT,fill='y')
            trv.configure(yscrollcommand=scrlbr.set)
            style=ttk.Style(w)
            style.theme_use("clam")
            style.configure("Treeview.Heading",background="red4",foreground="yellow")
            style.configure('Treeview',background="yellow",foreground="red4")
            

            trv["columns"]=("1","2","3","4")
            trv['show']='headings'

            trv.column("1", width = 150, anchor ='c')
            trv.column("2", width = 210, anchor ='c')
            trv.column("3", width = 210, anchor ='c')
            trv.column("4", width = 210, anchor ='c')

            trv.heading("1",text="ID")
            trv.heading("2",text="Amount")
            trv.heading("3",text="Type")
            trv.heading("4",text="Date")

    button_with=Button(x,text="Withdraw",fg="yellow",bg="red4",font=('arial',27,'bold'),border=8,relief=RAISED,command=withdr)
    button_with.place(x=1070,y=160,height=60,width=280)   
     

    button_deposit=Button(x,text="Deposit",fg="yellow",bg="red4",font=('arial',27,'bold'),border=8,relief=RAISED,command=deposit)
    button_deposit.place(x=1070,y=280,height=60,width=280) 

    button_check=Button(x,text="Check Balance",fg="yellow",bg="red4",font=('arial',27,'bold'),border=8,relief=RAISED, command=check_balance)
    button_check.place(x=1070,y=400,height=60,width=280)    

    button_pinchg=Button(x,text="PIN Change",fg="yellow",bg="red4",font=('arial',27,'bold'),border=8,relief=RAISED,command=pin_change)
    button_pinchg.place(x=1070,y=520,height=60,width=280) 

    button_mini=Button(x,text="Pass Book",fg="yellow",bg="red4",font=('arial',27,'bold'),border=8,relief=RAISED,command=passbook)
    button_mini.place(x=1070,y=640,height=60,width=280) 
    
    button_viewall_transac=Button(x,text="View All Transaction",fg="yellow",bg="red4",font=('arial',27,'bold'),border=8,relief=RAISED,command=viewall)
    button_viewall_transac.place(x=500,y=640,height=60,width=380) 
       
    
    x.mainloop()

def login(accountno):
    
    def afterlogin():
         account_entry1=account_entry.get()
         pin_entry1=pin_entry.get()
         data=(account_entry1,pin_entry1,)
         q="select * from accounts where accountno=? and pin=?"
         res=con.execute(q,data)
         if(res.fetchone()):
              transactions(account_entry1)
         else:
              messagebox.showerror("Error","Invalid Login details", parent=z)
    def afterlogin1(e):
        afterlogin()

    z=Toplevel() 
    z.title("Login")
    z.state("zoomed")
    
    heading_label=Label(z,text="Punjab National Bank",bg="red4",fg="yellow",font=('times new roman',29,'bold'),height=2)
    heading_label.pack(fill=X)
    l2=Label(z,bg="yellow")
    l2.pack(fill=X)

    img3=Image.open("pnblogo.png")
    img3=img3.resize((45,43))
    img3=ImageTk.PhotoImage(img3)
    labeling3=Label(z,image=img3,bg="red4")
    labeling3.place(x=440,y=25)

    name_label=Label(z,text="Designed By :- CHIRAG BANSAL ",font="arial",fg="green")
    name_label.place(x=1050,y=650)

    accont_label=Label(z,text="Account No:- ",font=('arial',35,'bold'),fg="red4")
    accont_label.place(x=490,y=180)
    acentry=StringVar()
    account_entry=Entry(z,bg="yellow",font="bold", textvariable=acentry)
    account_entry.place(x=490,y=250,height=35,width=300)
    acentry.set(accountno)
    
    pin_label=Label(z,text="PIN:- ",font=('arial',35,'bold'),fg="red4")
    pin_label.place(x=585,y=315)
    pin_entry=Entry(z,bg="yellow",font=("bold",19),show="*")
    pin_entry.place(x=490,y=385,height=35,width=300)
    pin_entry.bind("<Return>",afterlogin1)
    
    button_verify=Button(z,text="Verify",fg="yellow",bg="red4",font=('arial',27,'bold'),border=8,relief=RAISED,command=afterlogin)
    button_verify.place(x=530,y=520,height=60,width=250)
    z.mainloop()

button_login=Button(win,text="Login",fg="yellow",bg="red4",font=('arial',27,'bold'),border=8,relief=RAISED)
button_login.place(x=850,y=230,height=60,width=250)
emptyac=StringVar()
emptyac=""
button_login.configure(command=lambda:login(emptyac))

def new_account():
    def work():
        name=cusname_entry.get()
        dob=DOB_entry.get()
        contact=cont_entry.get()
        pin=pin_entry.get()
        aadhar=adh_entry.get()
        pan=pan_entry.get()
        accountno=random.randint(11111111111111,99999999999999)
        print(accountno)

        if name=="" or dob=="" or contact=="" or pin=="" or aadhar=="" or pan=="":
            messagebox.showerror("error","all fields are require",parent=y) 

        else:    
            data=(name,dob,contact,pin,aadhar,pan,accountno)
            try:
                q="insert into accounts (name,dob,contact,pin,aadhar,pan,accountno) values(?,?,?,?,?,?,?)"
                con.execute(q,data)
                con.commit()
                messagebox.showinfo("Success","Account Created",parent=y)
                login(accountno)
            except Exception as e:
                print(e)
                messagebox.showerror("Error","Error",parent=y)
            

    y=Toplevel()
    y.title("New Account")
    y.state("zoomed")
 
    heading_label=Label(y,text="Punjab National Bank",bg="red4",fg="yellow",font=('times new roman',29,'bold'),height=2)
    heading_label.pack(fill=X)
    l2=Label(y,bg="yellow")
    l2.pack(fill=X)

    img4=Image.open("pnblogo.png")
    img4=img4.resize((45,43))
    img4=ImageTk.PhotoImage(img4)
    labeling5=Label(y,image=img4,bg="red4")
    labeling5.place(x=440,y=25)

    name_label=Label(y,text="Designed By :- CHIRAG BANSAL ",font="arial",fg="green")
    name_label.place(x=1050,y=650)

    cusname_label=Label(y,text="Customer Name:- ",font=('arial',25,'bold'),fg="red4")
    cusname_label.place(x=50,y=180)
    cusname_entry=Entry(y,bg="yellow",font="bold")
    cusname_entry.place(x=350,y=185,height=35,width=300)

    DOB_label=Label(y,text="DOB:- ",font=('arial',25,'bold'),fg="red4")
    DOB_label.place(x=50,y=250)
    DOB_entry=Entry(y,bg="yellow",font="bold")
    DOB_entry.place(x=350,y=255,height=35,width=300)

    cont_label=Label(y,text="Contact No:- ",font=('arial',25,'bold'),fg="red4")
    cont_label.place(x=50,y=320)
    cont_entry=Entry(y,bg="yellow",font="bold")
    cont_entry.place(x=350,y=325,height=35,width=300)

    pin_label=Label(y,text="PIN:- ",font=('arial',25,'bold'),fg="red4")
    pin_label.place(x=50,y=390)
    pin_entry=Entry(y,bg="yellow",font=("bold",19),show="*")
    pin_entry.place(x=350,y=395,height=35,width=300)

    conpin_label=Label(y,text="Confirm PIN:- ",font=('arial',25,'bold'),fg="red4")
    conpin_label.place(x=50,y=460)
    conpin_entry=Entry(y,bg="yellow",font=("bold",19),show="*")
    conpin_entry.place(x=350,y=465,height=35,width=300)

    adh_label=Label(y,text="Adhaar No:- ",font=('arial',25,'bold'),fg="red4")
    adh_label.place(x=750,y=180)
    adh_entry=Entry(y,bg="yellow",font="bold")
    adh_entry.place(x=950,y=185,height=35,width=300)

    pan_label=Label(y,text="PAN No:- ",font=('arial',25,'bold'),fg="red4")
    pan_label.place(x=750,y=250)
    pan_entry=Entry(y,bg="yellow",font="bold")
    pan_entry.place(x=950,y=255,height=35,width=300)
    
    button_create=Button(y,text="Verify",fg="yellow",bg="red4",font=('arial',27,'bold'),border=8,relief=RAISED,command=work)
    button_create.place(x=560,y=590,height=70,width=300)
   
    y.mainloop()

button_account=Button(win,text="New Account ",fg="yellow",bg="red4",font=('arial',27,'bold'),border=8,relief=RAISED,command=new_account)
button_account.place(x=850,y=380,height=60,width=250)
   
win.mainloop()
   