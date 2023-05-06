import random
from Unit import *
from Archer import *
from Warrior import *
from Mage import *
from Items import *
from Enemies import *
from Store import *
def fight_with_monster(char1, monster):
    while char1.health > 0 and monster.health > 0:
        a = int(input('Выберите действие: 1. Атака, 2. Защита, 3. Отдых, 4. Воспользоваться предметом из инвентаря. \n'))
        if a == 1:
            char1.attack(monster)
        elif a == 2:
            char1.defend()
        elif a == 3:
            char1.rest()
        elif a == 4:
            char1.show_inventory()
            choose = int(input())
            item = char1.inventory[choose]
            char1.use(monster, item)
        print('Теперь очередь противника')
        monster.attack(char1)
        char1.end_turn()
        if monster.health <= 0 < char1.health:  
            char1.gain_exp()  
            print(f"{char1.name} победил и ему было добавлено {Unit.exp_up},  опыта \nВ ваш инвентарь был добавлен новый предмет")
            monster.death(char1)
        elif char1.health <= 0 < monster.health:
            print(f"Вы погибли!")

def arena(char1, char2):  # функция битвы
    while char1.health > 0 and char2.health > 0:
        a = int(input('Выберите действие: 1. Атака, 2. Защита, 3. Отдых, 4. Воспользоваться предметом из инвентаря. \n'))
        if a == 1:
            char1.attack(char2)
        elif a == 2:
            char1.defend()
        elif a == 3:
            char1.rest()
        elif a == 4:
            char1.show_inventory()
            choose = int(input())
            item = char1.inventory[choose]
            use = int(input('На кого вы хотите использовать этот предмет?\n 1. На себя 2. На противника'))
            char1.use(char1, item) if use == 1 else char1.use(char2, item)
        print('Теперь очередь противника')
        b = random.randint(1,3)
        if b == 1:
            char2.attack(char1)
        elif b == 2:
            char2.defend()   
        elif b == 3:
            char2.rest()
        char2.attack(char1)
        char1.end_turn()
        char2.end_turn()
        if char2.health <= 0 < char1.health: 
            char1.gain_exp()  
            print(f"{char1.name} победил и ему было добавлено {Unit.exp_up} опыта,\nВ ваш инвентарь был добавлен новый предмет")
        elif char1.health <= 0 < char2.health:
            char2.gain_exp()
            print(f"{char2.name} победил и ему было добавлено {Unit.exp_up} опыта")

store = Store(6)
mage = Mage('John')
warrior = Warrior('Liam')
ogre = Ogre('Огр', 3)
run = True
while run:
    choose = int(input('Куда отправимся? 1. На арену 2. Драться с монстрами 3. В магазин 4. Выход из игры \n'))
    if choose == 1:
        arena(warrior, mage)
    if choose == 2:
        fight_with_monster(warrior, ogre)
    if choose == 3:
        store.print()
    if choose == 4:
        run = False