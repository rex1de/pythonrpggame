from Effects import *
class Item:
    default_quantity = 1
    default_max_quantity = 1
    def __init__(self, name, buy_price, sell_price, quantity=default_quantity, max_quantity=default_max_quantity):
        self.name = name
        self.quantity = quantity
        self.max_quantity = max_quantity
        self.buy_price = buy_price
        self.sell_price = sell_price
        
    def __str__(self):
        return self.name
        
    def use(self, target):
        pass
     
class Equipment(Item):
    def __init__(self, name, slot, buy_price, sell_price):
        super().__init__(name, buy_price, sell_price)
        self.name = name
        self.slot = slot

    def equip(self, target):
        pass
        
    def unequip(self, target):
        pass
    
class Armour(Equipment):
    
    def __init__(self, name, slot, defense_buff, buy_price, sell_price):
        super().__init__(name, slot, buy_price, sell_price)
        self.defense_buff = defense_buff
        self.buy_price = buy_price
        self.sell_price = sell_price
        
    def equip(self, target):
        target.defense += self.defense_buff 
        
    def unequip(self, target):
        target.defense -= self.defense_buff
       
class Weapon(Equipment):
    
    def __init__(self, name, slot, damage_buff, buy_price, sell_price):
        super().__init__(name, slot, buy_price, sell_price)
        self.damage_buff = damage_buff
        self.buy_price = buy_price
        self.sell_price = sell_price
        
    def equip(self, target):
        target.damage += self.damage_buff
        
    def unequip(self, target):
        target.damage -= self.damage_buff

class Potion(Item):
    def __init__(self, name):
        super().__init__(name, 100, 50)
    
    def use(self, target, value):
        self.quantity -= 1

class Heal_potion(Potion):
    def __init__(self, name):
        super().__init__(name)
        
    def use(self, target):
        target.health += 35
        self.quantity -= 1
        
class Poison_potion(Potion):
    def __init__(self, name):
        super().__init__(name)
    
    def use(self, target):
        target.apply_effect(Poison('poison', 3))
        self.quantity -= 1