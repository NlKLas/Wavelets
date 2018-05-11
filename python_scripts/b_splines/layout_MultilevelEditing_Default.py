import matplotlib
matplotlib.use('TkAgg')

import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class MultilevelEditingDefaultLayout:
    
    def __init__(self, root_frame, figure):
        print('hi from MultilevelEditingDefaultLayout')
        
        self.root_frame = root_frame
        self.fig= figure
        
        
        self.root_frame.columnconfigure(0, weight=1)
        self.root_frame.rowconfigure(0, weight=1)
        
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=0, sticky=('N','S','E','W'))
        
        
        
        self.toolbar_frame = ttk.Frame(self.root_frame)
        self.toolbar_frame.grid(column=1, row=0, sticky=('N','E','S','W'))
        
        self.toolbar_frame.columnconfigure(0, weight=1)
        self.toolbar_frame.rowconfigure(3, weight=1)
        
        self.toolbar_label = ttk.Label(self.toolbar_frame, text='Toolbar')
        self.toolbar_label.grid(column=0, row=0, sticky=('W','E'))
        
        
        self.smooth_btn = ttk.Button(self.toolbar_frame, text='Smooth')
        self.smooth_btn.grid(column=0, row=1, sticky=('W','E'))
        
        self.edit_btn = ttk.Button(self.toolbar_frame, text='Edit')
        self.edit_btn.grid(column=0, row=2, sticky=('W','E'))        
        
        self.discard_btn = ttk.Button(self.toolbar_frame, text='Discard')
        self.discard_btn.grid(column=0, row=3, sticky=('W','E','S'))
        
        
    def set_discard_callback(self, callback):
        self.discard_btn['command'] = callback
    
    def set_smooth_callback(self, callback):
        self.smooth_btn['command'] = callback
    
    def set_edit_callback(self, callback):
        self.edit_btn['command'] = callback
    
    def redraw_figure(self):
        self.canvas.draw()
    
    def clean_up(self):
        print('MultilevelEditingDefaultLayout cleaning up')
        
        self.discard_btn.grid_forget()
        self.edit_btn.grid_forget()
        self.smooth_btn.grid_forget()
        self.toolbar_label.grid_forget()
        self.toolbar_frame.grid_forget()
        self.canvas.get_tk_widget().grid_forget()
