import pygame
from scene import Scene


class GameOverScene(Scene):
    
    def __init__(self, manager, game):
        self.manager = manager
        self.game = game
        font = pygame.font.Font(None, 74)
        font2 = pygame.font.Font(None, 36)
        self.textlose = font.render("Програв.", True, (255, 0, 0))
        self.textcatch = font.render("Тебе сцапали.", True, (255, 0, 0))
        self.restart_text = font2.render("Натисни 'R' Для рестарту", True, (255, 255, 255))


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    from scenes.game_scene import GameScene
                    self.manager.change_scene(GameScene(self.manager, self.game))

                        

    def update(self, keys):
        pass


    def draw(self, screen):
        screen_size = screen.get_size()
        screen.fill((0,0,0))
        screen.blit(self.textlose, (280, 180))
        screen.blit(self.textcatch, (280, 240))
        screen.blit(self.restart_text, (screen_size[0]//2 - 140, screen_size[1]//2 + 20))