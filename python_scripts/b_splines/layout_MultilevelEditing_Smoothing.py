import matplotlib
matplotlib.use('TkAgg')

import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class MultilevelEditingSmoothingLayout:
    
    def __init__(self, root_frame, figure, max_lod):
        print('hi from MultilevelEditingSmoothingLayout')
        
        self.root_frame = root_frame
        self.fig = figure
        self.max_lod = max_lod
        
        self.root_frame.columnconfigure(0, weight=1)
        self.root_frame.rowconfigure(0, weight=1)
        
        
        self.left_frame = ttk.Frame(self.root_frame)
        self.left_frame.grid(column=0, row=0, sticky=('N','E','S','W'))
        self.left_frame.columnconfigure(0, weight=1)
        self.left_frame.rowconfigure(0, weight=1)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.left_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=0, sticky=('N','S','E','W'))
        
        
        self.lod_scale_head = ttk.Label(self.left_frame, text='Adjust Level of Smoothing:')
        self.lod_scale_head.grid(column=0, row=1, sticky=('W','N','E','S'))
        
        
        self.lod_scale = ttk.Scale(self.left_frame, from_=0, to=self.max_lod, orient='horizontal')
        self.lod_scale.grid(column=0, row=2, sticky=('W','N','E','S'))
        
        
        
        self.toolbar_frame = ttk.Frame(self.root_frame)
        self.toolbar_frame.grid(column=1, row=0, sticky=('N','E','S','W'))
        
        self.toolbar_frame.columnconfigure(0, weight=1)
        self.toolbar_frame.rowconfigure(3, weight=1)
        
        self.toolbar_label = ttk.Label(self.toolbar_frame, text='Toolbar')
        self.toolbar_label.grid(column=0, row=0, sticky=('W','E'))
        
        self.num_points_head = ttk.Label(self.toolbar_frame, text='Number of Points:')
        self.num_points_head.grid(column=0, row=1, sticky=('W','E'))
        
        self.num_points_label = ttk.Label(self.toolbar_frame)
        self.num_points_label.grid(column=0, row=2, sticky=('W','E'))
        
        self.num_points_var = tk.StringVar()
        
        self.num_points_label['textvariable'] = self.num_points_var
        
        self.back_btn = ttk.Button(self.toolbar_frame, text='Back')
        self.back_btn.grid(column=0, row=3, sticky=('W','E','S'))
        
    
    def redraw_figure(self):
        self.canvas.draw()
    
    def set_num_points(self, num_points):
        self.num_points_var.set(num_points)
    
    def set_lod_scale_value(self, value):
        self.lod_scale.set(value)
    
    def set_lod_scale_callback(self, callback):
        self.lod_scale['command'] = callback
    
    def set_back_callback(self, callback):
        self.back_btn['command'] = callback
    
    def clean_up(self):
        print('MultilevelEditingSmoothingLayout cleaning up')
        
        self.back_btn.grid_forget()
        self.num_points_label.grid_forget()
        self.num_points_head.grid_forget()
        self.toolbar_label.grid_forget()
        self.toolbar_frame.grid_forget()
        self.lod_scale.grid_forget()
        self.lod_scale_head.grid_forget()
        self.canvas.get_tk_widget().grid_forget()
        self.left_frame.grid_forget()
