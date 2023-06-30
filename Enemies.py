from Items import *


class Monster:
    def __init__(self, name, health, damage, defense, lvl):
        self.lvl = lvl
        self.name = name
        self._health = health * (1 + (0.03 * lvl))
        self.damage = damage * (1 + (0.03 * lvl))
        self.defense = defense * (1 + (0.03 * lvl))

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if value < 0:
            self._health = 0
        else:
            self._health = int(value)

    def attack(self, character):
        if character.defense >= self.damage:
            print(f'{character.name} защитился от удара')
        else:
            character.take_damage(self.damage)
            print(f'{self.name} ударил {character.name}: нанесено урона: {round(self.damage - character.defense, 1)}, здоровье {character.name}: {character.health}')

    def death(self, character):
        pass

    def take_damage(self, value):
        self.health -= value - self.defense


class Ogre(Monster):
    def __init__(self, name, lvl):
        super().__init__(name, 100, 15, 0.05, lvl)

    def death(self, character):
        character.add_to_inventory(
            Weapon("Ogre's club", "left_hand", 1000, 10))
