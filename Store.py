import random
class Store:
    itemlist = []
    def __init__(self, itemscount):
        self.itemscount = itemscount
        self.pool = random.SystemRandom().sample(self.itemscount, Store.itemlist)
        
    def print(self):
        for count, item in enumerate(self.pool):
            itemlist += str(count) + '. ' + item.name + ' '
        print(itemlist)
    
    def buy_item(self, index, character):
        if character.money >= self.pool[index].buy_price:
            character.money -= self.pool[index].buy_price
            character.add_to_inventory(self.pool[index])
            print(f'Вы успешно купили {self.pool[index].name}.')     
        else:
            print('У вас недостаточно денег')
            
    def sell_item(self, item, character):
        character.money += item.sell_price
        character.remove_from_inventory(item)
        print(f'Вы успешно продали {item.name}')
        self.pool.append(item)
        
    