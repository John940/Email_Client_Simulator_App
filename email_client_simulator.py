from tkinter import *
from tkinter import ttk
win = Tk()    #Creating tkinter Window
win.geometry("700x200")
s = ttk.Style()
s.theme_use('clam')
tree = ttk.Treeview(win , column=("From", "Subject", "Date"), show="headings",height=5)    #CreatingTreeview
tree.column("#1", anchor=CENTER)
tree.heading("#1", text="From")
tree.column("#2", anchor=CENTER)
tree.heading("#2", text="Subject")
tree.column("#3", anchor=CENTER)
tree.heading("#3", text="Date")
scrollbar = Scrollbar(win)
scrollbar.pack(side=RIGHT, fill=Y,)
scrollbar.config(command=tree.yview)
tree.pack(side=TOP)    #treeviw at topside
Email_screen = Text(win,height=50,width=75)    #Creating Text screen, to appears the email text
scrollbar = Scrollbar(win)    # Creating scrollbar at Text
scrollbar.pack(side = RIGHT, fill=Y)
scrollbar.config(command=Email_screen.yview)
Email_screen.pack(side=BOTTOM)    # Text screen at Bottom

Email_dict = {}   #dictionary containing emails......where key = 'from' + name + 'Subject' +text + 'date:'+ text
             #value = The email text
try:
    with open("emails.txt","r+") as file1:   #the emails.txt have the above form 1st line 'from:' + name + 'Subject:' +text + 'date:'+ text ,in the next line is the email text
        lines = file1.readlines()   # A list with all lines of emails.txt file
except FileNotFoundError:
    print("Can't find the file with emails")
for line in lines:   
    if line.startswith("from"): 
        Sender = line[line.index("from:") :line.index("Subject:")].strip("from:")    #Finding The email Sender
        subject = line[line.index("Subject:") : line.index("date:")].strip("Subject:")    #Finding the Email Sublect
        date = line[line.index("date:"):].strip("date:\n")    #Finding the email Date
        Email_dict["from:" + Sender + "Subject:" + subject + "date:" + date]= ""    # Insert that email at dictionary with the unique key
        tree.insert('','end',id= "from:" + Sender + "Subject:" + subject + "date:" + date,values=(Sender, subject, date))    #Inserting also at the treeview
                                                                                                                                    # where key = id of Treeview
    else:    #If line don't start with form: , it s the email text 
        Email_dict["from:" + Sender + "Subject:" + subject + "date:" + date] += line    #Insert that email text at dictionary email with the right key
file1.close()

def del_func(event):    # A fuction to delete an email when user pressing the 'd' button
    Email_dict.pop(tree.focus())    # Delete from dictionary the email that user have focus (With mouse click)...
    selected_item = tree.selection()[0]  
    tree.delete(selected_item)    # Delete that email form treeview too
    Email_screen.delete('1.0', END)    #Clear the text Screen
    try:
        file = open('emails.txt','w')   
    except FileNotFoundError:
        print("Can't find the file with emails")
    for k,v in Email_dict.items():    # For every key-value at renewal dictionary ..(we have deleted the email)...
        if k.endswith("\n"):    #Write it at file
            file.write(k)
        else:
            file.write(k+"\n")
        if v.endswith("\n"):    
            file.write(v)
        else:
            file.write(v+"\n")
    file.close()

tree.bind('d',del_func)    #A listener everytime we press  'd' Button calling the del_func

def showme(event):    #A fuction that reveals the text email ,When the user pressing the  Enter
    Email_screen.delete('1.0', END)    #Clear the text screen
    Email_screen.insert(INSERT,Email_dict[tree.focus()])    #Reveal the Email text form dictionary where dictionary key = focus value

tree.bind("<Return>",showme)    #When we press Enter calling the showme fuction

if tree.focus() == "":    
    Email_screen.insert(INSERT,"")    # the text is empty...

#print(Email_dict)
win.mainloop()



