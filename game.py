import pygame
from settings import *
from entities.player import Player
from entities.bullet import Bullet
from entities.enemy import Enemy
import os
import random
import math
import resources

pygame.init()
pygame.mixer.init()

BASE_DIR = os.path.dirname(__file__)

shoot_sound = resources.get_sound("shoot")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#створення гравця й ворогів
player = Player(WIDTH/2, HEIGHT/2, resources.get_sprite("alien"))
#Вороги
player_img_normal = resources.get_sprite("alien")
player_img_normal = pygame.transform.scale(player_img_normal, (PLAYER_SIZE, PLAYER_SIZE))

player_img_enemy = resources.get_sprite("cosmoman")
player_img_enemy = pygame.transform.scale(player_img_enemy, (PLAYER_SIZE, PLAYER_SIZE))
enemy_img = resources.get_sprite("cosmoman")
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_SIZE, ENEMY_SIZE))

#фон
background = resources.get_image("bg")

menu_bg1 = resources.get_image("menu1")
menu_bg1 = pygame.transform.scale(menu_bg1, (WIDTH, HEIGHT))


menu_bg2 = resources.get_image("menu2")
menu_bg2 = pygame.transform.scale(menu_bg2, (WIDTH, HEIGHT))

menu_bg3 = resources.get_image("menu3")
menu_bg3 = pygame.transform.scale(menu_bg3, (WIDTH, HEIGHT))

menu_bg4 = resources.get_image("menu4")
menu_bg4 = pygame.transform.scale(menu_bg4, (WIDTH, HEIGHT))


#змінні
game_over = False
score = 0
game_state = "menu"
enemy_img_current = player_img_enemy
selected = 0
menu_frame = 0
menu_timer = 0
current_x = 242
target_x = 242
current_size1 = 40
current_size2 = 40
target_size1 = 40
target_size2 = 40

#вороги
enemies = []

