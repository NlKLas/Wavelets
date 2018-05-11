from matplotlib.figure import Figure

import numpy as np

import state_MultilevelEditing_Default
import layout_MultilevelEditing_Smoothing
from b_splines import plot_uniform_b_spline_curve, completeDecomposition

class MultilevelEditingSmoothingState:
    
    def __init__(self, base, content_frame, control_points):
        print('hi from MultilevelEditingSmoothingState')
        
        self.base = base
        self.content_frame = content_frame
        
        self.control_points = control_points
        self.n = self.control_points.shape[0]-3
        self.max_lod = np.around(np.log2(self.n)).astype(int)
        
        self.lod_approximations = completeDecomposition(self.control_points)
        
        
        self.fig = Figure()
        
        self.layout = layout_MultilevelEditing_Smoothing.MultilevelEditingSmoothingLayout(self.content_frame, self.fig, self.max_lod)
        
        self.layout.set_lod_scale_callback(self._on_lod_scale_event)
        self.layout.set_back_callback(self._on_back)
        
        
        self.current_lod = self.max_lod
        self.layout.set_lod_scale_value(self.current_lod)
        
        self.layout.set_num_points(self.n+3)
        
        
        self.ax = self.fig.add_subplot(111)
        self.plot_curve_on_current_lod()
        
    
    
    def plot_curve_on_current_lod(self):
        print('I hear you want to plot the curve on a new lod...')
        self.ax.clear()
        self.ax.set_xlim(0,1)
        self.ax.set_ylim(0,1)
        
        data = self.lod_approximations[self.current_lod]
        
        self.ax.scatter(data[:,0], data[:,1])
        plot_uniform_b_spline_curve(self.ax, data, degree=3, N=1000, color='black')
        
        self.layout.redraw_figure()
    
    def _on_lod_scale_event(self, evt):
        #print('I hear you want to adjust the level of smoothing')
        value = float(evt)
        #tolerance around the integer values
        eps = 0.00001
        #reject non integer values
        if np.abs(np.around(value)-value) > eps:
            self.layout.set_lod_scale_value(np.around(value))
        #update if a new integer value is reached
        elif np.abs(self.current_lod - value) > eps:
            self.update_lod(value)
    
    def update_lod(self, value):
        print('I hear you want to change the lod...')
        self.current_lod = np.around(value).astype(int)
        self.layout.set_num_points((self.lod_approximations[self.current_lod]).shape[0])
        self.plot_curve_on_current_lod()
    
    
    
    def _on_back(self):
        print('I hear you want to go back...')
        
        new_state = state_MultilevelEditing_Default.MultilevelEditingDefaultState(self.base, self.content_frame, self.control_points)
        
        self.base.update_program_state(new_state)
        self.clean_up()
    
    def clean_up(self):
        self.layout.clean_up()
        print('MultilevelEditingSmoothingState cleaning up')
