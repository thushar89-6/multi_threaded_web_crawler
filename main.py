import customtkinter as ctk
import tkinter as tk
import threading
#import file crawler.py from files folder
import files.crawler as ncrawl
#import getarticle.py from files folder
import files.getarticle as getarticle
import os

#function for button 1
def fn1():
    #create a new window
    window = ctk.CTkToplevel(root)
    #set always on top of parent window
    window.attributes("-topmost",True)
    #calculation to place the new window at center of screen and set window size
    ws = root.winfo_screenwidth() 
    hs = root.winfo_screenheight() 
    x = (ws/2) - (350/2)
    y = (hs/2) - (100/2)
    #window.geometry("350x100+x+y") where x and y are offsets about where to place window when created, by default it places randomly when specified like this window.geometry("350x100")
    window.geometry("350x100+%d+%d" % (x,y))
    #create title, text entry box
    window.title("Enter seed url")
    e1 = ctk.CTkEntry(window)
    #set 0th column to expand infinitely to right
    window.grid_columnconfigure(0,weight=1)
    #place the text entry in that 0th row and 0th column (makes it grow infinitely to left and right, then put padding 30 left and right)
    e1.grid(row=0,column=0,sticky='ew',padx=30,pady=10)
    #function when save is clicked (puts content of e1 to uncrawled.txt in files folder)
    def ffn1():
        if not os.path.exists("files/uncrawled.txt"):
            f=open("files/uncrawled.txt", "w+")
        else:
            f=open("files/uncrawled.txt","a+",encoding='utf-8')
        f.write(e1.get()+"\n")
        f.close()
        #put the message on text field on main window
        t1.insert(tk.END,"URL added sucessfully to uncrawled.txt\n")
        window.destroy()
    #save button which will execute ffn1
    bb = ctk.CTkButton(window,text="Save",command=ffn1)
    bb.grid(row=1,column=0)
    window.mainloop
#function to 2nd button creates a new window with 2 entries and crawl button, asks for retrictions and no of threads
def fn2():
    w2=ctk.CTkToplevel(root)
    w2.attributes("-topmost",True)
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen
    x = (ws/2) - (350/2)
    y = (hs/2) - (180/2)
    w2.geometry("350x180+%d+%d" % (x,y))
    w2.title("Add restrictions")
    e1 = ctk.CTkEntry(w2,placeholder_text="Pattern to match in URLs")
    w2.grid_columnconfigure(0,weight=1)
    e1.grid(row=0,column=0,sticky='ew',padx=30,pady=10)
    e2 = ctk.CTkEntry(w2,placeholder_text="No of threads")
    e2.grid(row=1,column=0,sticky='ew',padx=30,pady=10)
    e3 = ctk.CTkEntry(w2,placeholder_text="No of iterations")
    e3.grid(row=2,column=0,sticky='ew',padx=30,pady=10)
    #function when crawl button is clicked
    def ffn1():
        text = e1.get()
        no= 2 if e2.get()=="" else int(e2.get())#set default threads to 2 if not entered
        itr= 1 if e3.get()=="" else int(e3.get())#no of iterations, default 1
        #destroy the child window
        w2.destroy()
        #clear the t1 textfield and add message
        t1.delete(0.0,tk.END)
        t1.insert(tk.END,"Crawling...")
        #start ffn2 function as a new thread. If thread is not created main window shows not responding as it has to wait for function to complete executing for long time.
        threading.Thread(target=ffn2,args=(text,no,itr)).start()
    #function which executed crawler.py in files folder with restriction and no of threads as arguments, written in seperate ffn2 so that it can be executed as a thread.
    def ffn2(text,no,itr):
        #returns a string containing all the messages appended into it during execution, and after execution writes it into text field t1 in main window.
        out = ncrawl.new(text,no,itr)
        t1.insert(tk.END,out)   
        

    bb = ctk.CTkButton(w2,text="Crawl",command=ffn1)
    bb.grid(row=3,column=0)
    w2.mainloop()
    
#functions to clear, view uncrawled and crawled files
def fn3():
    with open("files/uncrawled.txt","w") as f:
        pass
    t1.insert(tk.END,"Uncrawled.txt cleared successfully!\n")

