import tkinter as tk
from tkinter import ttk


class DefaultLayout:
    
    def __init__(self, root_frame):
        print('hi from DefaultLayout')
        
        self.root_frame = root_frame
        
        self.root_frame.columnconfigure(0, weight=1)
        self.root_frame.rowconfigure(1, weight=1)
        
        
        self.toolbar_frame = ttk.Frame(self.root_frame)
        self.toolbar_frame.grid(column=0, row=0, sticky=('W','N','E','S'))
        
        self.toolbar_frame.columnconfigure(0, weight=1)
        self.toolbar_frame.rowconfigure(1, weight=1)
        
        self.load_img_btn = ttk.Button(self.toolbar_frame, text='Load Image')
        self.load_img_btn.grid(column=0, row=0, sticky='W')
        
        s = ttk.Style()
        s.configure('Placeholder.TFrame', foreground='white', background='white')
        self.placeholder = ttk.Frame(self.root_frame, style='Placeholder.TFrame')
        self.placeholder.grid(column=0, row=1, sticky=('W','N','E','S'))
        
        self.placeholder.columnconfigure(0, weight=1)
        self.placeholder.rowconfigure(0, weight=1)
        
        
    def set_load_img_callback(self, callback):
        self.load_img_btn['command'] = callback
    
    def clean_up(self):
        self.toolbar_frame.grid_forget()
        self.toolbar_frame.destroy()
        
        self.placeholder.grid_forget()
        self.placeholder.destroy()
        
        
        
        
