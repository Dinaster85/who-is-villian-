import pygame
from scene import Scene
from collections import deque
import resources
from translations import TEXT
from scenes.character_select_scene import CharacterSelectScene


class MenuScene(Scene):
    
    def __init__(self, manager, game):
        self.manager = manager
        self.game = game
        self.font = pygame.font.Font(None, 50)
        self.game_mode = "endless"
        self.langs = deque(TEXT.keys())
        self.option = 0
        self.timer = 0
        self.backgrounds = deque([
            resources.get_image("menu1"),
            resources.get_image("menu2"),
            resources.get_image("menu3"),
            resources.get_image("menu4")
        ])


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_w:
                        self.option = (self.option - 1) % 4
                    case pygame.K_s:
                        self.option = (self.option + 1) % 4

                    case pygame.K_RETURN:
                        if self.option == 0:
                            self.manager.change_scene(CharacterSelectScene(self.manager, self.game))
                        elif self.option == 1:
                            self.game_mode = "story" if self.game_mode == "endless" else "endless"
                        elif self.option == 2:
                            self.langs.rotate()
                            self.game.language = self.langs[0]
                        elif self.option == 3: 
                            self.game.running = False
                        

    def update(self, keys):
        self.timer += 1
        if self.timer >= 30:
            self.timer = 0
            self.backgrounds.rotate()


    def draw(self, screen):
        screen.blit(self.backgrounds[0], (0,0))
        menu_items = [
            TEXT[self.game.language]["play"],
            f'{TEXT[self.game.language]["mode"]}: {TEXT[self.game.language][self.game_mode]}',
            f'{TEXT[self.game.language]["language"]}: {self.game.language.upper()}',
            TEXT[self.game.language]["exit"]
        ]
        for i, item in enumerate(menu_items):
            color = (255, 255, 0) if i == self.option else (255, 255, 255)
            txt = self.font.render(item, True, color)
            screen.blit(txt, (250, 220 + i * 60))