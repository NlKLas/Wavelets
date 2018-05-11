
import state_Default
import state_MultilevelEditing_Default

class MultilevelEditingState:
    
    def __init__(self, base, content_frame, control_points):
        print('hi from MultilevelEditingState')
        
        self.base = base
        self.content_frame = content_frame
        
        
        self.substate = state_MultilevelEditing_Default.MultilevelEditingDefaultState(self, self.content_frame, control_points)
    
    
    def exit_to_default(self):
        print('leaving MultilevelEditingState')
        
        new_state = state_Default.DefaultState(self.base, self.content_frame)
        
        self.base.update_program_state(new_state)
        self.clean_up()
    
    def update_program_state(self, new_state):
        self.substate = new_state
    
    def clean_up(self):
        self.substate.clean_up()
        print('MultilevelEditingState cleaning up')
