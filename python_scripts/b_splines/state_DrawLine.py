from matplotlib.figure import Figure

import numpy as np

import state_Default
import layout_DrawLine
import state_MultilevelEditing
from b_splines import upsample, interpolateCubic

class DrawLineState:
    
    def __init__(self, base, content_frame, figure=None):
        print('hi from DrawLineState')
        
        self.base = base
        self.content_frame = content_frame
        self.fig = figure
        
        if not self.fig:
            self.fig = Figure()
        
        self.layout = layout_DrawLine.DrawLineLayout(self.content_frame, self.fig)
        
        self.layout.set_upsample_callback(self._on_upsample)
        self.layout.set_done_callback(self._on_done)
        self.layout.set_discard_callback(self._on_discard)
        
        
        
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0,1)
        self.ax.set_ylim(0,1)
        self.layout.redraw_figure()
        
        self.x = []
        self.y = []
        
        self.data = None
        
        self.cids = []
        
        self.mouse_down = False
        
        self.start_recording()
        
    
    def _on_discard(self):
        print('I hear you want to discard your line...')
        
        new_state = state_Default.DefaultState(self.base, self.content_frame)
        
        self.base.update_program_state(new_state)
        self.clean_up()
        self.layout.clean_up()
    
    def _on_upsample(self):
        print('I hear you want to upsample...')
        if self.data is None:
            self.data = np.hstack((np.array(self.x).reshape((-1,1)),np.array(self.y).reshape((-1,1))))
        self.data = upsample(self.data)
        
        self.layout.set_num_points(self.data.shape[0])
        
        self.ax.clear()
        self.ax.set_xlim(0,1)
        self.ax.set_ylim(0,1)
        self.ax.plot(self.data[:,0], self.data[:,1], color='black')
        self.layout.redraw_figure()
        
        self.layout.enable_done_btn()
    
    def _on_done(self):
        print('I hear you are done drawing...')
        
        control_points = interpolateCubic(self.data)
        new_state = state_MultilevelEditing.MultilevelEditingState(self.base, self.content_frame, control_points)
        
        self.base.update_program_state(new_state)
        self.clean_up()
    
    def clean_up(self):
        self.layout.clean_up()
        print('DrawLineState cleaning up')
    
    
    def start_recording(self):
        if not self.cids:
            self.cids.append(self.layout.mpl_connect('button_press_event', self._on_mouse_press))
            self.cids.append(self.layout.mpl_connect('motion_notify_event', self._on_mouse_motion))
            self.cids.append(self.layout.mpl_connect('button_release_event', self._on_mouse_release))
            print("Started Recording!")
        else:
            print("Already Recording!!!")
    
    
    def stop_recording(self):
        while self.cids:
            self.layout.mpl_disconnect(self.cids.pop())
        print("Stopped Recording!")
        self.data = np.hstack((np.array(self.x).reshape((-1,1)),np.array(self.y).reshape((-1,1))))
        self.layout.enable_upsample_btn()
        
        n = self.data.shape[0]-1
        m = np.around(np.power(2, np.ceil(np.log2(n)))).astype(int)
        if n == m:
            self.layout.enable_done_btn()
        
    
    def _on_mouse_press(self, evt):
        if evt.inaxes:
            self.mouse_down = True
            self.add_point(evt.xdata, evt.ydata)
    
    
    def _on_mouse_motion(self, evt):
        if evt.inaxes:
            if self.mouse_down:
                if self.x:
                    self.ax.plot([self.x[-1], evt.xdata], [self.y[-1], evt.ydata], color='black')
                    self.layout.redraw_figure()
                
                self.add_point(evt.xdata, evt.ydata)
    
    
    def _on_mouse_release(self, evt):
        if evt.inaxes:
            if self.mouse_down:
                self.add_point(evt.xdata, evt.ydata)
                self.stop_recording()
            self.mouse_down = False
    
     
    def add_point(self, xdata, ydata):
        if xdata and ydata:
            self.x.append(xdata)
            self.y.append(ydata)
        
            self.layout.set_num_points(len(self.x))
