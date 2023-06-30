import random, pygame, json, os, math
from Unit import *
from Archer import *
from Warrior import *
from Mage import *
from Items import *
from Enemies import *
from Store import *
from Render import *
from button import Button

def display():
    global screen
    screen = pygame.display.set_mode((1020, 1020))
    pygame.display.set_caption('Python RPG')
    
def text_formation(text):
    formated_string = ''
    lst = []
    for i in text:
        formated_string += i
        if len(formated_string) > 20 and i == ' ': # если длина передававаемой строки больше 20 символов, разделяет ее на насколько строк
            lst.append(formated_string) # и добавляет в список
            formated_string = ''
    lst.append(formated_string)
    return lst
        
def play_music(file):
    global is_music_paused
    if not is_music_paused:
        pygame.mixer.music.unload()
        pygame.mixer.music.load(file)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(loops=-1)
    elif is_music_paused: 
        is_music_paused = False
        pygame.mixer.music.unpause()

def pause_music():
    global is_music_paused
    pygame.mixer.music.pause()
    is_music_paused = True
    
def buy(name):
    for i in store.pool:
        if name == i.name:
            if main_char.money >= i.price:
                main_char.money -= i.price
                main_char.add_to_inventory(i) 
    menu_shop()    
    
# создает файл save.json и в виде словаря переносит все переменные
def save():
    data = {
    'name': main_char.name,
    'spec': main_char.spec,
    'money': main_char.money,
    'lvl': main_char.lvl,
    'exp': main_char.exp,
    'needed_exp': main_char.needed_exp,
    'inventory': [[i.name, i.quantity] for i in main_char.inventory],
    'equipment': [i.name for i in filter(lambda x : x, main_char.equipment.values())], 
    'health': main_char.health,
    'damage': main_char.damage,
    'defense': main_char.defense,
    'stamina': main_char.stamina,
    'mana': main_char.mana,
    'is_forest': is_forest,
    'is_arena': is_arena,
    'x': char_rect.draw_object.x,
    'y': char_rect.draw_object.y,
    'trees': [[i.draw_object.x, i.draw_object.y, i.draw_object.height, i.draw_object.width] for i in trees]
    }   
    
    with open("save.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load():
    global main_char
    global is_arena
    global is_forest
    with open('save.json', encoding="utf-8") as file:
        data = json.load(file)
        if data['spec'] == 'mage': # создание обьектов с загруженными переменными
            main_char = Mage(data['name'])
        elif data['spec'] == 'archer':
            main_char = Archer(data['name'])
        elif data['spec'] == 'warrior':
            main_char = Warrior(data['name'])
        main_char.money = data['money']
        main_char.lvl = data['lvl']
        main_char.exp = data['exp']
        main_char.needed_exp = data['needed_exp']
        main_char.health = data['health']
        main_char.damage = data['damage']
        main_char.defense = data['defense']
        main_char.stamina = data['stamina']
        main_char.mana = data['mana']
        char_rect.draw_object.x = data['x']
        char_rect.draw_object.y = data['y']
        is_arena = data['is_arena']
        is_forest = data['is_forest']
        # если предмет есть в списке всех предметов игры - он его добавляет в инвентарь    
        for i in range(len(data['inventory'])):
            for j in Store.itemlist:
                if data['inventory'][i][0] == j.name:
                    j.quantity = data['inventory'][i][1]
                    main_char.add_to_inventory(j)    
        # если предмет есть в списке всех предметов игры - он его экипирует    
        for i in range(len(data['equipment'])):
            for j in Store.itemlist:
                if data['equipment'][i] == j.name:
                    main_char.equip(j)
        trees.clear()
        for rect in data['trees']:
            trees.append(Render_object('', 'black', pygame.Rect(rect[0], rect[1], rect[2], rect[3]), pygame.Rect(rect[0], rect[1], rect[2], rect[3])))
    game()
    
def create_char(index, char_name):
    global main_char
    if index == 'Archer':
        main_char = Archer(char_name)
    elif index == 'Mage':
        main_char = Mage(char_name)
    else:
        main_char = Warrior(char_name)
        
def main_menu():
    while True:
        # простое меню, создает текст и кнопки 
        screen.fill('black')
        screen.blit(pygame.transform.scale(pygame.image.load(r'assets\sprites\menu_bg.jpg'), (1050,1050)), (0,0))
        mouse_pos = pygame.mouse.get_pos()
        main_menu_text = pygame.font.Font(r"assets\font.ttf", 50).render("Главное меню", True, "#b68f40")
        main_menu_rect = main_menu_text.get_rect(center=(510, 100))
        
        play = Button(image=None, pos=(510, 250), 
                            text_input="Играть", font=pygame.font.Font(r"assets\font.ttf", 50), base_color="#030303", hovering_color="#4f4f4f")
        options = Button(image=None, pos=(510, 400), 
                            text_input="Настройки", font=pygame.font.Font(r"assets\font.ttf", 50), base_color="#030303", hovering_color="#4f4f4f")
        quit = Button(image=None, pos=(510, 550), 
                            text_input="Выход", font=pygame.font.Font(r"assets\font.ttf", 50), base_color="#030303", hovering_color="#4f4f4f")

        screen.blit(main_menu_text, main_menu_rect)

        for button in [play, options, quit]:
            button.changeColor(mouse_pos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play.checkForInput(mouse_pos):
                    character_menu()
                if quit.checkForInput(mouse_pos):
                    pygame.quit()
        pygame.display.update()

def character_menu():
    input_box = pygame.Rect(300, 250, 410, 50)
    color_inactive = pygame.Color('#4f4f4f')
    color_active = pygame.Color('#828282')
    color = color_inactive
    active = False
    text = ''
    warrior_clicked = False
    mage_clicked = False
    archer_clicked = False
    while True:
        screen.fill('black')
        screen.blit(pygame.transform.scale(pygame.image.load(r'assets\sprites\menu_bg.jpg'), (1050,1050)), (0,0))
        mouse_pos = pygame.mouse.get_pos()
        char_menu_text = pygame.font.Font(r"assets\font.ttf", 50).render("Создание персонажа", True, "#b68f40")
        char_menu_rect = char_menu_text.get_rect(center=(510, 100))
        
        char_play = Button(image=None, pos=(510, 550), 
                            text_input="Играть", font=pygame.font.Font(r"assets\font.ttf", 50), base_color="#030303", hovering_color="#4f4f4f")
        button_warrior = Button(image=None, pos=(200, 400), 
                            text_input="Воин", font=pygame.font.Font(r"assets\font.ttf", 50), base_color="#030303", hovering_color="#4f4f4f", clicked=warrior_clicked)
        button_mage = Button(image=None, pos=(500, 400), 
                            text_input="Маг", font=pygame.font.Font(r"assets\font.ttf", 50), base_color="#030303", hovering_color="#4f4f4f", clicked=mage_clicked)
        button_archer = Button(image=None, pos=(800, 400), 
                            text_input="Лучник", font=pygame.font.Font(r"assets\font.ttf", 50), base_color="#030303", hovering_color="#4f4f4f", clicked=archer_clicked,)

        screen.blit(char_menu_text, char_menu_rect)

        for button in [char_play, button_warrior, button_mage, button_archer]:
            button.changeColor(mouse_pos)
            button.update(screen)
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # проверка на коллизию и перевод в активное состояние текстинпута
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive
                if char_play.checkForInput(mouse_pos):
                    game()
                if button_warrior.checkForInput(mouse_pos):
                    create_char('Warrior', text)
                    warrior_clicked = True
                    archer_clicked = False
                    mage_clicked = False
                    button_warrior.changeColor(mouse_pos)
                elif button_mage.checkForInput(mouse_pos):
                    create_char('Mage', text)
                    mage_clicked = True
                    warrior_clicked = False
                    archer_clicked = False
                    button_mage.changeColor(mouse_pos)
                elif button_archer.checkForInput(mouse_pos):
                    create_char('Archer', text)
                    archer_clicked = True
                    warrior_clicked = False
                    mage_clicked = False                  
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif len(text) < 10:
                        text += event.unicode
                
        txt_surface = pygame.font.Font(r"assets\font.ttf", 37).render(text, True, 'white')
        width = max(410, txt_surface.get_width()+10)
        input_box.w = width
        pygame.draw.rect(screen, color, input_box, 0)
        screen.blit(txt_surface, (input_box.x+20, input_box.y+10))
        pygame.display.update()

def pause_menu():
    pause_music()
    while True:
        screen.fill('black')
        screen.blit(pygame.transform.scale(pygame.image.load(r'assets\sprites\menu_bg.jpg'), (1050,1050)), (0,0))
        mouse_pos = pygame.mouse.get_pos()
        menu_text = pygame.font.Font(r"assets\font.ttf", 50).render("Пауза", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(510, 100))
        
        pause_return = Button(image=None, pos=(510, 250), 
                            text_input="Продолжить", font=pygame.font.Font(r"assets\font.ttf", 50), base_color="#030303", hovering_color="#4f4f4f")
        pause_options = Button(image=None, pos=(510, 400), 
                            text_input="Настройки", font=pygame.font.Font(r"assets\font.ttf", 50), base_color="#030303", hovering_color="#4f4f4f")
        pause_quit = Button(image=None, pos=(510, 550), 
                            text_input="Выход", font=pygame.font.Font(r"assets\font.ttf", 50), base_color="#030303", hovering_color="#4f4f4f")

        screen.blit(menu_text, menu_rect)

        for button in [pause_return, pause_options, pause_quit]:
            button.changeColor(mouse_pos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_return.checkForInput(mouse_pos):
                    if is_arena:
                        arena()
                    elif is_forest:
                        forest()
                    else:
                        game()
                if pause_quit.checkForInput(mouse_pos):
                    confirmation_menu()
        pygame.display.update()

def save_menu():
    while True:
        screen.fill('black')
        screen.blit(pygame.transform.scale(pygame.image.load(r'assets\sprites\menu_bg.jpg'), (1050,1050)), (0,0))
        mouse_pos = pygame.mouse.get_pos()
        save_menu_text = pygame.font.Font(r"assets\font.ttf", 25).render("Вы хотите загрузить последнее сохранение?", True, "#b68f40")
        save_menu_rect = save_menu_text.get_rect(center=(510, 100))
        
        save_yes = Button(image=None, pos=(510, 250), 
                            text_input="Да", font=pygame.font.Font(r"assets\font.ttf", 50), base_color="#030303", hovering_color="#4f4f4f")
        save_no = Button(image=None, pos=(510, 400), 
                            text_input="Нет", font=pygame.font.Font(r"assets\font.ttf", 50), base_color="#030303", hovering_color="#4f4f4f")

        screen.blit(save_menu_text, save_menu_rect)

        for button in [save_yes, save_no]:
            button.changeColor(mouse_pos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if save_yes.checkForInput(mouse_pos):
                    load()
                if save_no.checkForInput(mouse_pos):
                    main_menu()

        pygame.display.update()

def confirmation_menu():
    save()
    pause_music()
    while True:
        screen.fill('black')
        screen.blit(pygame.transform.scale(pygame.image.load(r'assets\sprites\menu_bg.jpg'), (1050,1050)), (0,0))
        mouse_pos = pygame.mouse.get_pos()
        conf_menu_text = pygame.font.Font(r"assets\font.ttf", 25).render("Вы уверены что хотите выйти из игры?", True, "#b68f40")
        conf_menu_rect = conf_menu_text.get_rect(center=(510, 100))
        
        confirmation_yes = Button(image=None, pos=(510, 250), 
                            text_input="Да", font=pygame.font.Font(r"assets\font.ttf", 50), base_color="#030303", hovering_color="#4f4f4f")
        confirmation_no = Button(image=None, pos=(510, 400), 
                            text_input="Нет", font=pygame.font.Font(r"assets\font.ttf", 50), base_color="#030303", hovering_color="#4f4f4f")

        screen.blit(conf_menu_text, conf_menu_rect)

        for button in [confirmation_yes, confirmation_no]:
            button.changeColor(mouse_pos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if confirmation_no.checkForInput(mouse_pos):
                    if is_arena:
                        arena()
                    elif is_forest:
                        forest()
                    else:
                        game()
                if confirmation_yes.checkForInput(mouse_pos):
                    pygame.quit()
        pygame.display.update()
        
def menu_shop():
    global is_music_paused
    store.refresh(main_char)
    buttons = []
    item_rects = []
    item_names = []
    item_names_rects = []
    button_x = 150
    button_y = 510
    is_music_paused = False
    play_music(r'assets\music\Shop.ogg')
    # создает списки с кнопками и именами предметов
    for i in range(6):
            buttons.append(Button(image=None, pos=(button_x, button_y), 
                                text_input=str(store.pool[i].price), font=pygame.font.Font(r"assets\font.ttf", 35), base_color="#d7fcd4", hovering_color="White"))
            button_x += 150  
    button_x = 120
    for i in range(len(buttons)):
        item_rects.append(pygame.Rect(button_x, button_y-100, 50, 50))
        button_x += 150
    for i in range(len(buttons)):
        item_names.append(pygame.font.Font(r"assets\font.ttf", 10).render(store.pool[i].name, True, "#d7fcd4"))
    button_x = 150
    for i in item_names:
        item_names_rects.append(i.get_rect(center=(button_x, button_y-150)))
        button_x += 150


    while True:
        
        screen.fill('black')
        mouse_pos = pygame.mouse.get_pos()
        
        # сначала рендерится шрифт, после получается его рект и уже после этот рект заменяется шрифтом
        
        menu_text = pygame.font.Font(r"assets\font.ttf", 50).render("Магазин", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(510, 100))
        money_text = pygame.font.Font(r"assets\font.ttf", 35).render(f"Деньги: {main_char.money}", True, "#ffff00")
        money_rect = money_text.get_rect(center=(510, 210))
        shop_quit = Button(image=None, pos=(510, 700), 
                            text_input="Выход", font=pygame.font.Font(r"assets\font.ttf", 50), base_color="#d7fcd4", hovering_color="white")
        coin_rect = pygame.Rect(740, 185, 50, 50)
        
        
        screen.blit(pygame.transform.scale(pygame.image.load(r"assets\sprites\items\coin.png"), (50,50)), coin_rect)
        screen.blit(menu_text, menu_rect)
        screen.blit(money_text, money_rect)
        
        for i in range(len(item_names)):
            screen.blit(item_names[i], item_names_rects[i])
            
        shop_quit.changeColor(mouse_pos)
        shop_quit.update(screen)
        
        for button in buttons:
            button.update(screen)
            button.changeColor(mouse_pos)
            
        for i in range(len(item_rects)):
            screen.blit(store.pool[i].sprite, item_rects[i])

            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(buttons)):
                    # пробегаем циклом все кнопки и проверяем нажатие   
                    if buttons[i].checkForInput(mouse_pos):
                        buy_menu(i)
                if shop_quit.checkForInput(mouse_pos):
                    game()

        pygame.display.update()

    
def buy_menu(index):
    while True:
        screen.fill('black')
        mouse_pos = pygame.mouse.get_pos()
        menu_text = pygame.font.Font(r"assets\font.ttf", 50).render("Покупка", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(510, 100))
        money_text = pygame.font.Font(r"assets\font.ttf", 35).render(f"Деньги: {main_char.money}", True, "#ffff00")
        money_rect = money_text.get_rect(center=(510, 210))
        item_rect = pygame.Rect(410, 250, 200, 200)
        coin_rect = pygame.Rect(740, 185, 50, 50)
        
        screen.blit(pygame.transform.scale(pygame.image.load(r"assets\sprites\items\coin.png"), (50,50)), coin_rect)
        screen.blit(pygame.transform.scale(store.pool[index].sprite, (200, 300)), item_rect)
        x = 510
        y = 600
        # передают в функцию для форматирования текст, она его делит и он выводится
        
        for i in text_formation(store.pool[index].print_stats()):
            y += 100
            item_text = pygame.font.Font(r"assets\font.ttf", 30).render(i, True, "#b68f40")
            item_rect = item_text.get_rect(center=(x,y))
            screen.blit(item_text, item_rect)

        buy_button = Button(image=None, pos=(310, 600), 
                    text_input="Купить", font=pygame.font.Font(r"assets\font.ttf", 50), base_color="#d7fcd4", hovering_color="white")
        
        buy_quit = Button(image=None, pos=(710, 600), 
                            text_input="Назад", font=pygame.font.Font(r"assets\font.ttf", 50), base_color="#d7fcd4", hovering_color="white")
        
        screen.blit(menu_text, menu_rect)
        screen.blit(money_text, money_rect)
        for button in [buy_button, buy_quit]:
            button.changeColor(mouse_pos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buy_button.checkForInput(mouse_pos):
                    buy(store.pool[index].name)
                if buy_quit.checkForInput(mouse_pos):
                    menu_shop()
        pygame.display.update()


def menu_arena():
    pause_music()
    while True:
        screen.fill('black')
        screen.blit(pygame.transform.scale(pygame.image.load(r'assets\sprites\menu_bg.jpg'), (1050,1050)), (0,0))
        mouse_pos = pygame.mouse.get_pos()
        conf_menu_text = pygame.font.Font(r"assets\font.ttf", 25).render("Вы хотите пойти на арену?", True, "#b68f40")
        conf_menu_rect = conf_menu_text.get_rect(center=(510, 100))
        
        arena_yes = Button(image=None, pos=(510, 250), 
                            text_input="Да", font=pygame.font.Font(r"assets\font.ttf", 50), base_color="#030303", hovering_color="#4f4f4f")
        arena_no = Button(image=None, pos=(510, 400), 
                            text_input="Нет", font=pygame.font.Font(r"assets\font.ttf", 50), base_color="#030303", hovering_color="#4f4f4f")

        screen.blit(conf_menu_text, conf_menu_rect)

        for button in [arena_yes, arena_no]:
            button.changeColor(mouse_pos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if arena_yes.checkForInput(mouse_pos):
                    is_music_paused = False
                    arena()
                if arena_no.checkForInput(mouse_pos):
                    game()
        pygame.display.update()
        
def menu_forest():
    pause_music()
    global is_forest
    while True:
        screen.fill('black')
        screen.blit(pygame.transform.scale(pygame.image.load(r'assets\sprites\menu_bg.jpg'), (1050,1050)), (0,0))
        mouse_pos = pygame.mouse.get_pos()
        forest_menu_text = pygame.font.Font(r"assets\font.ttf", 25).render("Вы хотите пойти в лес?", True, "#b68f40")
        forest_menu_rect = forest_menu_text.get_rect(center=(510, 100))
        
        forest_yes = Button(image=None, pos=(510, 250), 
                            text_input="Да", font=pygame.font.Font(r"assets\font.ttf", 50), base_color="#030303", hovering_color="#4f4f4f")
        forest_no = Button(image=None, pos=(510, 400), 
                            text_input="Нет", font=pygame.font.Font(r"assets\font.ttf", 50), base_color="#030303", hovering_color="#4f4f4f")

        screen.blit(forest_menu_text, forest_menu_rect)

        for button in [forest_no, forest_yes]:
            button.changeColor(mouse_pos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if forest_yes.checkForInput(mouse_pos):
                    is_forest = True
                    forest()
                if forest_no.checkForInput(mouse_pos):
                    game()
        pygame.display.update()
        
def inventory():
    inventory_rect = pygame.Rect(250, 100, 500, 500)
    items_rects = []
    equipment_rects = []
    inv_buttons = []
    is_using = False
    items_x = 300
    items_y = 300
    equipment_y = 230
    for i in range(9):
        items_rects.append(pygame.Rect(items_x, items_y, 50, 50))
        items_x += 70
        if len(items_rects) == 5:
            items_x = 300
            items_y = 400
            items_rects.append(pygame.Rect(items_x, items_y, 50, 50))
            items_x += 70
    for i in range(5):
        equipment_rects.append(pygame.Rect(670, equipment_y, 50, 50))
        equipment_y += 70
    confirm_buttons = [Button(image=None, pos=(425, 325), 
                                            text_input='Да', font=pygame.font.Font(r"assets\font.ttf", 25), base_color="#d7fcd4", hovering_color="White"),
                        Button(image=None, pos=(575, 325), 
                                            text_input='Нет', font=pygame.font.Font(r"assets\font.ttf", 25), base_color="#d7fcd4", hovering_color="White")]    
    while True:
        movement()
        mouse_pos = pygame.mouse.get_pos()
        if not is_using:
            pygame.draw.rect(screen, 'black', inventory_rect)
        inventory_text = pygame.font.Font(r"assets\font.ttf", 25).render("Инвентарь", True, "#d7fcd4")
        inventory_text_rect = inventory_text.get_rect(center=(510, 150))
        confirm_text = pygame.font.Font(r'assets\font.ttf', 10).render('Использовать этот предмет?', True, '#d7fcd4')
        confirm_text_rect = confirm_text.get_rect(center=(500,275))
        for i in range(len(main_char.inventory)):
            inv_buttons.append(Button(image=pygame.transform.scale(main_char.inventory[i].sprite, (35,35)), pos=(items_rects[i].x+25, items_rects[i].y+25), 
                                 text_input=None, font=pygame.font.Font(r"assets\font.ttf", 35), base_color="#d7fcd4", hovering_color="White"))
        equipment_buttons = {
            
                'Helmet': Button(image=pygame.transform.scale(main_char.equipment['Helmet'].sprite if main_char.equipment['Helmet'] else pygame.transform.scale(pygame.image.load(r'assets\sprites\items\sword.png'), (1,1)), (35,35)), pos=(equipment_rects[0].x+25, equipment_rects[0].y+25), 
                                            text_input=None, font=pygame.font.Font(r"assets\font.ttf", 35), base_color="#d7fcd4", hovering_color="White"),
                'Chestplate': Button(image=pygame.transform.scale(main_char.equipment['Chestplate'].sprite if main_char.equipment['Chestplate'] else pygame.transform.scale(pygame.image.load(r'assets\sprites\items\sword.png'), (1,1)), (35,35)), pos=(equipment_rects[1].x+25, equipment_rects[1].y+25), 
                                            text_input=None, font=pygame.font.Font(r"assets\font.ttf", 35), base_color="#d7fcd4", hovering_color="White") ,
                'Leggins': Button(image=pygame.transform.scale(main_char.equipment['Leggins'].sprite if main_char.equipment['Leggins'] else pygame.transform.scale(pygame.image.load(r'assets\sprites\items\sword.png'), (1,1)), (35,35)), pos=(equipment_rects[2].x+25, equipment_rects[2].y+25), 
                                            text_input=None, font=pygame.font.Font(r"assets\font.ttf", 35), base_color="#d7fcd4", hovering_color="White"),
                'Left_hand' : Button(image=pygame.transform.scale(main_char.equipment['Left_hand'].sprite if main_char.equipment['Left_hand'] else pygame.transform.scale(pygame.image.load(r'assets\sprites\items\sword.png'), (1,1)), (35,35)), pos=(equipment_rects[3].x+25, equipment_rects[3].y+25), 
                                            text_input=None, font=pygame.font.Font(r"assets\font.ttf", 35), base_color="#d7fcd4", hovering_color="White"),
                'Right_hand': Button(image=pygame.transform.scale(main_char.equipment['Right_hand'].sprite if main_char.equipment['Right_hand'] else pygame.transform.scale(pygame.image.load(r'assets\sprites\items\sword.png'), (1,1)), (35,35)), pos=(equipment_rects[4].x+25, equipment_rects[4].y+25), 
                                            text_input=None, font=pygame.font.Font(r"assets\font.ttf", 35), base_color="#d7fcd4", hovering_color="White")
            }    
        if not is_using:
            screen.blit(inventory_text, inventory_text_rect)
            for i in items_rects:
                pygame.draw.rect(screen, 'grey', i)
        
            for i in equipment_rects:
                pygame.draw.rect(screen, 'grey', i)    
        
            for button in inv_buttons:
                button.changeColor(mouse_pos)
                button.update(screen)
        
            for button in equipment_buttons.values():
                button.changeColor(mouse_pos)
                button.update(screen)
        
        if is_using:
            for button in confirm_buttons:
                button.update(screen)
                button.changeColor(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                event_cycle = False
                for i in range(len(inv_buttons)):
                    if inv_buttons[i].checkForInput(mouse_pos):
                        if main_char.equip(main_char.inventory[i]):
                            event_cycle = True
                            break
                        elif not hasattr(main_char.inventory[i], 'equip'):
                            is_using = True
                            pygame.draw.rect(screen, 'grey', (350,225,300,150))
                            screen.blit(confirm_text, confirm_text_rect)
                    if confirm_buttons[0].checkForInput(mouse_pos):
                        main_char.use(main_char, main_char.inventory[i])
                        is_using = False
                        break
                    elif confirm_buttons[1].checkForInput(mouse_pos):
                        is_using = False
                        break       
                    
                if event_cycle:
                    break

                for key in main_char.equipment.keys():
                    if main_char.equipment[key]:
                        if equipment_buttons[key].checkForInput(mouse_pos):
                            main_char.unequip(main_char.equipment[key])
                            break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_b]:
            break
        
        pygame.display.update()
        inv_buttons.clear()
        equipment_buttons.clear()

def movement():
    global char_walk
    global tick
    global inventory_state
    keys = pygame.key.get_pressed()
    char_walk = False
    vx = 0
    vy = 0
    speed = 7
    if keys[pygame.K_w]:
        if char_rect.draw_object.y > 50:
            char_walk = True
            vy = -speed 
    if keys[pygame.K_s]:
        if char_rect.draw_object.y < 890:
            char_walk = True
            vy = speed
    if keys[pygame.K_a]:
        if char_rect.draw_object.x > 50:
            char_walk = True
            vx = -speed
    if keys[pygame.K_d]:
        if char_rect.draw_object.x < 890:
            char_walk = True
            vx = speed
    if keys[pygame.K_w] and keys[pygame.K_s]:
        char_walk = False
        vy = 0
    if keys[pygame.K_a] and keys[pygame.K_d]:
        char_walk = False
        vx = 0
    if vx and vy: # если одновременно два вектора больше нуля - делим на корень из двух
        vx = vx / math.sqrt(2)
        vy = vy / math.sqrt(2)
    char_rect.draw_object.x += vx
    char_rect.draw_object.y += vy
    if keys[pygame.K_ESCAPE]:
        pause_menu()
    tick += clock.tick(60)            
    if tick >= inventory_delay:
        if keys[pygame.K_b]:
            tick = 0
            if inventory_state:
                inventory_state = False            
            else:
                inventory_state = True

def trees_collision():
    trees_collision = char_rect.draw_object.collideobjects(trees, key=lambda o: o.collision_box)
    keys = pygame.key.get_pressed()
    if trees_collision:
        if keys[pygame.K_w]:
                char_rect.draw_object.y += 7
        if keys[pygame.K_s]:
                char_rect.draw_object.y -= 7
        if keys[pygame.K_a]:
                char_rect.draw_object.x += 7 
        if keys[pygame.K_d]:
                char_rect.draw_object.x -= 7

def main_game_collision():
    collision = char_rect.draw_object.collideobjects(objects, key=lambda o: o.draw_object)
    keys = pygame.key.get_pressed()
    if collision:
        if keys[pygame.K_w]:
                char_rect.draw_object.y += 7
        if keys[pygame.K_s]:
                char_rect.draw_object.y -= 7
        if keys[pygame.K_a]:
                char_rect.draw_object.x += 7
        if keys[pygame.K_d]:
                char_rect.draw_object.x -= 7    

def func_collision():
    collision = char_rect.draw_object.collideobjects(objects, key=lambda o: o.collision_box)
    keys = pygame.key.get_pressed()
    if collision:
        if collision.name == 'shop_rect':
            if keys[pygame.K_w]:
                    char_rect.draw_object.y += 7
            if keys[pygame.K_s]:
                    char_rect.draw_object.y -= 7
            if keys[pygame.K_a]:
                    char_rect.draw_object.x += 7
            if keys[pygame.K_d]:
                    char_rect.draw_object.x -= 7    
            menu_shop()
        if collision.name == 'arena_rect':
            if keys[pygame.K_w]:
                    char_rect.draw_object.y += 7
            if keys[pygame.K_s]:
                    char_rect.draw_object.y -= 7
            if keys[pygame.K_a]:
                    char_rect.draw_object.x += 7
            if keys[pygame.K_d]:
                    char_rect.draw_object.x -= 7 
            menu_arena()
        if collision.name == 'forest_rect':
            if keys[pygame.K_w]:
                    char_rect.draw_object.y += 7
            if keys[pygame.K_s]:
                    char_rect.draw_object.y -= 7
            if keys[pygame.K_a]:
                    char_rect.draw_object.x += 7
            if keys[pygame.K_d]:
                    char_rect.draw_object.x -= 7 
            menu_forest()
        if collision.name == 'sword_rect':
            main_char.add_to_inventory(Sword('', 100, 10, pygame.transform.scale(pygame.image.load(r"assets\sprites\items\sword.png"), (50,50))))

def draw_objects():
    global objects
    global screen
    global frame
    global is_forest
    if is_forest:
        if char_walk:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                    screen.blit(pygame.transform.scale(Render_char.walk_up[frame], (60,60)), char_rect.draw_object)
            elif keys[pygame.K_s]:
                    screen.blit(pygame.transform.scale(Render_char.walk_down[frame], (60,60)), char_rect.draw_object)
            elif keys[pygame.K_a]:
                    screen.blit(pygame.transform.scale(Render_char.walk_left[frame], (60,60)), char_rect.draw_object)
            elif keys[pygame.K_d]:
                    screen.blit(pygame.transform.scale(Render_char.walk_right[frame], (60,60)), char_rect.draw_object)
        elif not char_walk:
            screen.blit(pygame.transform.scale(Render_char.idle, (60,60)), char_rect.draw_object)
        for i in trees:
            i.draw(screen) 
    else:
        for i in objects:
            i.draw(screen)  
        if char_walk:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                    screen.blit(pygame.transform.scale(Render_char.walk_up[frame], (60,60)), char_rect.draw_object)
            elif keys[pygame.K_s]:
                    screen.blit(pygame.transform.scale(Render_char.walk_down[frame], (60,60)), char_rect.draw_object)
            elif keys[pygame.K_a]:
                    screen.blit(pygame.transform.scale(Render_char.walk_left[frame], (60,60)), char_rect.draw_object)
            elif keys[pygame.K_d]:
                    screen.blit(pygame.transform.scale(Render_char.walk_right[frame], (60,60)), char_rect.draw_object)
        elif not char_walk:
            screen.blit(pygame.transform.scale(Render_char.idle, (60,60)), char_rect.draw_object)
            
def generate_trees():
    global trees
    trees = []
    while len(trees) != 9:
        rect = pygame.Rect(random.randint(20, 1000), random.randint(20, 1000), 60, 60)
        # перегенерация при наличии колизии с другими обьектами
        while rect.collideobjects(trees, key=lambda o: o.draw_object) or rect.colliderect(char_rect.draw_object) or rect.collideobjects(monsters_rects, key=lambda o : o.draw_object): 
            rect = pygame.Rect(random.randint(20, 1000), random.randint(20, 1000), 60, 60)
        trees.append(Render_object('', 'black', pygame.transform.scale(pygame.image.load(r'assets\sprites\tree.png'), (120,120)), rect, rect))
    
def fight(enemy, sprite, bg=None):
    is_fight = True
    fight_buttons = [Button(image=None, pos=(150, 950), 
                                            text_input='Атаковать', font=pygame.font.Font(r"assets\font.ttf", 12), base_color="#d7fcd4", hovering_color="White"),
                     Button(image=None, pos=(350, 950), 
                                            text_input='Защищаться', font=pygame.font.Font(r"assets\font.ttf", 12), base_color="#d7fcd4", hovering_color="White"),
                     Button(image=None, pos=(550, 950), 
                                            text_input="Открыть инвентарь", font=pygame.font.Font(r"assets\font.ttf", 12), base_color="#d7fcd4", hovering_color="White"),
                     Button(image=None, pos=(750,950), 
                                            text_input="Отдых", font=pygame.font.Font(r"assets\font.ttf", 12), base_color="#d7fcd4", hovering_color="White"),
                     Button(image=None, pos=(950,950), 
                                            text_input="Сдаться", font=pygame.font.Font(r"assets\font.ttf", 12), base_color="#d7fcd4", hovering_color="White"),
    ]

    main_char_turn = True
    last_action = None
    while main_char.health > 0 and enemy.health > 0 and is_fight:
        last_action_text = pygame.font.Font(r"assets\font.ttf", 15).render(last_action if last_action else '', True, "#d7fcd4")
        last_action_rect = last_action_text.get_rect(center=(510, 900))
        
        mouse_pos = pygame.mouse.get_pos()
        characters_health = [Button(image=None, pos=(200, 850), 
                                        text_input=f'Здоровье {main_char.name}: {main_char.health}', font=pygame.font.Font(r"assets\font.ttf", 15), base_color="#d7fcd4", hovering_color="d7fcd4"),
                    Button(image=None, pos=(800,850), 
                                        text_input=f'Здоровье {enemy.name}: {enemy.health}', font=pygame.font.Font(r"assets\font.ttf", 15), base_color="#d7fcd4", hovering_color="d7fcd4")
                    ]
        
        screen.fill('white')
        if bg:
            screen.blit(pygame.transform.scale(bg, (1020,1020)), (0,-200))
        pygame.draw.rect(screen, 'black', (0, 800, 1050, 1050))
        screen.blit(sprite, (800, 300))
        screen.blit(pygame.transform.scale(char_rect.idle, (100,100)), (200, 300))
        if main_char_turn:
            for button in fight_buttons:
                button.update(screen)
                button.changeColor(mouse_pos)
        for button in characters_health:
            button.update(screen)
        screen.blit(last_action_text, last_action_rect) # вывод последнего действия
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                is_fight = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(fight_buttons)):
                    if fight_buttons[i].checkForInput(mouse_pos):
                        if i == 0:
                            last_action = main_char.attack(enemy)
                            main_char_turn = False
                            enemy_action = random.randint(1,3)
                            if enemy_action == 1:
                                last_action = enemy.attack(main_char)
                            elif enemy_action == 2:
                                last_action = enemy.defend()
                            elif enemy_action == 3:
                                last_action = enemy.rest()
                            main_char_turn = True
                        elif i == 1:
                            last_action = main_char.defend()
                            main_char_turn = False
                            enemy_action = random.randint(1,3)
                            if enemy_action == 1:
                                last_action = enemy.attack(main_char)
                            elif enemy_action == 2:
                                last_action = enemy.defend()
                            elif enemy_action == 3:
                                last_action = enemy.rest()
                            main_char_turn = True
                        elif i == 2:
                            inventory()
                        elif i == 3:
                            last_action = main_char.rest()
                            main_char_turn = False
                            enemy_action = random.randint(1,3)
                            if enemy_action == 1:
                                last_action = enemy.attack(main_char)
                            elif enemy_action == 2:
                                last_action = enemy.defend()
                            elif enemy_action == 3:
                                last_action = enemy.rest()
                            main_char_turn = True
                        elif i == 4:     
                            confirmation_menu()
        if enemy.health <= 0 < main_char.health:
            main_char.gain_exp()
        elif main_char.health <= 0 < enemy.health:
            enemy.gain_exp()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pause_menu()
        clock.tick(30)
        pygame.display.flip()
            
def arena():
    global is_arena
    global is_music_paused
    names = ['Liam', 'Alex', 'Nathan', 'John', 'Andrew']
    is_arena = True
    is_music_paused = False
    play_music(r'assets\music\Fight.ogg')
    enemy_class = random.randint(1,3)
    if enemy_class == 1:
        enemy = Archer(random.choice(names))
    if enemy_class == 2:
        enemy = Warrior(random.choice(names))
    if enemy_class == 3:
        enemy = Mage(random.choice(names))
    fight(enemy, pygame.transform.scale(pygame.image.load(r'assets\sprites\anims\main_char\idle_main.png'), (100,100)), bg=pygame.image.load(r'assets\sprites\arena.jpg'))

def forest():
    global is_forest
    global tick
    global frame
    global is_music_paused
    global monsters_rects
    is_forest = True
    is_music_paused = False
    char_rect.draw_object.x = 50
    char_rect.draw_object.y = 50
    tick = 0
    delay = 50
    frame = 0
    monsters = [Monster('monster', 120, 10, 10, 5) for i in range(3)]
    monsters_rects = [Render_object('', 'black', monster_idle_sprite[1], pygame.Rect(random.randint(20, 950), random.randint(20, 950), 50,50)) for i in range(3)]
    generate_trees()
    play_music(r'assets\music\Mystical.ogg')
    while is_forest:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                is_forest = False
        screen.fill('green')
        draw_objects()
        movement()
        trees_collision()
        if char_walk: 
            tick += clock.tick(60)
            if tick >= delay:
                tick = 0
                frame = (frame + 1) % len(Render_char.walk_up)
        forest_exit_rect.draw(screen)
        for i in monsters_rects:
            screen.blit(pygame.transform.scale(i.sprite, (150, 150)), i.draw_object)
        collision = char_rect.draw_object.collideobjects(monsters_rects, key=lambda o : o.draw_object)
        if collision:
            fight(monsters[monsters_rects.index(collision)], pygame.transform.scale(pygame.image.load(r"assets\sprites\anims\orc_warrior\front1.png"), (150, 150)), bg=pygame.image.load(r'assets\sprites\arena.jpg'))
        keys = pygame.key.get_pressed()
        if char_rect.draw_object.colliderect(forest_exit_rect.draw_object):
            if keys[pygame.K_w]:
                    char_rect.draw_object.y += 5
            if keys[pygame.K_s]:
                    char_rect.draw_object.y -= 5
            if keys[pygame.K_a]:
                    char_rect.draw_object.x += 5
            if keys[pygame.K_d]:
                    char_rect.draw_object.x -= 5 
            char_rect.draw_object.x = 700
            char_rect.draw_object.y = 110
            game()   
        pygame.display.flip()
        
def game():
    global tick
    global frame
    is_forest = False
    running = True
    delay = 50
    play_music(r'assets\music\Village.ogg')
    while running:   
        if is_arena:
            arena()
        elif is_forest:
            forest()
        else:
            if inventory_state:
                inventory()  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save()
                    running = False
            screen.blit(pygame.image.load(r'assets\sprites\bg2.png'), (0,0)) 
            draw_objects()
            if char_walk: # счет тиков, как только тик становится больше задержки, меняем кадр анимации
                tick += clock.tick(60)
                if tick >= delay:
                    tick = 0
                    frame = (frame + 1) % len(Render_char.walk_up)
            movement()
            main_game_collision()
            func_collision()
            pygame.display.flip()
        
is_arena = False
is_forest = False
is_music_paused = False
inventory_state = False
main_char = None
store = Store(6)
clock = pygame.time.Clock()
char_walk = False
frame = 0
delay = 50
inventory_delay = 500
tick = 0 
trees = []

monster_idle_sprite = [pygame.image.load(r'assets\sprites\anims\orc_warrior\front1.png'),
                    pygame.image.load(r'assets\sprites\anims\orc_warrior\front2.png'),
                    pygame.image.load(r'assets\sprites\anims\orc_warrior\front3.png'),
                    pygame.image.load(r'assets\sprites\anims\orc_warrior\front4.png')]

unit_idle = [pygame.image.load(r'assets\sprites\anims\ninja\front1.png'),
            pygame.image.load(r'assets\sprites\anims\ninja\front2.png'),
            pygame.image.load(r'assets\sprites\anims\ninja\front3.png'),
            pygame.image.load(r'assets\sprites\anims\ninja\front4.png')]


char_rect =  Render_char('main char', 'white', pygame.Rect(60, 60, 60, 60), pygame.Rect(60,60,60,60))
forest_exit_rect = Render_object("forest_rect", 'yellow',  pygame.transform.scale(pygame.image.load(r'assets\sprites\tree.png'), (120,120)), pygame.Rect(50, 500, 60, 80), pygame.Rect(50, 500, 60, 80))

objects = [
    Render_object("shop_rect", 'green', pygame.transform.scale(pygame.image.load(r'assets\sprites\shop_sprite.png') , (200, 250)), pygame.Rect(350, 300, 200, 220), pygame.Rect(415, 540, 70, 20)),
    Render_object('tree1', 'white', pygame.transform.scale(pygame.image.load(r'assets\sprites\tree.png'), (120,120)), pygame.Rect(50, 300, 60, 60), pygame.Rect(50, 300, 60, 60)),
    Render_object('tree2', 'white', pygame.transform.scale(pygame.image.load(r'assets\sprites\tree.png'), (120,120)), pygame.Rect(50, 450, 60, 60), pygame.Rect(50, 450, 60, 60)),
    Render_object('tree3', 'white', pygame.transform.scale(pygame.image.load(r'assets\sprites\tree.png'), (120,120)), pygame.Rect(50, 600, 60, 60), pygame.Rect(50, 600, 60, 60)),
    Render_object("arena_rect", 'red', pygame.transform.scale(pygame.image.load(r'assets\sprites\tree.png'), (120,120)), pygame.Rect(650, 650, 60, 60), pygame.Rect(645, 630, 100, 100)),
    Render_object("forest_rect", 'yellow', pygame.transform.scale(pygame.image.load(r'assets\sprites\tree.png'), (120,120)), pygame.Rect(800, 150, 60, 60), pygame.Rect(780, 130, 100, 100)),
    Render_object("sword_rect", 'white', pygame.transform.scale(pygame.image.load(r'assets\sprites\tree.png'), (120,120)), pygame.Rect(700, 150, 60, 60), pygame.Rect(680, 130, 100, 100))
]

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    display()
    # проверка на наличие сейва 
    if os.path.exists("save.json") and os.path.getsize("save.json") >= 1:
        save_menu()
    else:
        main_menu() 