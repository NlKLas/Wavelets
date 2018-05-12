from tkinter import filedialog

import layout_Default
import state_ImageLoaded

import PIL
import numpy as np

class DefaultState:
    
    def __init__(self, base, content_frame):
        print('hi from DefaultState')
        
        self.base = base
        self.content_frame = content_frame
        
        
        self.layout = layout_Default.DefaultLayout(self.content_frame)
        
        self.layout.set_load_img_callback(self._on_load_image)
    
    
    def _on_load_image(self):
        filename = filedialog.askopenfilename(title='Select an Image')
        print(filename)
        
        # I should really check that the image has proper dimensions.....
        image = np.asarray(PIL.Image.open(filename))    
        image = np.mean(image, axis=2)
        
        self.layout.clean_up()
        new_state = state_ImageLoaded.ImageLoadedState(self.base, self.content_frame, image)
        
        self.base.update_program_state(new_state)
        self.clean_up()
    
    
    def clean_up(self):
        pass
