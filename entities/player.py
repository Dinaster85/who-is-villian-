import pygame
from settings import WIDTH, HEIGHT, PLAYER_SIZE, PLAYER_SPEED, DASH_SPEED, DASH_DURATION


class Player:
    def __init__(self, x, y, sprite):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.sprite = pygame.transform.scale(sprite, (PLAYER_SIZE, PLAYER_SIZE))

        self.speed = PLAYER_SPEED

        # напрямок (для стрільби)
        self.dir_x = 0
        self.dir_y = -1

        # ривок
        self.dash_time = 0
        self.dash_cooldown = 0
        self.dash_dx = 0
        self.dash_dy = 0

    def update(self, keys):
        # режим ривка
        if self.dash_time > 0:
            self.rect.x += self.dash_dx * DASH_SPEED
            self.rect.y += self.dash_dy * DASH_SPEED
            self.dash_time -= 1
            return

        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]

        if dx != 0 or dy != 0:
            self.dir_x = dx
            self.dir_y = dy

        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.clamp_to_screen()

    def start_dash(self):
        if self.dash_time == 0:
            self.dash_dx = self.dir_x
            self.dash_dy = self.dir_y
            self.dash_time = DASH_DURATION
            self.dash_cooldown = 0 # TODO чому???

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)
        self.clamp_to_screen()

    def clamp_to_screen(self):
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > HEIGHT: self.rect.bottom = HEIGHT
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH