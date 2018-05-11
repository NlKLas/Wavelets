import matplotlib
matplotlib.use('TkAgg')

import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class MultilevelEditingEditingLayout:
    
    def __init__(self, root_frame, figure, max_lod):
        print('hi from MultilevelEditingEditingLayout')
        
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
        
        
        self.display_lod_scale_head = ttk.Label(self.left_frame, text='Level of Detail of the displayed curve:')
        self.display_lod_scale_head.grid(column=0, row=1, sticky=('W','N','E','S'))
        
        
        self.display_lod_scale = ttk.Scale(self.left_frame, from_=0, to=self.max_lod, orient='horizontal')
        self.display_lod_scale.grid(column=0, row=2, sticky=('W','N','E','S'))
        
        
        self.edit_lod_scale_head = ttk.Label(self.left_frame, text='Level of Detail for editing:')
        self.edit_lod_scale_head.grid(column=0, row=3, sticky=('W','N','E','S'))
        
        
        self.edit_lod_scale = ttk.Scale(self.left_frame, from_=0, to=self.max_lod, orient='horizontal')
        self.edit_lod_scale.grid(column=0, row=4, sticky=('W','N','E','S'))
        
        
        
        self.toolbar_frame = ttk.Frame(self.root_frame)
        self.toolbar_frame.grid(column=1, row=0, sticky=('N','E','S','W'))
        
        self.toolbar_frame.columnconfigure(0, weight=1)
        self.toolbar_frame.rowconfigure(1, weight=1)
        
        self.toolbar_label = ttk.Label(self.toolbar_frame, text='Toolbar')
        self.toolbar_label.grid(column=0, row=0, sticky=('W','E'))
        
        
        self.back_btn = ttk.Button(self.toolbar_frame, text='Back')
        self.back_btn.grid(column=0, row=1, sticky=('W','E','S'))
        
    
    def mpl_connect(self, event_type, callback):
        return self.canvas.mpl_connect(event_type, callback)
    
    def mpl_disconnect(self, cid):
        self.canvas.mpl_disconnect(cid)
    
    def redraw_figure(self):
        self.canvas.draw()
    
    def set_display_lod_scale_value(self, value):
        self.display_lod_scale.set(value)
        
    def set_edit_lod_scale_value(self, value):
        self.edit_lod_scale.set(value)
    
    def set_display_lod_scale_callback(self, callback):
        self.display_lod_scale['command'] = callback
    
    def set_edit_lod_scale_callback(self, callback):
        self.edit_lod_scale['command'] = callback
    
    def set_back_callback(self, callback):
        self.back_btn['command'] = callback
    
    def clean_up(self):
        print('MultilevelEditingEditingLayout cleaning up')
        
        self.back_btn.grid_forget()
        self.toolbar_label.grid_forget()
        self.toolbar_frame.grid_forget()
        self.edit_lod_scale.grid_forget()
        self.edit_lod_scale_head.grid_forget()
        self.display_lod_scale.grid_forget()
        self.display_lod_scale_head.grid_forget()
        self.canvas.get_tk_widget().grid_forget()
        self.left_frame.grid_forget()
