import matplotlib
from tkinter import *
# from PIL import ImageTk, Image
import numpy as np
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
# Note the changed name of the toolbar widget in the next line witout "Agg" at the end
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class mclass:
    def __init__(self,  window):
        self.window = window
        self.box = Entry(window)
        self.button = Button(window, text="Click Here to see House Price Distribution!", command=self.plot)
        self.box.pack()
        self.button.pack()

    def plot (self):
        house_prices = np.random.normal(300000,25000,2000)
        income = np.random.normal(25000,5000,2000)
        x = np.array (house_prices)
        v = np.array (income)
        #p = np.array (plot_y2[0:20])
        fig = Figure(figsize=(10,5), dpi = 100)

        a = fig.add_subplot(121)
        b = fig.add_subplot(122)
        a.scatter(x,v,color='red')
        b.hist(x,color='blue',bins = 50)
        #a.invert_yaxis()

        b.set_title("Histogram", fontsize = 14)
        b.set_ylabel("Frequency", fontsize=12)
        b.set_xlabel("House Price", fontsize=12)
        a.set_title ("Scatterplot", fontsize=14)
        a.set_ylabel("Frequency", fontsize=12)
        a.set_xlabel("Income", fontsize=12)

        qvalues = FigureCanvasTkAgg(fig, master=self.window)
        qvalues.get_tk_widget().pack()
        qvalues.draw()

        toolbar = NavigationToolbar2Tk(qvalues, root)
        toolbar.update()
        qvalues.get_tk_widget().pack()
        

root = Tk()
root.wm_title("Embedding Matplotlib Graphics in Tk")
start = mclass(root)
root.mainloop()
