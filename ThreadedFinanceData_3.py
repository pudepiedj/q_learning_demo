# This does several things
# mostly it calls a google resource for current FTSE100 data
# but it also taught me a lot more than that
# note that this version supersedes ThreadedFinanceData_3.py WHICH WILL NOT BE UPDATED ANY FURTHER

# The great thing here is that I conquered the button configuration sufficiently well to be able to click any one of the 100 stock buttons and get the
# information about that stock individually. This involves understanding the command = lambda <parameters>: expression syntax
# in conjunction with the controller functionality

# It draws three or four pages with buttons that don't do anything except switch pages
# The Graph Page displays either a static graph or an animation of the data stored in a text file
# Now we want to use threading to increment the data that we are plotting in real time
# So that the graph will update without us doing silly text-file amendments that don't mean anything
# So we'll create a thread to update the xLIst, yList variables that are being plotted separately and continuously
# And it really works!
# Now we can put the generation of the numbers using a thread into the page class so it regenerates the graph on each visit

# The commented-out bits are because I don't have pandas

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

import threading
import random               # used to generate dummy data in the thread increment
import time
import logging

# following the installation of Python8.2 this is no longer necessary
# import sys
# sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages')
# for i in range(len(sys.path)):
#    print(sys.path[i])
    
import pandas as pd
import numpy as np

import requests

import json
import urllib.request


LARGE_FONT = ("Verdana", 12)

style.use("ggplot") # or can use "dark_background" and "ggplot" and others

lock = threading.Lock()

ftseread = False

f = Figure(figsize = (8,8), dpi = 100)
a = f.add_subplot(221)
b = f.add_subplot(222)
c = f.add_subplot(223)
d = f.add_subplot(224)

g = Figure(figsize = (10,5), dpi = 100)
e = g.add_subplot(111)

h = Figure(figsize = (10,5), dpi = 100)
k = h.add_subplot(111)

wList = []
xList = []
yList = []
zList = []

resample_data = True

#global nameList
#global priceList
#global changeList

nameList = []
priceList = []
changeList = []
changepercentList = []
tagList = []

googleButton = []

def animate(i):
    #pullData = open("sampleData.txt","r").read()  # this needs to be in the same folder as the code unless add PATH
    #dataList = pullData.split('\n')
    #xList = []
    #yList = []
    #for eachLine in dataList:
    #    if len(eachLine)>1:
    #        x, y = eachLine.split(',')
    #        xList.append(int(x))
    #        yList.append(int(y))

    a.clear()
    b.clear()
    c.clear()
    d.clear()
    
    e.clear()

    a.set_title("FTSE Change Against Price")
    a.set_xlabel("Price Change Today")
    a.set_ylabel("Share Price")
    a.tick_params(labelrotation = 90, labelsize = 6, color = 'blue', axis = 'x')
    minLength = min(len(changeList),len(priceList))
    a.scatter(changeList[0:minLength], priceList[0:minLength])
    b.set_title("Scatter of %Change Against Price")
    b.scatter(changepercentList, priceList)
    c.set_title("Random Bar Graph")
    c.bar(xList, yList)
    d.set_title("Daily Percentage Change")
    d.scatter(changeList[0:minLength], changepercentList[0:minLength])

    #lock.acquire()
    #e.plot(xList, wList)            # This uses dummy data to make sure the second window is working
    e.tick_params(labelrotation = 90, labelsize = 4, labelleft = True, axis = 'x')
    minLength = min(len(nameList),len(priceList))
    e.bar(nameList[0:minLength], priceList[0:minLength])     # This tries to use live data from the FTSE stream; will need formatting

class SetUpPages(tk.Tk):

    print("We're inside SetUpPages now\n")
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.grid(sticky = "w")
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
            
        self.show_frame(StartPage, 999, "")
        
    # notice how this takes the argument passed to it and changes the frame to that page
    
    def show_frame(self, cont, counter, googleurl):

        if googleurl != "" and counter != 999:
            print("counter =", counter, "\n", googleurl)
            print(requests.get(googleurl).text)
            # local = input("Strike any key to continue")
        else:
            print("There's nothing for you here!")
            # local = input("Strike any key to continue")

        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        self.controller = controller

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Start Page", font = LARGE_FONT)
        label.grid(pady = 10, padx = 10)

        button = tk.Button(self, bg = '#303030', fg = '#b7f731', relief='flat', text = "FTSE100 Data", command = lambda: self.controller.show_frame(PageOne, 999, ""))
        button.grid()      

        button2 = tk.Button(self, text = "FTSE100 Price Plot", command = lambda: controller.show_frame(PageTwo, 999, ""))
        button2.grid()

        button3 = tk.Button(self, text = "Random Graph Page", command = lambda: controller.show_frame(PageThree, 999, ""))
        button3.grid()


