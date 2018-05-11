import matplotlib
matplotlib.use('TkAgg')

import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class DrawLineLayout:
    
    def __init__(self, root_frame, figure):
        print('hi from DrawLineLayout')
        
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
        self.toolbar_frame.rowconfigure(5, weight=1)
        
        self.toolbar_label = ttk.Label(self.toolbar_frame, text='Toolbar')
        self.toolbar_label.grid(column=0, row=0, sticky=('W','E'))
        
        
        self.upsample_btn = ttk.Button(self.toolbar_frame, text='Upsample')
        self.upsample_btn.grid(column=0, row=1, sticky=('W','E'))
        self.upsample_btn.state(['disabled'])
        
        self.done_btn = ttk.Button(self.toolbar_frame, text='Done')
        self.done_btn.grid(column=0, row=2, sticky=('W','E','S'))
        self.done_btn.state(['disabled'])
        
        
        self.num_points_head = ttk.Label(self.toolbar_frame, text='Number of Points:')
        self.num_points_head.grid(column=0, row=3, sticky=('W','E'))
        
        self.num_points_label = ttk.Label(self.toolbar_frame)
        self.num_points_label.grid(column=0, row=4, sticky=('W','E','S'))
        
        self.num_points_var = tk.StringVar()
        self.num_points_var.set(0)
        
        self.num_points_label['textvariable'] = self.num_points_var
        
        
        self.discard_btn = ttk.Button(self.toolbar_frame, text='Discard')
        self.discard_btn.grid(column=0, row=5, sticky=('W','E','S'))
    
    
    def enable_upsample_btn(self):
        self.upsample_btn.state(['!disabled'])
    
    def enable_done_btn(self):
        self.done_btn.state(['!disabled'])
    
    def disable_upsample_btn(self):
        self.upsample_btn.state(['disabled'])
    
    def disable_done_btn(self):
        self.done_btn.state(['disabled'])
    
    def set_num_points(self, num_points):
        self.num_points_var.set(num_points)
    
    def redraw_figure(self):
        self.canvas.draw()
    
    def mpl_connect(self, event_type, callback):
        return self.canvas.mpl_connect(event_type, callback)
    
    def mpl_disconnect(self, cid):
        self.canvas.mpl_disconnect(cid)
    
    def set_upsample_callback(self, callback):
        self.upsample_btn['command'] = callback
    
    def set_done_callback(self, callback):
        self.done_btn['command'] = callback
    
    def set_discard_callback(self, callback):
        self.discard_btn['command'] = callback
    
    def clean_up(self):
        print('DrawLineLayout cleaning up')
        
        self.discard_btn.grid_forget()
        self.num_points_label.grid_forget()
        self.num_points_head.grid_forget()
        self.done_btn.grid_forget()
        self.upsample_btn.grid_forget()
        self.toolbar_label.grid_forget()
        self.toolbar_frame.grid_forget()
        self.canvas.get_tk_widget().grid_forget()
