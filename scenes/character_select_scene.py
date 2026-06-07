import math

import pygame
from scene import Scene
from collections import deque
import resources


class CharacterSelectScene(Scene):
    def __init__(self, manager, game):
        self.manager = manager
        self.game = game
        self.font = pygame.font.Font(None, 50)
        self.option = 0
        self.timer = 0
        self.unselected_size = (40,40)
        self.selected_size = (55,55)
        self.options_x = [0,0]
        self.pointer_x = 0
        self.load_res()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_a:
                        self.option = 0
                        self.cosmoman = pygame.transform.scale(self.sprite_cosmoman, self.selected_size)
                        self.alien = pygame.transform.scale(self.sprite_alien, self.unselected_size)
                    case pygame.K_d:
                        self.option = 1
                        self.cosmoman = pygame.transform.scale(self.sprite_cosmoman, self.unselected_size)
                        self.alien = pygame.transform.scale(self.sprite_alien, self.selected_size)
                    case pygame.K_RETURN:
                        self.game.skin = "cosmoman" if self.option == 0 else "alien"
                        self.game.enemyskin = "alien" if self.option == 0 else "cosmoman"
                        from scenes.game_scene import GameScene
                        self.manager.change_scene(GameScene(self.manager, self.game))
                        

    def update(self, keys):
        self.timer += 1
        if self.timer >= 30:
            self.timer = 0
            self.backgrounds.rotate()
        self.pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 155 + 100
        self.pointer_x += ((self.options_x[1] if self.option == 0 else self.options_x[2]) - self.pointer_x)  * 0.15


    def draw(self, screen):
        screen_size  = screen.get_size()
        self.options_x = [i* screen_size[0] / 3 for i in range(3)]

        screen.blit(self.backgrounds[0], (0,0))
        screen.blit(self.text1, (200, 180))
        color = (self.pulse, self.pulse, self.pulse)
        cosmoman_x = self.options_x[1] - self.cosmoman.get_width()/2
        alien_x = self.options_x[2] - self.alien.get_width()/2
        screen.blit(self.cosmoman, (cosmoman_x, screen_size[1]/2))
        screen.blit(self.alien, (alien_x, screen_size[1]/2))
        pygame.draw.rect(screen, color, (self.pointer_x - 35, 292, 70, 70), 3)



    def load_res(self):
        self.backgrounds = deque([
            resources.get_image("menu1"),
            resources.get_image("menu2"),
            resources.get_image("menu3"),
            resources.get_image("menu4")
        ])
        self.text1 = self.font.render("Обери ким ти будеш:", True, (255, 255, 255))
        self.sprite_alien = resources.get_sprite("alien")
        self.sprite_cosmoman = resources.get_sprite("cosmoman")

        self.cosmoman = pygame.transform.scale(self.sprite_cosmoman, (40, 40))
        self.alien = pygame.transform.scale(self.sprite_alien, (40, 40))