def fn4():
    with open("files/crawled.txt","w") as f:
        pass
    t1.insert(tk.END,"Crawled.txt cleared successfully!\n")

def fn5():
    with open("files/crawled.txt","r",encoding='utf-8') as f:
        ouput=f.read()
    t1.delete(0.0,tk.END)
    t1.insert(tk.END,ouput)

def fn6():
    with open("files/uncrawled.txt","r",encoding='utf-8') as f:
        ouput=f.read()
    t1.delete(0.0,tk.END)
    t1.insert(tk.END,ouput)
#function to extract article from one url. window with one text entry field and on button
def fn7():
    w3=ctk.CTkToplevel(root)
    w3.attributes("-topmost",True)

    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen
    x = (ws/2) - (350/2)
    y = (hs/2) - (100/2)
    w3.geometry("350x100+%d+%d" % (x,y))
    w3.title("Extract article")
    e1 = ctk.CTkEntry(w3)
    w3.grid_columnconfigure(0,weight=1)
    e1.grid(row=1,column=0,sticky='ew',padx=30,pady=8)
    def ex():
        url=str(e1.get())
        w3.destroy()
        #run getarticle.py first argument 0 for extracting one article from url(2nd argument), first argument 1 for extracting article from all links in crawled.txt. Aricles will be put in Articles folder.
        out=getarticle.extract(0,url)
        t1.delete(0.0,tk.END)
        t1.insert(tk.END,out)
    bb = ctk.CTkButton(w3,text="Extract",command=ex)
    bb.grid(row=2,column=0,padx=30,pady=10)
    w3.mainloop()

def fn8():
    t1.delete(0.0,tk.END)
    t1.insert(tk.END,"Extracting articles...")
    def ffn1():
        out=getarticle.extract(1,"")
        t1.delete(0.0,tk.END)
        t1.insert(tk.END,out)
    threading.Thread(target=ffn1).start()

#create main windowa
root= ctk.CTk()
root.title("Crawler")
# ws1 = root.winfo_screenwidth()
# hs1 = root.winfo_screenheight()
# w=700
# h=450
# x1 = (ws1//2) - (w//2)
# y1 = (hs1//2) - (h//2)
# root.geometry("%dx%d+%d+%d" % (w,h,x1,y1))
root.geometry("700x450")
#create a frame where all buttons are added
f3 = ctk.CTkFrame(root)
btn1= ctk.CTkButton(f3,text="Add seed urls",command=fn1)
btn1.grid(row=1,column=0,padx=10,pady=10)

btn2= ctk.CTkButton(f3,text="Crawl",command=fn2)
btn2.grid(row=2,column=0,pady=10,padx=10)

btn3= ctk.CTkButton(f3,text="Clear uncrawled",command=fn3)
btn3.grid(row=1,column=1,pady=10,padx=10)
btn4= ctk.CTkButton(f3,text="Clear crawled",command=fn4)
btn4.grid(row=2,column=1,pady=10,padx=10)

btn5= ctk.CTkButton(f3,text="View Crawled",command=fn5)
btn5.grid(row=1,column=2,pady=10,padx=10)
btn6= ctk.CTkButton(f3,text="View Uncrawled",command=fn6)
btn6.grid(row=2,column=2,pady=10,padx=10)

    
btn7= ctk.CTkButton(f3,text="Extract article",command=fn7)
btn7.grid(row=1,column=3,pady=10,padx=10)
btn8= ctk.CTkButton(f3,text="Extract all article",command=fn8)
btn8.grid(row=2,column=3,pady=10,padx=10)


f3.grid(row=0,column=0,pady=20)

#create a 2nd frame to place text field t1 where all outputs are shown.
f2=ctk.CTkFrame(root)
root.grid_rowconfigure(1,weight=1)
root.grid_columnconfigure(0,weight=1)
f2.grid(row=1,column=0,sticky='nsew',padx=30,pady=30)

t1=ctk.CTkTextbox(f2)
t1.insert(tk.END,"")
f2.grid_rowconfigure(0,weight=1)
f2.grid_columnconfigure(0,weight=1)
t1.grid(row=0,column=0,padx=20,pady=20,sticky='nsew')



root.mainloop()
