import matplotlib
matplotlib.use('TkAgg')

import tkinter as tk
from tkinter import ttk

from matplotlib.figure import Figure

import layout_Default
import state_DrawLine

class DefaultState:
    
    def __init__(self, base, content_frame):
        
        self.base = base
        self.content_frame = content_frame
        
        self.fig = Figure()
        
        self.layout = layout_Default.DefaultLayout(self.content_frame, self.fig)
        
        self.layout.set_draw_line_callback(self._on_draw_line)
        
        print('hi from DefaultState!')
    
    
    def _on_draw_line(self):
        print('I hear you want to draw a line...')
        
        new_state = state_DrawLine.DrawLineState(self.base, self.content_frame, self.fig)
        
        self.base.update_program_state(new_state)
        self.clean_up()
    
    
    def clean_up(self):
        self.layout.clean_up()
        print('DefaultState cleaning up')
        
        
        
