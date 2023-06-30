from Effects import *
from Items import *
import pygame 


class Unit:   # главный абстрактный класс, как бы шаблон, с помощью которого создаем настоящих героев, изменяя их свойства
    stamina = 100
    mana = 100
    arrows = 0
    exp_up = 300
    capacity = 10
    money = 10000
    slot_rus = {
        'Helmet': 'Шлем',
        'Chestplate': 'Нагрудник',
        'Leggins': 'Поножи',
        'Left_hand': 'Левая рука',
        'Right_hand': 'Правая рука'
    }

    def __init__(self, name, health, stamina, damage, defense, spec):
        self.name = name
        self._health = health
        self.stamina = stamina
        self.damage = damage
        self.defense = defense
        self.mana = 0
        self.arrows = 0
        self.mana_up = 15
        self.stamina_up = 15
        self.needed_exp = 1000
        self.exp = 0
        self.max_hp = 100
        self.lvl = 1
        self.effects = {}
        self.spec = spec
        self.inventory = []

        self.equipment = {
            'Helmet': None,
            'Chestplate': None,
            'Leggins': None,
            'Left_hand': None,
            'Right_hand': None
        }

    @property  # геттер здоровья
    def health(self):
        return self._health

    @health.setter  # сеттер здоровья
    def health(self, value):
        if value < 0:
            self._health = 0
        elif value > self.max_hp:
            self._health = self.max_hp
        else:
            self._health = int(value)

    # действия (атака, защита, отдых)

    def attack(self, character):
        if character.defense >= self.damage:
            return f'{character.name} защитился от удара'
        else:
            character.take_damage(self.damage)
            self.stamina -= 15
            return f'{self.name} ударил {character.name}: нанесено урона: {round(self.damage - character.defense, 1)}, здоровье {character.name}: {character.health}'

    def rest(self):
        self.stamina += 15
        return '{self.name} восстановил энергию!'

    def defend(self):
        effect = Defense('defense', 2)
        self.apply_effect(effect)
        return f'{self.name} увеличил свою защиту!'

    def __lvl_up(self):
        self.lvl += 1
        print(
            f'Поздравляем, ваш уровень повышен! Теперь ваш герой {self.lvl} уровня. Все характеристики повышены')
        self.damage = self.damage * 1.05
        self.defense = self.defense * 1.05
        self.stamina = self.stamina * 1.05
        self.mana = self.mana * 1.05
        self.needed_exp = self.needed_exp * 1.25

    def gain_exp(self):
        self.exp += self.exp_up
        if self.exp >= self.needed_exp:
            self.__lvl_up()

    def take_damage(self, value):
        self.health -= value - self.defense

    def apply_effect(self, effect):
        effect.apply(self)
        self.effects[effect.name] = effect

    def end_turn(self):
        lst = []
        for name, effect in self.effects.items():
            effect.duration -= 1
            if effect.duration == 0:
                lst.append(name)
            if hasattr(effect, 'tick'):
                effect.tick(self)
        for name in lst:
            self.effects[name].remove(self)
            del self.effects[name]

    def add_to_inventory(self, item):
        for old_item in self.inventory:
            if item.name == old_item.name:
                if old_item.quantity + item.quantity <= old_item.max_quantity:
                    old_item.quantity += item.quantity
                else:
                    item.quantity -= (old_item.max_quantity -
                                      old_item.quantity)
                    old_item.quantity = old_item.max_quantity
                    if len(self.inventory) < Unit.capacity:
                        self.inventory.append(item)
        if len(self.inventory) < Unit.capacity:
            self.inventory.append(item)

    def remove_from_inventory(self, item):
        self.inventory.remove(item)

    def use(self, target, item):
        if not hasattr(item, 'equip'):
            item.use(target)
            if item.quantity <= 0:
                self.remove_from_inventory(item)
            print(f'Вы использовали предмет {item.name}')
            return True
        else:
            return False

    def equip(self, equipment):
        if hasattr(equipment, 'equip'):
            if self.spec in equipment.available_classes:
                for name, value in self.equipment.items():
                    if equipment.slot == name and value == None:
                        equipment.equip(self)
                        self.equipment[name] = equipment
                        print(
                            f'Вы экипировали предмет {equipment.name}')
                        self.remove_from_inventory(equipment)
                        return True
            else:
                print(
                    'Предмет не соответствует вашему классу!')
                return False
        else:
            print('Этот предмет нельзя экипировать!')
            return False

    def unequip(self, equipment):
        for name, value in self.equipment.items():
            if equipment.slot == name and value != None:
                equipment.unequip(self)
                self.equipment[name] = None
                self.add_to_inventory(equipment)
                print(f'Вы сняли предмет {equipment.name}')

    def show_inventory(self):
        for count, item in enumerate(self.inventory):
            print(str(count) + '. ' + item.name + ' ')

    def show_equipment(self):
        for slot, item in self.equipment.items():
            if item == None:
                print(Unit.slot_rus[slot] + ': ' + 'Пусто' + ' ')
            elif item != None:
                print(Unit.slot_rus[slot] + ': ' + item.name + ' ')
