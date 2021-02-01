import pygame
from objects import *
from random import randrange



class Alien():
    size_x, size_y = (48, 32)
    movement = None
    @staticmethod
    def generator(game):
        margin_width = int(game.setings['alien']['margin_width'])
        margin_height = int(game.setings['alien']['margin_height'])
        if game.setings['alien']['column'] == 'd':
            column = (game.width - margin_width) // 50
        else : column = int(game.setings['alien']['column'])
        row = int(game.setings['alien']['row'])
        width_x = int(game.setings['alien']['width_x'])
        width_y = int(game.setings['alien']['width_y'])
        image_id = eval(game.setings['alien']['alien_column_config'])
        for x in range(0, column):
            for y in range(0, row):
                game.aliens.append(Alien(game, 
                margin_width + x*(Alien.size_x + width_x), 
                margin_height + y*(Alien.size_y + width_y), 
                image_id[str(y)]
                ))


    def __init__(self, game, x, y, image_id):
        self.x = x
        self.game = game
        self.y = y
        self.image_id = image_id
        self.image_number = 1

    def draw(self):
        self.game.screen.blit(getattr(self.game.assets, self.image_id['path'+ str(self.image_number)]), (self.x, self.y))
        # pygame.draw.rect(self.game.screen,  
        #                  (81, 43, 88),  
        #                  pygame.Rect(self.x, self.y, Alien.size, Alien.size))

        if Alien.movement == None : Alien.movement = int(self.game.setings['alien']['movement'])
        if self.x >= self.game.width-50 : Alien.movement = -int(self.game.setings['alien']['movement'])
        elif self.x <= 20 : Alien.movement = int(self.game.setings['alien']['movement'])
        if self.game.frame_count == 30 or self.game.frame_count == 59:
            self.y += 1
            self.x += Alien.movement
            if self.image_number == 1:
                self.image_number = 2
            else:
                self.image_number = 1



    def checkCollision(self, game):
        for rocket in game.player_rockets:
            if (rocket.x < self.x + Alien.size_x+2 and rocket.x > self.x-2 and
                    rocket.y > self.y and rocket.y < self.y + Alien.size_y):
                game.player_rockets.remove(rocket)
                game.aliens.remove(self)


class Player():
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y
        self.Health = 3
        self.image = game.assets.Ship
        self.size_x, self.size_y = self.image.get_size()


    def display_health(self):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 15)
        textsurface = font.render(str(self.Health), False, (150, 0, 62))
        self.game.screen.blit(textsurface, (self.game.width-(self.game.width-10), self.game.height-(self.game.height-10)))

    def draw(self):
        self.display_health()
        self.game.screen.blit(self.image, (self.x, self.y)) 
  

    def checkCollision(self, game):
        for rocket in game.alien_rockets:
            if (rocket.x < self.x + (self.size_x+2) and rocket.x > self.x-2 and
                    rocket.y > self.y and rocket.y < self.y + self.size_y):
                if (rocket.x > self.x + (self.size_x-20) // 2 and self.Health == 3):
                        self.image = game.assets.Ship_CR
                elif self.Health == 3 : self.image = game.assets.Ship_CL
                else : self.image = game.assets.Ship_CC
                game.alien_rockets.remove(rocket)
                self.Health -= 1
                if self.Health <= 0:
                    self.game.lost = True

    def move_right(self):
        """
        move palyer to right
        """
        self.x += int(self.game.setings['player 1']['speed']) if self.x < self.game.width - int(self.game.setings['player 1']['margin']) else 0

    def move_left(self):
        """
        move palyer to left
        """
        self.x -= int(self.game.setings['player 1']['speed']) if self.x > int(self.game.setings['player 1']['margin']) else 0

    def shoot_rocket(self):
        """
        player shoot Rocket
        """
        self.game.player_rockets.append(
            Rocket(self.game, self.x + (self.size_x//2)-0.5, self.y, -2, self.game.assets.bullet_red))


class Castle():
    size = 10
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y
        self.Health = 3
        


    @staticmethod
    def generator(game):
        start_x = int(game.setings['castle']['start_x'])
        start_y = int(game.setings['castle']['start_y'])
        castle_location = eval(game.setings['castle']['castle_location'])
        for x in range(start_x, game.width, start_x+(5*Castle.size)):
            Castle._castle_generator(game, castle_location, x, start_y)
        
        

    def _castle_generator(game, castle_location, start_x, start_y):
        column, Row = int(game.setings['castle']['column']) , int(game.setings['castle']['row'])
        for i in range(0,Row):
            for j in range(0,column):
                if castle_location[i][j] == 1:
                    game.castles += [Castle(game, start_x + j*(Castle.size), start_y + i*(Castle.size))]
    
    def checkCollision(self, game):
        
        for rocket in game.alien_rockets:
            if (rocket.x < self.x + (self.size+2) and rocket.x > self.x-2 and
                    rocket.y > self.y and rocket.y < self.y + self.size):
                game.alien_rockets.remove(rocket)
                self.Health -=1
                if self in game.castles and self.Health <= 0 :
                    game.castles.remove(self)

        for rocket in game.player_rockets:
            if (rocket.x < self.x + (self.size+2) and rocket.x > self.x-2 and
                    rocket.y > self.y and rocket.y < self.y + self.size):
                game.player_rockets.remove(rocket)
                self.Health -=1
                if self in game.castles and self.Health <= 0 :
                    game.castles.remove(self)
                

    def draw(self):
                pygame.draw.rect(self.game.screen,
                         eval(self.game.setings['castle']['block_l' + str(self.Health)]),
                         pygame.Rect(self.x, self.y, self.size, self.size))


class Rocket():
        def __init__(self, game, x, y, move, image):
            self.x = x
            self.y = y
            self.game = game
            self.move = move
            self.image = image

        def draw(self):
            # pygame.draw.rect(self.game.screen,
            #                  (254, 52, 110),
            #                  pygame.Rect(self.x, self.y, 2, 4))
            self.game.screen.blit(self.image, (self.x, self.y))
            self.y += self.move