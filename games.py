import pygame
from objects import *

class base_game ():
    screen = None
    aliens = []
    castles = []
    alien_rockets = []
    player_rockets = []
    lost = False
    def start_game():
        pass
    


class Game (base_game):
    def __init__(self, setings, assets, width, height):
        pygame.init()
        Game.setings = setings
        Game.assets = assets
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Space Invaders')
        pygame.display.set_icon(Game.assets.icon)
        self.clock = pygame.time.Clock()
        self.done = False
        self.SHOOT = pygame.USEREVENT+1
        pygame.time.set_timer(self.SHOOT, 250)
        self.frame_count = 0

        self.player = Player(self, width / 2, height - 20)
        Alien.generator(self)
        Castle.generator(self)
        self.rocket = None
        
    def start_game(self):
        while not self.done:
            self.frame_count += 1
            if self.frame_count == 60 : self.frame_count = 0
            if len(self.aliens) == 0:
                self.displayText("VICTORY ACHIEVED")

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                self.player.move_left()
            elif pressed[pygame.K_RIGHT]:
                self.player.move_right()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.lost:
                    self.player.shoot_rocket()
                if event.type == self.SHOOT:
                    if len(self.aliens) > 0:
                        a = self.aliens[randrange(len(self.aliens))]
                        self.alien_rockets.append(
                            Rocket(self, a.x+(a.size_x/2), a.y, 2, Game.assets.bullet))
                        del a

            pygame.display.flip()
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))
            self.screen.blit(Game.assets.background, (0, 0))

            for alien in self.aliens:
                alien.draw()
                alien.checkCollision(self)
                if (alien.y > self.height):
                    self.lost = True
                    self.displayText("YOU DIED")

            for castle in self.castles:
                castle.draw()
                castle.checkCollision(self)

            for rocket in self.alien_rockets + self.player_rockets:
                rocket.draw()

            if not self.lost:
                self.player.draw()
                self.player.checkCollision(self)
            else:
                self.displayText("YOU DIED")

    def displayText(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        textsurface = font.render(text, False, (255, 0, 95))#ff005f
        self.screen.blit(textsurface, (110, 160))