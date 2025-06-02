__author__ = 'jcp'

import matplotlib
import numpy as np
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.animation as animation

# This is all to do with matplotlib
plot_x = []
plot_y1 = []
plot_y2 = []
plt.plot([], [])
# plt.ion()
# plt.legend()
fig, ax = plt.subplots()
# plt.show()
# legendmarker = 0

import random
import tkinter
from tkinter import *
root = Tk()

# this is not the most efficient way to do this plot but this at least works
class mclass:
    def __init__(self,  window):
        self.window = window
        self.box1 = Entry(window)
        self.box2 = Entry(window)
        self.button1 = Button (window, text="Click Here to Plot", command = self.plot)
        self.box1.grid()
        self.button1.grid() 
        # the end of the next line needs to say "plot" to plot and "animate" to animate; will later automate this
        self.button2 = Button (window, text="Click Here to Animate", command = self.animate)
        self.box2.grid()
        self.button2.grid()

    def plot(self):
        x = np.array (plot_x)
        v = np.array (plot_y1)
        p = np.array (plot_y2)
        fig = Figure(figsize=(15,5))
        a = fig.add_subplot(131)
        b = fig.add_subplot(132)
        a.clear()
        a.scatter(x,p,color='red')
        b.clear()
        b.plot(x,p,color='blue')
        a.invert_yaxis()

        a.set_title ("Amazing If This Works", fontsize=16)
        a.set_ylabel("Score on Success/Fail", fontsize=14)
        a.set_xlabel("Attempt", fontsize=14)
        
        qvalues = FigureCanvasTkAgg(fig, master = self.window)
        qvalues.get_tk_widget().grid()
        qvalues.draw()

        #toolbar = NavigationToolbar2Tk(qvalues, root)
        #toolbar.update()
        #qvalues.get_tk_widget().grid()

    def animate(self):
        xList = np.array(plot_x)
        yList = np.array(plot_y2)

        fig = Figure(figsize = (15,5), dpi = 100)
        c = fig.add_subplot(133)
        c.clear()
        c.plot(xList, yList)

        c.set_title ("Amazing If This Works", fontsize=16)
        c.set_ylabel("Score on Success/Fail", fontsize=14)
        c.set_xlabel("Attempt", fontsize=14)

        qvalues = FigureCanvasTkAgg(fig, master = self.window)
        qvalues.get_tk_widget().grid()
        qvalues.draw()

for i in range(100):
    j = random.randint(0,100)
    k = random.randint(0,100)
    l = random.randint(0,100)
    plot_x.append(j)
    plot_y1.append(k)
    plot_y2.append(l)
print(plot_x, plot_y1, plot_y2)

start = mclass(root)
ani = animation.FuncAnimation(fig, mclass.animate, interval = 1000)
root.mainloop()