class PageOne(tk.Frame):
        
    def __init__(self, parent, controller):

        # this line assigns contoller to a local variable/field and makes it possible to pass it to the subroutine/function (I think)
        self.controller = controller
        
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Page One", font = LARGE_FONT)
        label.grid(row = 0, column = 0)
                
        button1 = tk.Button(self, text = "Home", command = lambda: controller.show_frame(StartPage, 999, ""))
        button1.grid(row = 1, column = 1)

        button2 = tk.Button(self, text = "Page Two", command = lambda: controller.show_frame(PageTwo, 999, ""))
        button2.grid(row = 1, column = 2)

        button3 = tk.Button(self, text = "Random Graph Page", command = lambda: controller.show_frame(PageThree, 999, ""))
        button3.grid(row = 1, column = 3)

        button4 = tk.Button(self, highlightbackground = '#FF00FF', fg = '#000000', text = "FTSE100", command = lambda: self.makebuttons())
        button4.grid(row = 0, column = 2)


    # this is tewwibly clever but it doesn't work because whatever button is pressed it calls the final WHITBREAD stock information
    # I suspect this is because somehow the variable 'i' is always at the end of its range, but that suggests that the buttons don't store their parameters permanently
    def makebuttons(self):

        global googleButton

        for i in range(100):
            google_html_leadstr = 'https://spreadsheets.google.com/feeds/list/0AhySzEddwIC1dEtpWF9hQUhCWURZNEViUmpUeVgwdGc/1/public/basic'
            get_one_co = '?sq=symbol='
            just_try_one = tagList[i]
            
            #print('\n',just_try_one,'\n')
            # join can only take one argument which must be a list of string to join as above
            
            googleurl = setup_google_str(google_html_leadstr, get_one_co, just_try_one)
            googleButton.append(googleurl)
            
            #print(googleurl)
            #local = input("Is there anything here for you?")
            # Note the use of the "stock = i" to force the button to store the index; without it the index always comes out at 99 and you get the last stock
            
            if changeList[i] < 0:
                button = tk.Button(self, text = "{0:2d} {1} {2:9.2f} {3:9.2f}".format(i, nameList[i], priceList[i], changeList[i]),
                                   highlightbackground = 'red', fg = 'black',
                                   command = lambda stock = i: self.controller.show_frame(PageOne, stock, googleButton[stock]))
            elif changeList[i] > 0:
                button = tk.Button(self, text = "{0:2d} {1} {2:9.2f} {3:9.2f}".format(i, nameList[i], priceList[i], changeList[i]),
                                   highlightbackground = 'green', fg = 'black',
                                   command = lambda stock = i: self.controller.show_frame(PageOne, stock, googleButton[stock]))
            else:
                button = tk.Button(self, text = "{0:2d} {1} {2:9.2f} {3:9.2f}".format(i, nameList[i], priceList[i], changeList[i]),
                                   highlightbackground = 'blue', fg = 'black',
                                   command = lambda stock = i: self.controller.show_frame(PageOne, stock, googleButton[stock]))         
            #for key in button.config():
            #    print(key, button.config(key))
            #for item in button.keys():
            #    print(item, " ... ",button.cget(item))
            #local = input("Well")
            button.grid(row = 3 + divmod(i,34)[1], column = 1 + divmod(i,34)[0], sticky = "W")

            
#PageTwo plots the e figure to one page; note that they are both created by the same animate function

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Page Two", font = LARGE_FONT)
        label.grid(row = 0, column = 0)

        button1 = ttk.Button(self, text = "Home", command = lambda: controller.show_frame(StartPage, 999, ""))
        button1.grid()

        button2 = ttk.Button(self, text = "Page One", command = lambda: controller.show_frame(PageOne, 999, ""))
        button2.grid()

        button3 = ttk.Button(self, text = "Random Graph Page", command = lambda: controller.show_frame(PageThree, 999, ""))
        button3.grid()

#        lock.acquire()
#        print(xList, yList)
        e.plot(xList, yList)            # This uses dummy data to make sure the second window is working
        canvas2 = FigureCanvasTkAgg(g, self)
        canvas2.draw()
        canvas2.get_tk_widget().grid(sticky = "w")
