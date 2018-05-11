import matplotlib
matplotlib.use('TkAgg')

import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class DefaultLayout:
    
    def __init__(self, root_frame, figure):
        print('hi from DefaultLayout')
        
        self.root_frame = root_frame
        
        self.root_frame.columnconfigure(0, weight=1)
        self.root_frame.rowconfigure(0, weight=1)
        
        
        
        self.fig = figure        
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=0, sticky=('N','S','E','W'))
        
        
        
        self.toolbar_frame = ttk.Frame(self.root_frame)
        self.toolbar_frame.grid(column=1, row=0, sticky=('N','E','S','W'))
        
        self.toolbar_frame.columnconfigure(0, weight=1)
        
        self.toolbar_label = ttk.Label(self.toolbar_frame, text='Toolbar')
        self.toolbar_label.grid(column=0, row=0, sticky=('W','E'))
        
        
        self.draw_line_btn = ttk.Button(self.toolbar_frame, text='Draw Line')
        self.draw_line_btn.grid(column=0, row=1, sticky=('W','E'))
        
        
        
    
    def set_draw_line_callback(self, callback):
        self.draw_line_btn['command'] = callback
    
    def clean_up(self):
        print('DefaultLayout cleaning up')
        
        self.draw_line_btn.grid_forget()
        self.toolbar_label.grid_forget()
        self.toolbar_frame.grid_forget()
        self.canvas.get_tk_widget().grid_forget()
