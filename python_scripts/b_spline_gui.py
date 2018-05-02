import matplotlib
matplotlib.use('TkAgg')

import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import numpy as np


class BasicMatplotlibGui:
    
    def __init__(self,title='Plot Window'):
        
        #manage gui components
        self.root = tk.Tk()
        self.root.title(title)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=('N','W','E','S'))
        
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(1, weight=1)
        
        
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.mainframe)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=1, sticky=('N','S','E','W'))
        
        ttk.Label(self.mainframe, text='Toolbar goes here!').grid(column=0, row=0, sticky=('W','E'))
        
        
        #register key-bindings
        self.root.bind('<Return>', self._done)
        
        
        #register event-bindings
        self.canvas.mpl_connect('pick_event', self._onpick)
        
        
        #initialize state variables
        self.pickerOption = False
        
        
    def show(self):
        tk.mainloop()
    
    def plot(self, *args, **kwargs):
        kwargs['picker'] = self.pickerOption
        self.ax.plot(*args,**kwargs)
    
    def scatter(self, *args, **kwargs):
        kwargs['picker'] = self.pickerOption
        self.ax.scatter(*args, **kwargs)
    
    def setPickerOption(self, value):
        self.pickerOption = value        
    
    def _done(self,e=None):
        self.root.quit()
        self.root.destroy()
    
    '''
    certainly works, I am just not sure how usefull it will be...
    '''
    def _onpick(self,evt):
        artist = evt.artist
        print(type(artist))
        
        if isinstance(artist, matplotlib.lines.Line2D):
            xdata, ydata = artist.get_data()
            data = np.vstack((xdata,ydata))
            print(data[...,evt.ind])
        
        elif isinstance(artist, matplotlib.collections.PathCollection):
            print(artist.get_offsets()[evt.ind,...])
        
            

if __name__ == '__main__':
    
    x = np.linspace(-5,5,50)
    y = np.sinc(x)
    
    gui = BasicMatplotlibGui()
    
    gui.scatter(x,y)
    gui.setPickerOption(True)
    gui.show()
    
    
    
    
    
    
    