#        lock.release()
        
        #toolbar2 = NavigationToolbar2Tk(canvas2, self)
        #toolbar2.update()
        #canvas2._tkcanvas.grid(sticky = "w")


# PageThree plots all of the a, b, c, d figures to one page
class PageThree(tk.Frame):

#    resample_data = False
        
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Graph Page", font = LARGE_FONT)
        label.grid(pady = 10, padx = 10)

        button1 = tk.Button(self, text = "Back to Home", command = lambda: controller.show_frame(StartPage, 999, ""))
        button1.grid()

        button2 = tk.Button(self, text = "Page One", command = lambda: controller.show_frame(PageOne, 999, ""))
        button2.grid()

        button3 = tk.Button(self, text = "Page Two", command = lambda: controller.show_frame(PageTwo, 999, ""))
        button3.grid()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().grid(sticky = "w")

        #toolbar = NavigationToolbar2Tk(canvas, self)
        #toolbar.update()
        #canvas._tkcanvas.grid(sticky = "w")

# concatenate as many string pieces as we need for what we want to call

def setup_google_str(prefix, suffix, identifier):

    googleList = (prefix, suffix, identifier)
    call_str = "".join(googleList)
    return call_str


def getftse(nameList, priceList, changeList):

    global ftseread
    ftseread = ftse_read.wait()
    
    print("\nStarting data pull\n")

    # the following has to be prepended to any call followed by something like '?alt-json' as from richard allen's blog
    google_html_leadstr = 'https://spreadsheets.google.com/feeds/list/0AhySzEddwIC1dEtpWF9hQUhCWURZNEViUmpUeVgwdGc/1/public/basic'
    ftse_all = '?alt=json'      # notice that this means the requested data is JSON but that isn't the default
    #get_one_co = '?sq=symbol='
    #just_try_one = 'VOD.L'
    # join can only take one argument which must be a list of string to join as above
    googleurl = setup_google_str(google_html_leadstr, ftse_all, "")
    #googleurl = setup_google_str(google_html_leadstr, get_one_co, just_try_one)
    print(googleurl)
    # data = requests.get(googleurl).json()
    data = requests.get(googleurl)          # we are no longer dealing with JSON data format
    print('\n\nThis is the data call response ... \n\n',data)
    print('\n\nThis is the data text string ...\n\n',data.text)
    print('\n\nThis is the data string header ...\n\n', data.headers)
    for key in data.headers:
        print(key,"...%40s" % (data.headers[key]),'\n')
    print('\n\nThis is the data string header ...\n\n', data.headers['Content-Type'])
    if (data.headers['Content-Type'].split('/')[1]).split(";")[0] == 'json':
        print("\n\nThis is JSON data ...")
        data = data.json()
    else:
        print("\n\nThis is not JSON data ... it is a data stream formatted as",(data.headers['Content-Type']).split('/')[1],"\n\n\n")
        data = data.text
        
    # data.to_csv("Stocks.csv") this saves the data to a csv file
    
    for key in data:
        for name in data[key]:
            if name == 'updated':
                timestamp = data[key][name]['$t'].split('T')
                print("FTSE100 on", timestamp[0],"\nat",timestamp[1].split('.')[0])
            elif name == 'entry':
                #print("\n\n",data[key][name],"\n\n")
                ups=0
                downs=0
                notapp=0
                # there is a problem with zeroing these arrays because the process is too quick for the plotting to catch up
                # so we introduce an enforced time.sleep so there is time for the plotting to happen before the zeroing
                # time.sleep(5.0)
                #nameList = []
                #priceList = []
                #changeList = []
                for i in range(0,100):
                    changepercent = 0
                    #print(data[key][name][i]['content']['$t'])
                    tag = data[key][name][i]['title']['$t']
                    nam, price, change = data[key][name][i]['content']['$t'].split(', ')    # this breaks up the entry into three pieces
                    nam = nam.split(': ')[1]
                    price = price.split(': ')[1]                                            # this breaks the pieces in two
                    change = change.split(': ')[1]
                    nameList.append(nam)                                                    # name is the company name string
                    if change == "#N/A":
                        change = 0
                        notapp += 1
                        print("%20s %8s %10s %10s %6s" % (nam, tag, price, change, ""))
                    if price != "#N/A":
                        changepercent = round(float(change)/float(price)*100,2)
                        print("%20s %8s %10s %10s %6s" % (nam, tag, price, change, changepercent))
                        priceList.append(float(price))          # price is the current price
                    else:
                        priceList.append(0)                 # price is the current price for #N/A entries
                        changepercent = 0
                    change = float(change)
                    changeList.append(change)        # change is the change today (I think)
                    changepercentList.append(changepercent)
                    tagList.append(tag)
                    if change < 0:
                        downs +=1
                    elif change > 0:
                        ups += 1
                print("\nUps =",ups,"Downs =",downs, "#N/A",notapp)
                ##print(nameList, priceList, changeList)
                ##print(xList, yList, zList, wList)

                #e = g.add_subplot(111)
                #e.clear()
                #e.plot(changeList,priceList)

    print("\nFinishing data pull\n")
