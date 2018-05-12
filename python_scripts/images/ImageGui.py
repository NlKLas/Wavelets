import tkinter as tk
from tkinter import ttk

import state_Default

class ImageGui:
    
    def __init__(self):
        
        self.root = tk.Tk()
        
        self.root.title('ImageGui')
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        
        self.content_frame = ttk.Frame(self.root, padding=3)
        self.content_frame.grid(column=0, row=0, sticky=('W','N','E','S'))
        
        
        self.root.bind('<Control-w>', self._done)
        
        self.program_state = state_Default.DefaultState(self, self.content_frame)
    
    
    def update_program_state(self, new_state):
        self.program_state = new_state
        
    def show(self):
        self.root.mainloop()
    
    def _done(self, evt=None):
        print('Bye!')
        self.root.quit()
        self.root.destroy()
        


if __name__ == '__main__':
    ImageGui().show()
