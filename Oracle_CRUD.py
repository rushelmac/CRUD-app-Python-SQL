from tkinter import *
from tkinter import messagebox 
from tkinter import ttk
import cx_Oracle

#================================================================================================#

try:
    conn = cx_Oracle.connect("system/Oracle1999@192.168.43.177:1521/XEPDB1")

    cursor = conn.cursor()
except:
    exit()

#=====================================================================================================================

root=Tk()
root.title('Oracle Database CRUD Operations')
root.configure(background='white')
root.geometry("1080x600")

topFrame = Frame(root)
midFrame = Frame(root,height=10)
bottomFrame = Frame(root,bg='white')
topFrame.pack()
midFrame.pack()
bottomFrame.pack(fill=BOTH, expand=1)

Label(topFrame,text="CRUD Operations on Oracle using Python",font=('Times New Roman',25),fg='red',bg='white').pack(side=TOP)

rf1=Frame(bottomFrame,bg='white',borderwidth = 1, relief = SUNKEN)
cf1=Frame(bottomFrame,bg='white',borderwidth = 1, relief = SUNKEN,width=70)
uf1=Frame(bottomFrame,bg='white',borderwidth = 1, relief = SUNKEN,width=70)
df1=Frame(bottomFrame,bg='white',borderwidth = 1, relief = SUNKEN,width=70)
rf1.pack(side=BOTTOM, fill=BOTH, expand=1)
cf1.pack(side=LEFT,fill=BOTH,padx=5,pady=5,expand=1)        
uf1.pack(side=LEFT,fill=BOTH,padx=5,pady=5,expand=1)        
df1.pack(side=LEFT,fill=BOTH,padx=5,pady=5,expand=1)

#==========================================================================================================================

#READ UI

Label(rf1,text="READ",bg='white',font=('Times New Roman',15),fg='blue').grid(row=0)

style = ttk.Style()
style.configure("Treeview",background="white",foreground='black',rowheight=25)
style.map('Treeview',background=[('selected','green')])

tv = ttk.Treeview(rf1,columns=(1,2,3,4,5),show="headings",height="5")
tv.grid(row=1,padx=10)
tv.heading(1,text='PRN',anchor=W)
tv.heading(2,text='Name',anchor=W)
tv.heading(3,text='Branch',anchor=W)
tv.heading(4,text='Localite',anchor=W)
tv.heading(5,text='Phone',anchor=W)

#=====================================================================================================================

# READ Query Processing

def display(tree):
    for i in tree.get_children():
        tree.delete(i)

    query = "Select * from student"
    cursor.execute(query)

    rows = cursor.fetchall()

    for i in rows:
        tree.insert('','end',values=i,tag='black')

#=====================================================================================================================

#CREATE Query Processing

def create():
    try:
        prn = ipEntry.get()
        name = inEntry.get()
        branch = ibEntry.get()
        localite = int(cr.get())
        phno = iphEntry.get()

        if(len(prn)==0):
            print(len(prn))
            messagebox.showwarning("Warning", "Enter a PRN to Insert")
            return
        if(len(name)==0):
            messagebox.showwarning("Warning", "Enter a Name to Insert")
            return
        if(len(branch)==0):
            messagebox.showwarning("Warning", "Enter a Branch to Insert")
            return
        if(len(phno)==0 or len(phno)>10):
            messagebox.showwarning("Warning", "Enter a valid Phone Number to Insert")
            return    

        query = f"select * from student where prn = '{prn}'"
        cursor.execute(query)
        res = cursor.fetchall()
        
        if(res):
            messagebox.showwarning("Warning", "Record with given PRN already exists")
            return

        if localite==0:
            localite="N"
        else:
            localite="Y"
        
        phno=int(phno)

        query = f"insert into student values('{prn}','{name}','{branch}','{localite}',{phno} )"
    
        cursor.execute(query)
        cursor.execute('commit')

        messagebox.showinfo("Info", "Successfully updated")
        display(tv)


        ipEntry.delete(0,"end")
        inEntry.delete(0,"end")
        ibEntry.delete(0,"end")
        iphEntry.delete(0,"end")

    except Exception as ex:
        messagebox.showinfo("Error", "Something Wrong with the system, Please Restart the System" + ex)

#=====================================================================================================================

# UPDATE Query Processing

def update():
    try:
        prn = upEntry.get()

        if(len(prn)==0):
            messagebox.showwarning("Warning", "Enter a PRN to Update")
            return

        query = f"select * from student where prn = '{prn}'"
        cursor.execute(query)
        res = cursor.fetchall()

        if(not res):
            messagebox.showwarning("Warning", "Enter Valid PRN to Update")
            return

        name = unEntry.get()
        branch = ubEntry.get()
        localite = int(ur.get())
        phno = uphEntry.get()

        query = f"update student set "
        if(localite==0):
            query=query+"localite='N'"
        else:
            query=query+"localite='Y'"
        if(len(name)!=0):
            query=query+f",name='{name}'"
        if(len(branch)!=0):
            query=query+f",branch='{branch}'"
        if(len(phno)!=0):
            phno=int(phno)
            query=query+f",phno='{phno}'"
        
        query=query+f"where prn='{prn}'"
        
        cursor.execute(query)
        cursor.execute('commit')

        messagebox.showinfo("Info", "Successfully updated")

        upEntry.delete(0,"end")
        unEntry.delete(0,"end")
        ubEntry.delete(0,"end")
        uphEntry.delete(0,"end")

        display(tv)

    except Exception as ex:
        messagebox.showinfo("Error", "Something Wrong with the system, Please Restart the System" + ex)