#    resample_data = True
    
def incrementalupdate(xList, yList):

    global ftseread

    ftseread = ftse_read.wait()
    logging.warning("Event set: %s", ftseread)
    print("\nNow we're doing incrementalupdate")

    time.sleep(0.1)
    #xList = []
    #yList = []

    for i in range(500):
        time.sleep(0.01)
        xList.append(i)
        yList.append(random.randint(0,250))


def incrementalupdate2(wList, zList):

    global ftseread

    ftseread = ftse_read.wait()
    logging.warning("Event set: %s", ftseread)
    print("\nNow we're doing incrementalupdate TWO")   

    time.sleep(0.1)
    #wList = []
    #zList = []
            
    for i in range(500):
        time.sleep(0.01)
        zList.append(random.randint(0,50))      # Notice that if you do these assignments in different threads it is likely
        wList.append((random.randint(0,500)))   # that the sizes of the two lists will be incompatible

# this thread calls other threads and may execute too quickly for the main thread ever to work
# it may also interfere with the values shared by different threads, and seems therefore to require LOCKS

# this means other threads have to wait for ftse to finish
# and it does regulate the calls to data refresh but the other pages never appear

# Note that we are only invoking ONE animate function but that function sets all the mpl graphing which is then
# only DRAWN by the Tkinter Canvases when required, so the graphs are written in the background repeatedly
# but only displayed when required. This means that the updating can be quick and continuous
# but that the displays, which are much slower, only occur as needed
# so there can be as many "figures" f, g, etc as we like and we just create additional animx inside anim

# if I understand the flow correctly, having set resample_data to False, even though the getftse function sets
# it back to True on completion, by then the main thread has executed and fallen through the bottom of this while-loop
# so it has already terminated and by the time getftse comes back, it's all over!!! So the program doesn't do anything
# The question is: how to reset resample_data to True at an appropriate moment that doesn't cause a massive loop

# I suspect that this requires a more sophisticated method such as one involving LOCKS or BARRIERS or EVENTS

# It's necessary to make a list of animations to force different copies of FuncAnimation or it gets overwritten by each call
# Conceptually it isn't clear to me where to force the program to restart and redraw all the graphs
# This seems to be how the "restart" loop works in the QMaze-Learner-World set
# So should we recreate that loop and reset the "restart" flag when we complete, say, the incremental update?
# And force a new read of the FTSE data at the same time - but that will happen automatically, won't it?

print("Now we're running the program again ...")

# since app has been defined as SetUpPages(), the following runs it as the main thread

if __name__ == "__main__":

    logging.basicConfig(filename='example.log', filemode = 'w', level=logging.WARNING, format='(%(threadName)-9s) %(message)s',)
    logging.warning('Main thread started\n')
    # time.sleep(1)
    ftse_read = threading.Event()

    app = SetUpPages()
    time.sleep(1.0)
    th = threading.Thread(name = "inc1",target=incrementalupdate, args = (xList, yList))
    th.start()
    ftseread = ftse_read.set()
    #th.join()
    th2 = threading.Thread(name = "inc2", target=incrementalupdate2, args = (wList, zList))
    th2.start()
    ftseread = ftse_read.set()
    #th2.join()
    ftse = threading.Thread(name = "ftse", target=getftse, args = (nameList, priceList, changeList))
    ftse.start()
    ftseread = ftse_read.set()
    logging.warning("Event set: %s", ftseread)
    print("Main thread finished\n")
    
    ani = []
    anim0 = animation.FuncAnimation(f, animate, interval = 1000)
    anim1 = animation.FuncAnimation(g, animate, interval = 1000)
    for anim in [anim0, anim1]:
        ani.append(anim)
    app.mainloop()

