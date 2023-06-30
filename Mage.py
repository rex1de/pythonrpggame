from Unit import Unit
class Mage(Unit):   # наследование класса Unit, изменение его свойств под класс мага
    def __init__(self, name):
        super().__init__(name, 75, self.stamina, 20, 5, 'mage')
        self.mana = 100
        self.stamina_up = 15
        self.mana_up = 15
        
    def attack(self, character):
        if character.defense >= self.damage:
            return f'{character.name} защитился от удара'
        else:
            character.take_damage(self.damage)
            self.mana -= 15
            return f'{self.name} ударил {character.name}: нанесено урона: {round(self.damage - character.defense, 1)}, здоровье {character.name}: {character.health}'
   
    def rest(self):
        self.stamina += 15
        self.mana += self.mana_up
        return f'{self.name} восстановил энергию и ману!'
    