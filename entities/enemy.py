import pygame
from settings import ENEMY_SIZE, ENEMY_SPEED


class Enemy:
    def __init__(self, x, y, sprite):
        self.rect = pygame.Rect(x, y, ENEMY_SIZE, ENEMY_SIZE)
        self.sprite = pygame.transform.scale(sprite, (ENEMY_SIZE, ENEMY_SIZE))

        self.speed = ENEMY_SPEED

    def update(self, player_rect):
        # рух до гравця по X
        if self.rect.x < player_rect.x:
            self.rect.x += self.speed
        elif self.rect.x > player_rect.x:
            self.rect.x -= self.speed

        # рух до гравця по Y
        if self.rect.y < player_rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player_rect.y:
            self.rect.y -= self.speed

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)

    def collides(self, rect):
        # перевірка колізії з іншим об’єктом
        return self.rect.colliderect(rect)