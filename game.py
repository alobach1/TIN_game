 
class Player:
    def __init__(self):
        self.state = 1

    def get_state(self):
        return self.state

    def set_state(self,data):
        self.state = data - self.state  
        return self.state
