class Effect:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        
    def apply(self, target):
        pass
       
    def remove(self, target):
        pass
    
class Defense(Effect):
    def __init__(self, name, duration):
        super().__init__(name, duration)
        self.defense = 0
        
    def apply(self, target):
        self.defense = target.defense
        target.defense += self.defense * 0.05
        
    def remove(self, target):
        target.defense -= self.defense * 0.05

class Poison(Effect):
    def __init__(self, name, duration):
        super().__init__(name, duration)
        
    def tick(self, target):
        target.health -= 10
        
    

    