import matplotlib
matplotlib.use('TkAgg')

import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class ImageLoadedLayout:
    
    def __init__(self, root_frame, img_fig, plot_fig):
        print('hi from ImageLoadedLayout')
        
        self.root_frame = root_frame
        
        self.root_frame.columnconfigure(0, weight=1)
        self.root_frame.rowconfigure(1, weight=1)
        
        
        self.toolbar_frame = ttk.Frame(self.root_frame)
        self.toolbar_frame.grid(column=0, row=0, sticky=('W','N','E','S'))
        
        self.toolbar_frame.columnconfigure(0, weight=1)
        self.toolbar_frame.rowconfigure(1, weight=1)
        
        self.back_btn = ttk.Button(self.toolbar_frame, text='Back')
        self.back_btn.grid(column=0, row=0, sticky='W')
        
        
        s = ttk.Style()
        s.configure('figures.TFrame', background='#334353')
        self.figure_frame = ttk.Frame(self.root_frame, style='figures.TFrame')
        self.figure_frame.grid(column=0, row=1, sticky=('W','N','E','S'))
        
        self.figure_frame.columnconfigure(0, weight=1)
        self.figure_frame.columnconfigure(1, weight=1)
        self.figure_frame.rowconfigure(0, weight=1)
        
        
        self.img_fig = img_fig
        self.img_canvas = FigureCanvasTkAgg(self.img_fig, master=self.figure_frame)
        self.img_canvas.get_tk_widget().grid(column=0, row=0, sticky=('W','N','E','S'))
        self.img_canvas.draw()
        
        self.plot_fig = plot_fig
        self.plot_canvas = FigureCanvasTkAgg(self.plot_fig, master=self.figure_frame)
        self.plot_canvas.get_tk_widget().grid(column=1, row=0, sticky=('W','N','E','S'))
        self.plot_canvas.draw()
        
        
        self.info_frame = ttk.Frame(self.root_frame)
        self.info_frame.grid(column=0, row=2, sticky=('W','N','E','S'))
        
        self.info_frame.columnconfigure(0, weight=1)
        #self.info_frame.rowconfigure(0, weight=1)
        
        ttk.Label(self.info_frame, text='Additional Information May Go Here').grid(column=0, row=0)
        
        
        
    
    def img_mpl_connect(self, event_type, callback):
        return self.img_canvas.mpl_connect(event_type, callback)
    
    def img_mpl_disconnect(self, cid):
        self.img_canvas.mpl_disconnect(cid)
    
    def plot_mpl_connect(self, event_type, callback):
        return self.plot_canvas.mpl_connect(event_type, callback)
    
    def plot_mpl_disconnect(self, cid):
        self.plot_canvas.mpl_disconnect(cid)
    
    def redraw_img_fig(self):
        self.img_canvas.draw()
    
    def redraw_plot_fig(self):
        self.plot_canvas.draw()
    
    def set_back_callback(self, callback):
        self.back_btn['command'] = callback
    
    
    def clean_up(self):
        self.info_frame.grid_forget()
        self.info_frame.destroy()
        
        self.figure_frame.grid_forget()
        self.figure_frame.destroy()
        
        self.toolbar_frame.grid_forget()
        self.toolbar_frame.destroy()
