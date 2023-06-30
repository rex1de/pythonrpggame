import pygame
class Render_object:
    def __init__(self, name, color, sprite, draw_object, collision_box=None):
        self.name = name
        self.color = color
        self.sprite = sprite
        self.draw_object = draw_object
        if collision_box:
            self.collision_box = collision_box
        else:
            self.collision_box = draw_object.copy() # если collision box не задан, он копирует значение draw object
            
    def draw(self, screen): # рисовка спрайта
        screen.blit(self.sprite, self.draw_object)
            
class Render_animated_object(Render_object):
    def __init__(self, name, color, sprite, draw_object, collision_box=None):
         super().__init__(name, color, sprite, draw_object, collision_box)

    def draw(self, screen, frame):
        screen.blit(self.sprite[frame], self.draw_object)
    

class Render_char(Render_object):
    walk_up = [pygame.image.load(r'assets\sprites\anims\main_char\up1.png'),
               pygame.image.load(r'assets\sprites\anims\main_char\up2.png'),
               pygame.image.load(r'assets\sprites\anims\main_char\up3.png'),
               pygame.image.load(r'assets\sprites\anims\main_char\up4.png')]
    
    walk_down = [pygame.image.load(r'assets\sprites\anims\main_char\down1.png'),
               pygame.image.load(r'assets\sprites\anims\main_char\down2.png'),
               pygame.image.load(r'assets\sprites\anims\main_char\down3.png'),
               pygame.image.load(r'assets\sprites\anims\main_char\down4.png')]
    
    walk_left = [pygame.image.load(r'assets\sprites\anims\main_char\left1.png'),
               pygame.image.load(r'assets\sprites\anims\main_char\left2.png'),
               pygame.image.load(r'assets\sprites\anims\main_char\left3.png'),
               pygame.image.load(r'assets\sprites\anims\main_char\left4.png')]
    
    walk_right = [pygame.image.load(r'assets\sprites\anims\main_char\right1.png'),
               pygame.image.load(r'assets\sprites\anims\main_char\right2.png'),
               pygame.image.load(r'assets\sprites\anims\main_char\right3.png'),
               pygame.image.load(r'assets\sprites\anims\main_char\right4.png')]
    
    idle = pygame.image.load(r'assets\sprites\anims\main_char\idle_main.png')
    
    def __init__(self, name, color, draw_object, collision_box):
        super().__init__(name, color, draw_object, collision_box)
        self.char_walk = False
        self.frame = 0
        
