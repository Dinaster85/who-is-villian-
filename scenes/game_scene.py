import pygame, math, random
import resources
from scene import Scene
from entities.player import Player
from entities.bullet import Bullet
from entities.enemy import Enemy
from settings import SHOOT_DELAY, SPAWN_DELAY, ENEMY_SIZE, WIDTH, HEIGHT

class GameScene(Scene):
    
    def __init__(self, manager, game):
        self.manager = manager
        self.game = game
        self.score = 0
        self.spawn_timer = 0
        self.shoot_cooldown = 0
        self.player = Player(WIDTH/2, HEIGHT/2,resources.get_sprite(game.skin))
        self.bullets = []
        self.enemies = []
        self.background = resources.get_image("bg")
        self.shoot_sound = resources.get_sound("shoot")
        self.enemy_sprite = pygame.transform.scale(resources.get_sprite(game.enemyskin), (ENEMY_SIZE, ENEMY_SIZE))


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_e:
                        self.player.start_dash()
                    

    def update(self, keys):
        self.player.update(keys)
        self.spawn_timer +=1
        if self.shoot_cooldown > 0: self.shoot_cooldown -= 1
        if keys[pygame.K_l] and self.shoot_cooldown == 0:

            self.bullets.append(Bullet(
                self.player.rect.centerx,
                self.player.rect.centery,
                self.player.dir_x,
                self.player.dir_y
            ))

            self.shoot_sound.play()
            self.shoot_cooldown = SHOOT_DELAY
        
        bullets = [
            b for b in self.bullets
            if not b.is_offscreen(WIDTH, HEIGHT)
        ]
        #спавн ворогів
        if self.spawn_timer >= SPAWN_DELAY:
            self.spawn_timer = 0

            side = random.choice(["top", "bottom", "left", "right"])
            ex, ey = 0, 0
            if side == "top":
                ex = random.randint(0, WIDTH)
            elif side == "bottom":
                ex = random.randint(0, WIDTH)
                ey = HEIGHT
            elif side == "left":
                ey = random.randint(0, HEIGHT)
            elif side == "right":
                ex = WIDTH
                ey = random.randint(0, HEIGHT)

            self.enemies.append(Enemy(ex,ey,self.enemy_sprite))

        #рух ворогів
        for enemy in self.enemies:
            enemy.update(self.player.rect)

        #Колiзiї
        for bullet in self.bullets[:]:
            bullet.update()
            for enemy in self.enemies[:]:
                if bullet.collides(enemy):
                    bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 1
                    break

        for enemy in self.enemies:
            if enemy.collides(self.player.rect):
                from scenes.gameover_scene import GameOverScene
                self.manager.change_scene(GameOverScene(self.manager, self.game))



    def draw(self, screen):
        screen.blit(self.background, (0,0))
        for enemy in self.enemies:
            enemy.draw(screen)
        for bullet in self.bullets:
            bullet.draw(screen)
        self.player.draw(screen)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Рахунок: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))