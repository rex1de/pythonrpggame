from Items import *
import random, pygame

class Store:
    itemlist = [Heal_potion('Heal Potion', 100, pygame.transform.scale(pygame.image.load(r"assets\sprites\items\LifePot.png"), (50,50))),
                Poison_potion('Poison Potion', 100, pygame.transform.scale(pygame.image.load(r"assets\sprites\items\poison.png"), (50,50))),
                Sword("Ogre's club", 1000, 10, pygame.transform.scale(pygame.image.load(r"assets\sprites\items\club.png"), (50,50))),
                Helmet('Iron Helmet', 500, 5, pygame.transform.scale(pygame.image.load(r"assets\sprites\items\armour1.png"), (50,50))),
                Sword("Steel sword", 850, 7, pygame.transform.scale(pygame.image.load(r"assets\sprites\items\sword.png"), (50,50))),
                Leggins('Iron leggins', 500, 5, pygame.transform.scale(pygame.image.load(r"assets\sprites\items\armour3.png"), (50,50))),
                Chestplate('Iron chestplate', 800, 7, pygame.transform.scale(pygame.image.load(r"assets\sprites\items\armour2.png"), (50,50))),
                Bow('Compound Bow', 1000, 10, pygame.transform.scale(pygame.image.load(r"assets\sprites\items\bow.png"), (50,50))),
                Magic_wand('Magic wand', 1000, 10, pygame.transform.scale(pygame.image.load(r"assets\sprites\items\magic wand.png"), (50,50)))]

    def __init__(self, itemscount):
        self.itemscount = itemscount

    def print(self):
        for count, item in enumerate(self.pool):
            print(str(count + 1) + '. ' + item.name +
                  ' Цена: ' + str(item.price))

    def buy_item(self, character, index):
        if character.money >= self.pool[index].price:
            character.money -= self.pool[index].price
            character.add_to_inventory(self.pool[index])
            print(f'Вы успешно купили {self.pool[index].name}.')
            self.pool.remove(self.pool[index])
        else:
            print('У вас недостаточно денег')

    def sell_item(self, character, item):
        character.money += item.price - (item.price * 0.15)
        character.remove_from_inventory(item)
        print(f'Вы успешно продали {item.name}')
        self.pool.append(item)

    def refresh(self, character):
        spec_pool = []
        for item in Store.itemlist:
            if character.spec in item.available_classes:
                spec_pool.append(item)
        self.pool = random.SystemRandom().sample(spec_pool, self.itemscount)
        return self.pool
