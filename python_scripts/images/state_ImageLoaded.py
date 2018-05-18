import matplotlib
matplotlib.use('TkAgg')

from matplotlib.figure import Figure

import state_Default
import layout_ImageLoaded

from images import decompose_sort, cumulative_squared_error, eval_piecewise_linear, get_arc_length_seq, partially_reconstruct_img

import numpy as np

class ImageLoadedState:
    
    def __init__(self, base, content_frame, image):
        print('hi from ImageLoadedState')
        
        self.base = base
        self.content_frame = content_frame
        
        self.image = image
        self.image_reconstruction = self.image
        
        self.transform, self.sort_indices = decompose_sort(self.image, nonstandard=True)
        self.cum_err2 = cumulative_squared_error(self.transform, self.sort_indices)
        
        self.plot_x = np.linspace(1,0, self.cum_err2.size)
        self.plot_y = np.sqrt(self.cum_err2/self.cum_err2[-1])
        
        self.plot_data = np.hstack((self.plot_x.reshape((-1,1)),self.plot_y.reshape((-1,1))))
        self.arc_length_seq = get_arc_length_seq(self.plot_data)
        
        self.plot_t = np.linspace(0, self.arc_length_seq[-1], 1000)
        
        self.curve_approx = eval_piecewise_linear(self.plot_t, self.plot_data, self.arc_length_seq)        
        
        self.total_num_coefficients = self.transform.size
        self.num_coefficients = self.total_num_coefficients
        
        
        self.x_worst_case = np.linspace(0,1,1000)
        self.y_worst_case = np.sqrt(1 - self.x_worst_case)
        
        
        self.img_fig = Figure()
        self.plot_fig = Figure()
        
        
        
        self.layout = layout_ImageLoaded.ImageLoadedLayout(self.content_frame, self.img_fig, self.plot_fig)
        
        self.layout.set_back_callback(self._on_back)
        
        self.img_cids = []
        self.plot_cids = []
        
        self.plot_cids.append(self.layout.plot_mpl_connect('button_press_event', self._on_mouse_press_plot))
        self.plot_cids.append(self.layout.plot_mpl_connect('motion_notify_event', self._on_mouse_move_plot))
        self.plot_cids.append(self.layout.plot_mpl_connect('button_release_event', self._on_mouse_release_plot))
        
        self.mouse_down = False
        
        self.img_ax = self.img_fig.add_subplot(111)
        self.plot_ax = self.plot_fig.add_subplot(111)
        
        
        self.update_img_fig()
        
        self.update_plot_fig()
        
    
    def update_plot_fig(self):
        self.plot_ax.clear()
        self.plot_ax.set_xlim(-0.1, 1.1)
        self.plot_ax.set_ylim(-0.1, 1.1)
        
        p = self.get_closest_data_point()
        self.plot_ax.scatter(p[0], p[1], color='red')
        self.plot_ax.axvline(p[0], color='red')
        self.plot_ax.axhline(p[1], color='red')
        
        self.plot_ax.set_title('Relative $L^2$-Error: {0:.2f}%'.format(p[1]*100))
        
        self.plot_ax.plot(self.curve_approx[:,0], self.curve_approx[:,1], color='blue')
        
        self.plot_ax.plot(self.x_worst_case, self.y_worst_case, color='black', ls='--')
        self.plot_ax.set_xlabel('Fraction of Coefficients Used')
        self.plot_ax.set_ylabel('Relative $L^2$-Error')
        self.plot_ax.grid()
        self.layout.redraw_plot_fig()
        
        
    
    def update_img_fig(self):
        self.img_ax.clear()
        self.img_ax.set_title(str(self.num_coefficients)+'/'+str(self.total_num_coefficients)+' coefficients used')
        self.img_ax.imshow(self.image_reconstruction, cmap='gray')
        self.layout.redraw_img_fig()
    
    
    def _on_mouse_press_plot(self, evt):
        if evt.inaxes:
            self.mouse_down = True
    
    def _on_mouse_move_plot(self, evt):
        if evt.inaxes:
            if self.mouse_down:
                self.update_num_coefficients(self.closest_approx_point_ind(evt.xdata, evt.ydata))
                self.update_plot_fig()
    
    def _on_mouse_release_plot(self, evt):
        if evt.inaxes:
            if self.mouse_down:
                self.mouse_down = False
                self.update_num_coefficients(self.closest_approx_point_ind(evt.xdata, evt.ydata))
                self.update_plot_fig()
    
    def closest_approx_point_ind(self, x, y):
        dx = self.curve_approx[:,0] - x
        dy = self.curve_approx[:,1] - y
        dist2 = dx*dx + dy*dy
        ind = np.argmin(dist2)
        return ind
    
    def update_num_coefficients(self, selected_index):
        self.num_coefficients = np.around(self.curve_approx[selected_index, 0] * self.total_num_coefficients).astype(int)
        #print(self.num_coefficients)
        self.image_reconstruction = partially_reconstruct_img(self.transform, self.sort_indices, self.num_coefficients, nonstandard=True)
        self.update_img_fig()
    
    
    def get_closest_data_point(self):        
        x = self.num_coefficients/self.total_num_coefficients
        # this is the number of not used coefficients; it is also the index into y, as y
        # contains an additional data point at 0 coefficients used...
        ind = self.total_num_coefficients - self.num_coefficients
        y = self.plot_y[ind]
        
        return [x, y]
        
    
    def _on_back(self):
        self.clean_up()
        self.layout.clean_up()
        new_state = state_Default.DefaultState(self.base, self.content_frame)
        
        self.base.update_program_state(new_state)
    
    def clean_up(self):
        for cid in self.img_cids:
            self.layout.img_mpl_disconnect(cid)
        
        for cid in self.plot_cids:
            self.layout.plot_mpl_disconnect(cid)