#рестарт
def reset_game():
    global score, spawn_timer

    score = 0
    spawn_timer = 0

    enemies.clear()
    bullets.clear()

    player.rect.center = (WIDTH // 2, HEIGHT // 2)

#снаряд
bullets = []
shoot_cooldown = 0

#напрямок снаряду
direction_x = 0
direction_y = -1

#Для меню
language = "ua"
game_mode = "endless"   # endless / story
menu_option = 0
TEXT = {
    "ua": {
        "play": "Грати",
        "mode": "Режим",
        "language": "Мова",
        "exit": "Вихід",
        "endless": "Нескінченний",
        "story": "Сюжет",
    },

    "ru": {
        "play": "Играть",
        "mode": "Режим",
        "language": "Язык",
        "exit": "Выход",
        "endless": "Бесконечный",
        "story": "Сюжет",
    },

    "en": {
        "play": "Play",
        "mode": "Mode",
        "language": "Language",
        "exit": "Exit",
        "endless": "Endless",
        "story": "Story",
    }
}

#частота спавну ворогів
spawn_timer = 0

running = True
while running:
    keys = pygame.key.get_pressed()
    #меню
    if game_state == "menu":
        menu_timer += 1

        if menu_timer >= 30:#анімація
            menu_timer = 0

            if menu_frame == 0:
                menu_frame = 1
            elif menu_frame == 1:
                menu_frame = 2
            elif menu_frame == 2:
                menu_frame = 3
            elif menu_frame == 3:
                menu_frame = 0

        if menu_frame == 0:
            screen.blit(menu_bg1, (0, 0))
        elif menu_frame == 1:
            screen.blit(menu_bg2, (0, 0))
        elif menu_frame == 2:
            screen.blit(menu_bg3, (0, 0))
        elif menu_frame == 3:
            screen.blit(menu_bg4, (0, 0))

        font = pygame.font.Font(None, 50)#саме меню
        menu_items = [
            TEXT[language]["play"],
            f'{TEXT[language]["mode"]}: {TEXT[language][game_mode]}',
            f'{TEXT[language]["language"]}: {language.upper()}',
            TEXT[language]["exit"]
        ]
           
        for i, item in enumerate(menu_items):
            color = (255,255,0) if i == menu_option else (255,255,255)

            txt = font.render(item, True, color)
            screen.blit(txt, (250, 220 + i * 60))


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w:
                    menu_option = (menu_option - 1) % 4

                if event.key == pygame.K_s:
                    menu_option = (menu_option + 1) % 4

                if event.key == pygame.K_RETURN:

                    if menu_option == 0:
                        game_state = "character_select"

                    elif menu_option == 1:
                        game_mode = "story" if game_mode == "endless" else "endless"

                    elif menu_option == 2:
                        if language == "ua":
                            language = "ru"
                        elif language == "ru":
                            language = "en"
                        else:
                            language = "ua"

                    elif menu_option == 3:
                        running = False

        pygame.display.flip()
        clock.tick(FPS)
            
        continue

    if game_state == "character_select":

        menu_timer += 1

        if menu_timer >= 30:
            menu_timer = 0
            menu_frame = (menu_frame + 1) % 4
        if menu_frame == 0:
            screen.blit(menu_bg1, (0, 0))
        elif menu_frame == 1:
            screen.blit(menu_bg2, (0, 0))
        elif menu_frame == 2:
            screen.blit(menu_bg3, (0, 0))
        else:
            screen.blit(menu_bg4, (0, 0))

        font = pygame.font.Font(None, 50)

        #вибір
        text1 = font.render("Обери ким ти будеш:", True, (255, 255, 255))
        screen.blit(text1, (200 , 180))

        #анімація вибіру
        if selected == 0:
            target_x = 242
            target_size1 = 55
            target_size2 = 40


        if selected == 1:
            target_x = 442
            target_size2 = 55
            target_size1 = 40

        current_x += (target_x - current_x) * 0.15
        current_size1 += (target_size1 - current_size1) * 0.15
        current_size2 += (target_size2 - current_size2) * 0.15
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 155 + 100
        color = (pulse, pulse, pulse)
        pygame.draw.rect(screen, color, (current_x, 292, 70, 70), 3)           

        img1 = pygame.transform.scale(
            player_img_normal,
            (int(current_size1), int(current_size1))
        )

        img2 = pygame.transform.scale(
            player_img_enemy,
            (int(current_size2), int(current_size2))
        )

        screen.blit(img1, (250, 300))
        screen.blit(img2, (450, 300))

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_a:
                    selected = 0

                if event.key == pygame.K_d:
                    selected = 1

                if event.key == pygame.K_RETURN:

                    if selected == 0:
                        player_img = player_img_normal
                        enemy_img_current = player_img_enemy

                    else:
                        player_img = player_img_enemy
                        enemy_img_current = player_img_normal

                    game_state = "playing"

        pygame.display.flip()
        clock.tick(FPS)
        continue

    #Екран програшу
    if game_state == "game_over":
        screen.fill((0, 0, 0))

        font = pygame.font.Font(None, 74)
        text3 = font.render("Програв.", True, (255, 0, 0))
        text4 = font.render("Тебе сцапали.", True, (255, 0, 0))

        screen.blit(text3, (280, 180))
        screen.blit(text4, (220, 240))

        font2 = pygame.font.Font(None, 36)
        restart_text = font2.render("Натисни 'R' Для рестарту", True, (255, 255, 255))
        screen.blit(restart_text, (WIDTH//2 - 140, HEIGHT//2 + 20))

                #події
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    reset_game()
                    game_state = "character_select"

                    if menu_option == 0:  #грати

                        player_img = player_img_normal
                        enemy_img_current = player_img_enemy

                        game_state = "playing"

                    elif menu_option == 1:  #режим

                        if game_mode == "endless":
                            game_mode = "story"
                        else:
                            game_mode = "endless"

                    elif menu_option == 2:  #мова

                        if language == "ua":
                            language = "ru"
                        elif language == "ru":
                            language = "en"
                        else:
                            language = "ua"

                    elif menu_option == 3:  #вихід
                        running = False

        pygame.display.flip()
        clock.tick(FPS)
        continue
    
    #Гра
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                #ривок
                player.start_dash(keys)

    ###TIMERS
    direction_x = player.dir_x
    direction_y = player.dir_y

    if shoot_cooldown > 0: shoot_cooldown -= 1
    spawn_timer += 1

    ###LOGIC
    player.update(keys)

    #спавн снаряду
    if keys[pygame.K_l] and shoot_cooldown == 0:

        length = math.hypot(direction_x, direction_y)

        if length != 0:
            dx = direction_x / length
            dy = direction_y / length
        else:
            dx, dy = 0, -1

        bullets.append(Bullet(
            player.rect.centerx,
            player.rect.centery,
            dx, dy
        ))

        shoot_sound.play()
        shoot_cooldown = SHOOT_DELAY
        
    #видалення снарядів
    bullets = [
        b for b in bullets
        if not b.is_offscreen(WIDTH, HEIGHT)
    ]
    
    #спавн ворогів
    if spawn_timer >= SPAWN_DELAY:
        spawn_timer = 0

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

        enemies.append(Enemy(ex,ey,enemy_img_current))

    #рух ворогів
    for enemy in enemies:
        enemy.update(player.rect)

    #Колiзiї
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.collides(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                break
        bullet.update()

    for enemy in enemies:
        if enemy.collides(player.rect):
            game_state = "game_over"

    ###RENDERING
    screen.blit(background, (0, 0))

    for enemy in enemies:
        enemy.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)
    
    player.draw(screen)

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Рахунок: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    #END FRAME
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()