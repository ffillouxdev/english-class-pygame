class Character :
    def __init__(self,name):
        self.axeXpos = 0
        self.axeYpos = 0
        self.health = 100
        self.name = name

    def forward(self): 
        self.axeXpos += 10

    def backward(self):
        self.axeXpos -= 10
    
    def jump(self):
        self.axeYpos += 10
    
    def Crouch(self):
        self.axeYpos -= 10

    def hurt(self, damage):
        self.health -= damage        
        
    


