from matplotlib.figure import Figure

import state_Default
import layout_MultilevelEditing_Default
import state_MultilevelEditing_Smoothing
import state_MultilevelEditing_Editing
from b_splines import plot_uniform_b_spline_curve

import numpy as np

class MultilevelEditingDefaultState:
    
    def __init__(self, base, content_frame, control_points):
        print('hi form MultilevelEditingDefaultState')
        
        self.base = base
        self.content_frame = content_frame
        self.control_points = control_points
        
        self.fig = Figure()
        
        self.layout = layout_MultilevelEditing_Default.MultilevelEditingDefaultLayout(self.content_frame, self.fig)
        
        self.layout.set_smooth_callback(self._on_smooth)
        self.layout.set_edit_callback(self._on_edit)
        self.layout.set_discard_callback(self._on_discard)
        
        
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0,1)
        self.ax.set_ylim(0,1)
        
        plot_uniform_b_spline_curve(self.ax, self.control_points, degree=3, N=1000, color='black')
        self.ax.scatter(self.control_points[:,0],self.control_points[:,1], color='blue')
        
        self.layout.redraw_figure()
        
        
    
    def _on_smooth(self):
        print('I hear you want to smooth this b-spline...')
        
        new_state = state_MultilevelEditing_Smoothing.MultilevelEditingSmoothingState(self.base, self.content_frame, self.control_points)
        
        self.base.update_program_state(new_state)
        self.clean_up()
    
    
    def _on_edit(self):
        print('I hear you want to edit this b-spline...')
        
        new_state = state_MultilevelEditing_Editing.MultilevelEditingEditingState(self.base, self.content_frame, self.control_points)
        
        self.base.update_program_state(new_state)
        self.clean_up()
    
    
    def _on_discard(self):
        print('I hear you want to discard this b-spline...')
        self.base.exit_to_default()
    
    def clean_up(self):
        self.layout.clean_up()
        print('MultilevelEditingDefaultState cleaning up')
        
