import pygame
from scene_manager import SceneManager
from settings import WIDTH, HEIGHT, FPS
from game import Game
from scenes.menu_scene import MenuScene


pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

game = Game()
scenes = SceneManager()
scenes.change_scene(MenuScene(scenes, game))


while game.running:

    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    WIDTH, HEIGHT = screen.get_size()

    for event in events:
        if event.type == pygame.QUIT:
            game.running = False

    scenes.scene.handle_events(events)
    scenes.scene.update(keys)
    scenes.scene.draw(screen)


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()