import matplotlib
from matplotlib.figure import Figure

import state_MultilevelEditing_Default
import layout_MultilevelEditing_Editing
from b_splines import createFiltersAndProjectionsForMLE, completeDecomposition, updateCompleteDecomposition, plot_uniform_b_spline_curve

import numpy as np

class MultilevelEditingEditingState:
    
    def __init__(self, base, content_frame, control_points):
        print('hi from MultilevelEditingEditingState')
        
        self.base = base
        self.content_frame = content_frame
        
        self.n = control_points.shape[0]-3
        self.max_lod = np.around(np.log2(self.n)).astype(int)
        
        self.projectionsP, self.filters = createFiltersAndProjectionsForMLE(self.max_lod)
        
        self.lod_approximations = completeDecomposition(control_points, self.filters)
        
        self.current_display_lod = self.max_lod
        self.current_edit_lod = self.max_lod
        
        
        self.fig = Figure()
        
        self.layout = layout_MultilevelEditing_Editing.MultilevelEditingEditingLayout(self.content_frame, self.fig, self.max_lod)
        
        self.layout.set_display_lod_scale_callback(self._on_display_lod_scale_event)
        self.layout.set_edit_lod_scale_callback(self._on_edit_lod_scale_event)
        self.layout.set_back_callback(self._on_back)
        
        self.layout.set_display_lod_scale_value(self.current_display_lod)
        self.layout.set_edit_lod_scale_value(self.current_edit_lod)
        
        self.cids = []
        self.cids.append(self.layout.mpl_connect('button_press_event', self._on_mouse_press))
        self.cids.append(self.layout.mpl_connect('motion_notify_event', self._on_mouse_move))
        self.cids.append(self.layout.mpl_connect('button_release_event', self._on_mouse_release))
        
        
        self.ax = self.fig.add_subplot(111)
        
        self.plot_curve_on_current_lods()
        
        #ideally this would be dynamicly computed... or done in screen coordinates...
        self.select_dist2 = 0.01*0.01
        self.index_selected_point = -1
        
    
    
    def _on_mouse_press(self, evt):
        if evt.inaxes:
            #maybe switch to screen coordinates for this calculation
            edit_control_points = self.lod_approximations[self.current_edit_lod]
            dx = edit_control_points[:,0] - evt.xdata
            dy = edit_control_points[:,1] - evt.ydata
            dist2 = dx*dx + dy*dy
            ind = np.argmin(dist2)
            if dist2[ind] < self.select_dist2:
                print(ind) 
                self.index_selected_point = ind
    
    def _on_mouse_move(self, evt):
        if evt.inaxes:
            if self.index_selected_point >= 0:
                edit_control_points = self.lod_approximations[self.current_edit_lod]
                delta_x = evt.xdata - edit_control_points[self.index_selected_point,0]
                delta_y = evt.ydata - edit_control_points[self.index_selected_point,1]
                #print([delta_x, delta_y])
                
                deltaC_j = np.zeros_like(edit_control_points)
                deltaC_j[self.index_selected_point,0] = delta_x
                deltaC_j[self.index_selected_point,1] = delta_y
                
                self.lod_approximations = updateCompleteDecomposition(deltaC_j, self.lod_approximations, self.projectionsP, self.filters)
                
                self.plot_curve_on_current_lods()
                
                
    
    def _on_mouse_release(self, evt):
        self.index_selected_point = -1
        
    def plot_curve_on_current_lods(self):
        #print('I hear you want to plot the curve on a new lod...')
        self.ax.clear()
        self.ax.set_xlim(0,1)
        self.ax.set_ylim(0,1)
        
        display_data = self.lod_approximations[self.current_display_lod]
        edit_data = self.lod_approximations[self.current_edit_lod]
        
        plot_uniform_b_spline_curve(self.ax, display_data, degree=3, N=1000, color='black')
        self.ax.scatter(edit_data[:,0], edit_data[:,1], color='blue', picker=True)
        plot_uniform_b_spline_curve(self.ax, edit_data, degree=3, N=1000, color='red', ls='--')
        
        self.layout.redraw_figure()
    
    
    
    
    def _on_display_lod_scale_event(self, evt):
        value = float(evt)
        #tolerance around the integer values
        eps = 0.00001
        #reject non integer values
        if np.abs(np.around(value)-value) > eps:
            self.layout.set_display_lod_scale_value(np.around(value))
        #update if a new integer value is reached
        elif np.abs(self.current_display_lod - value) > eps:
            self.update_display_lod(value)
    
    def update_display_lod(self, value):
        print('I hear you want to change the display lod...')
        self.current_display_lod = np.around(value).astype(int)
        self.plot_curve_on_current_lods()
    
    
    
    
    
    def _on_edit_lod_scale_event(self, evt):
        value = float(evt)
        #tolerance around the integer values
        eps = 0.00001
        #reject non integer values
        if np.abs(np.around(value)-value) > eps:
            self.layout.set_edit_lod_scale_value(np.around(value))
        #update if a new integer value is reached
        elif np.abs(self.current_edit_lod - value) > eps:
            self.update_edit_lod(value)
    
    def update_edit_lod(self, value):
        print('I hear you want to change the editing lod...')
        self.current_edit_lod = np.around(value).astype(int)
        self.edit_control_points = self.lod_approximations[self.current_edit_lod]
        self.plot_curve_on_current_lods()
    
    
    
    
    
    
    def _on_back(self):
        print('I hear you want to go back...')
        
        new_state = state_MultilevelEditing_Default.MultilevelEditingDefaultState(self.base, self.content_frame, self.lod_approximations[-1])
        
        self.base.update_program_state(new_state)
        self.clean_up()
    
    def clean_up(self):
        for cid in self.cids:
            self.layout.mpl_disconnect(cid)
        self.layout.clean_up()
        print('MultilevelEditingEditingState cleaning up')
