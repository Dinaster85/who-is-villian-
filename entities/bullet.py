import pygame
from settings import BULLET_SPEED


class Bullet:
    def __init__(self, x, y, dx, dy):
        self.rect = pygame.Rect(x, y, 10, 10)

        self.dx = dx
        self.dy = dy

    def update(self):
        self.rect.x += self.dx * BULLET_SPEED
        self.rect.y += self.dy * BULLET_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def is_offscreen(self, width, height):
        # перевірка виходу за межі екрану
        return (
            self.rect.x < 0 or self.rect.x > width or
            self.rect.y < 0 or self.rect.y > height
        )

    def collides(self, enemy):
        # перевірка колізії з ворогом
        return self.rect.colliderect(enemy.rect)