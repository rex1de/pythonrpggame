from Unit import Unit
  
class Warrior(Unit):  # наследование класса Unit, изменение его свойств под класс воина
    
    def __init__(self, name):
        super().__init__(name, 100, self.stamina, 15, 5)