#=========================================================================================================================

#DELETE query Processing

def delete():
    prn = dpEntry.get()
    
    if(len(prn)==0):
            messagebox.showwarning("Warning", "Enter a PRN to Delete a praticular Record")
            return

    query = f"select * from student where prn = '{prn}'"
    cursor.execute(query)

    res = cursor.fetchall()

    if(not res):
        messagebox.showwarning("Warning", "Record not available to Delete")
        return

    query = f"delete from student where prn='{prn}'"
    cursor.execute(query)
    messagebox.showinfo("Info", "Successfully deleted")
    cursor.execute('commit')
    dpEntry.delete(0,"end")

    display(tv)

#==========================================================================================================================

#INSERT UI

Label(cf1,text="CREATE",bg='white',font=('Times New Roman',15),fg='blue').grid(row=0,padx=5,pady=5)
Label(cf1,text='PRN',bg='white').grid(row=1,column=0,padx=5,pady=5)
Label(cf1,text='First Name',bg='white').grid(row=2,column=0,padx=5,pady=5)
Label(cf1,text='Branch',bg='white').grid(row=3,column=0,padx=5,pady=5)
Label(cf1,text='Local',bg='white').grid(row=4,column=0,padx=5,pady=5)
Label(cf1,text='PhNo',bg='white').grid(row=5,column=0,padx=5,pady=5)
ipEntry=Entry(cf1,width=20)
ipEntry.grid(row=1,column=1)
inEntry=Entry(cf1,width=20)
inEntry.grid(row=2,column=1)
ibEntry=Entry(cf1,width=20)
ibEntry.grid(row=3,column=1)
cr=IntVar()
radioFrame1=Frame(cf1)
radioFrame1.grid(row=4,column=1)
Radiobutton(radioFrame1, text = "YES", variable = cr, value = 1,bg='white').grid(row=0,column=0)
Radiobutton(radioFrame1, text = "NO", variable = cr, value = 0,bg='white').grid(row=0,column=1)

iphEntry=Entry(cf1,width=20)
iphEntry.grid(row=5,column=1)
cSubmit=Button(cf1,text='Submit',padx=15,pady=5,command=create)
cSubmit.grid(row=6,column=1)

#=====================================================================================================================

#UPDATE UI

Label(uf1,text="UPDATE",bg='white',font=('Times New Roman',15),fg='blue').grid(row=0,padx=5,pady=5)
Label(uf1,text='PRN',bg='white').grid(row=1,column=0,padx=5,pady=5)
Label(uf1,text='(*required)',bg='white',font=("Times New Roman", 8)).grid(row=1,column=2,padx=5,pady=5)
Label(uf1,text='First Name',bg='white').grid(row=2,column=0,padx=5,pady=5)
Label(uf1,text='Branch',bg='white').grid(row=3,column=0,padx=5,pady=5)
Label(uf1,text='Local',bg='white').grid(row=4,column=0,padx=5,pady=5)
Label(uf1,text='PhNo',bg='white').grid(row=5,column=0,padx=5,pady=5)
upEntry=Entry(uf1,width=20)
upEntry.grid(row=1,column=1)
unEntry=Entry(uf1,width=20)
unEntry.grid(row=2,column=1)
ubEntry=Entry(uf1,width=20)
ubEntry.grid(row=3,column=1)
ur=IntVar()
radioFrame2=Frame(uf1)
radioFrame2.grid(row=4,column=1)
Radiobutton(radioFrame2, text = "YES", variable = ur, value = 1,bg='white').grid(row=0,column=0)
Radiobutton(radioFrame2, text = "NO", variable = ur, value = 0,bg='white').grid(row=0,column=1)

uphEntry=Entry(uf1,width=20)
uphEntry.grid(row=5,column=1)
uSubmit=Button(uf1,text='Submit',padx=15,pady=5,command=update)
uSubmit.grid(row=6,column=1)

#=====================================================================================================================

#DELETE UI

Label(df1,text="DELETE",bg='white',font=('Times New Roman',15),fg='blue').grid(row=0,padx=5,pady=5)
Label(df1,text='PRN',bg='white').grid(row=1,column=0,padx=5,pady=5)
dpEntry=Entry(df1,width=20)
dpEntry.grid(row=1,column=1)
uSubmit=Button(df1,text='Submit',padx=15,pady=5,command=delete)
uSubmit.grid(row=2,column=1)

#=====================================================================================================================

display(tv)
#=========================================================================================================================


root.mainloop()
