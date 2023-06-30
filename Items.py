from Effects import *


class Item:
    classes = ['warrior', 'archer', 'mage']
    default_quantity = 1
    default_max_quantity = 1

    def __init__(self, name, price, sprite, quantity=default_quantity, max_quantity=default_max_quantity, available_classes=classes):
        self.name = name
        self.quantity = quantity
        self.max_quantity = max_quantity
        self._price = price
        self.sprite = sprite
        self.available_classes = available_classes

    def __str__(self):
        return self.name

    def use(self, target):
        pass

    def print_stats(self):
        pass

    @property
    def price(self):
        return self._price * self.quantity


class Equipment(Item):
    def __init__(self, name, slot, price, sprite):
        super().__init__(name, price, sprite)
        self.slot = slot

    def equip(self, target):
        pass

    def unequip(self, target):
        pass


class Armour(Equipment):

    def __init__(self, name, slot, price, defense_buff, sprite):
        super().__init__(name, slot, price, sprite)
        self.defense_buff = defense_buff

    def equip(self, target):
        target.defense += self.defense_buff

    def unequip(self, target):
        target.defense -= self.defense_buff

    def print_stats(self):
        return f'Защита: {self.defense_buff}, слот для экипировки: {self.slot}, цена: {self.price}'


class Helmet(Armour):
    def __init__(self, name, price, defense_buff, sprite):
        super().__init__(name, 'Helmet', price, defense_buff, sprite )


class Chestplate(Armour):
    def __init__(self, name, price, defense_buff, sprite):
        super().__init__(name, 'Chestplate', price, defense_buff, sprite)


class Leggins(Armour):
    def __init__(self, name, price, defense_buff, sprite):
        super().__init__(name, 'Leggins', price, defense_buff, sprite)


class Shield(Armour):
    def __init__(self, name, price, defense_buff, sprite):
        super().__init__(name, 'Left_hand', price, defense_buff, sprite,)


class Weapon(Equipment):

    def __init__(self, name, slot, price, damage_buff, sprite):
        super().__init__(name, slot, price, sprite)
        self.damage_buff = damage_buff
    def equip(self, target):
        target.damage += self.damage_buff

    def unequip(self, target):
        target.damage -= self.damage_buff

    def print_stats(self):
        return f'Урон: {self.damage_buff}, слот для экипировки: {self.slot}, цена: {self.price}'

class Bow(Weapon):
    classes = ['archer']

    def __init__(self, name, price, damage_buff, sprite, available_classes=classes):
        super().__init__(name, 'Right_hand', price, damage_buff, sprite)
        self.available_classes = available_classes


class Sword(Weapon):
    classes = ['warrior']

    def __init__(self, name, price, damage_buff, sprite, available_classes=classes):
        super().__init__(name, 'Right_hand', price, damage_buff, sprite)
        self.available_classes = available_classes


class Magic_wand(Weapon):
    classes = ['mage']

    def __init__(self, name, price, damage_buff, sprite, available_classes=classes):
        super().__init__(name, 'Right_hand', price, damage_buff, sprite)
        self.available_classes = available_classes


class Potion(Item):
    def __init__(self, name, price, sprite, quantity=1, max_quantity=5):
        super().__init__(name, price, sprite, quantity, max_quantity)

    def use(self, target, value):
        self.quantity -= 1


class Heal_potion(Potion):
    def __init__(self, name, price, sprite, quantity=1, max_quantity=5):
        super().__init__(name, price, sprite, quantity, max_quantity)

    def use(self, target):
        target.health += 35
        self.quantity -= 1

    def print_stats(self):
        return f'Восстанавливает 35 единиц здоровья за раз. Цена: {self.price}'


class Poison_potion(Potion):
    def __init__(self, name, price, sprite, quantity=1, max_quantity=5):
        super().__init__(name, price, sprite, quantity, max_quantity)

    def use(self, target):
        target.apply_effect(Poison('poison', 3))
        self.quantity -= 1

    def print_stats(self):
        return f'Наносит 10 единиц урона в течении 3 раундов. Цена: {self.price}'
