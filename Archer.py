from Unit import Unit
class Archer(Unit):    # наследование класса Unit, изменение его свойств под класс лучника

    def __init__(self, name):
        super().__init__(name, 100, self.stamina, 15, 3)
        self.arrows = 3
        
    def attack(self, character):
        if character.defense >= self.damage:
            print(f'{character.name} защитился от удара')
        else:
            character.take_damage(self.damage)
            self.arrows -= 1
            print(f'{self.name} ударил {character.name}: нанесено урона: {self.damage - character.defense}, здоровье: {character.health}')
        if self.arrows == 0:
            self.rest()
        
    def rest(self):
        self.stamina += 15
        self.arrows += 1
        print(f'{self.name} восстановил энергию и перезарядился!')