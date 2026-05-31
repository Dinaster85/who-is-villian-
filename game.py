import pygame
from settings import *
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
player = pygame.Rect(400, 300, PLAYER_SIZE, PLAYER_SIZE)
player_img = resources.get_sprite("alien")
player_img = pygame.transform.scale(player_img, (PLAYER_SIZE, PLAYER_SIZE))
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
dash_time = 0
dash_cooldown_max = 0
dash_dx, dash_dy = 0, 0
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

    player.center = (WIDTH // 2, HEIGHT // 2)

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #фон гри
    screen.blit(background, (0, 0))

    #клавіші
    keys = pygame.key.get_pressed()

    #ривок
    if dash_time > 0:
        player.x += dash_dx * DASH_SPEED
        player.y += dash_dy * DASH_SPEED
        dash_time -= 1
        #напрямок ривку
        dash_dx = (keys[pygame.K_d] - keys[pygame.K_a])
        dash_dy = (keys[pygame.K_s] - keys[pygame.K_w])
    else:
        #базовий васд
        dx = (keys[pygame.K_d] - keys[pygame.K_a])
        dy = (keys[pygame.K_s] - keys[pygame.K_w])

        if dx != 0 or dy != 0:
            direction_x = dx
            direction_y = dy

        player.x += dx * PLAYER_SPEED
        player.y += dy * PLAYER_SPEED

    if shoot_cooldown > 0:
        shoot_cooldown -= 1

    #спавн снаряду
    if keys[pygame.K_l] and shoot_cooldown == 0:
        offset = 25

        length = math.hypot(direction_x, direction_y)
        if length != 0:
            dx = direction_x / length
            dy = direction_y / length
        else:
            dx, dy = 0, -1

        bullets.append({
            "rect": pygame.Rect(
                player.centerx + direction_x * offset,
                player.centery + direction_y * offset,
                10, 10
            ),
            "dx": dx,
            "dy": dy
        })

        shoot_sound.play()
        shoot_cooldown = SHOOT_DELAY
           
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet["rect"].colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                break
        pygame.draw.rect(screen, (255, 0, 0), bullet["rect"])
        bullet["rect"].x += bullet["dx"] * BULLET_SPEED
        bullet["rect"].y += bullet["dy"] * BULLET_SPEED

        
    #видалення снарядів
    bullets = [
        b for b in bullets
        if 0 < b["rect"].x < WIDTH and 0 < b["rect"].y < HEIGHT
    ]


    #кнопка для ривку
    if keys[pygame.K_e] and DASH_COOLDOWN == 0 and dash_time == 0:
        dash_time = DASH_DURATION
        DASH_COOLDOWN = dash_cooldown_max
    
    #Самі вороги
    spawn_timer += 1
    #спавн ворогів
    if spawn_timer >= SPAWN_DELAY:
        spawn_timer = 0

        enemy = pygame.Rect(0, 0, ENEMY_SIZE, ENEMY_SIZE)

        side = random.choice(["top", "bottom", "left", "right"])

        if side == "top":
            enemy.x = random.randint(0, WIDTH)
            enemy.y = 0
        elif side == "bottom":
            enemy.x = random.randint(0, WIDTH)
            enemy.y = HEIGHT
        elif side == "left":
            enemy.x = 0
            enemy.y = random.randint(0, HEIGHT)
        elif side == "right":
            enemy.x = WIDTH
            enemy.y = random.randint(0, HEIGHT)

        enemies.append(enemy)

    #рух ворогів
    for enemy in enemies:
        if enemy.x < player.x:
            enemy.x += ENEMY_SPEED
        if enemy.x > player.x:
            enemy.x -= ENEMY_SPEED
        if enemy.y < player.y:
            enemy.y += ENEMY_SPEED
        if enemy.y > player.y:
            enemy.y -= ENEMY_SPEED

    #відмальовка ворогів
    for enemy in enemies:
        screen.blit(enemy_img_current, (enemy.x, enemy.y))

    #смерть гравця
    for enemy in enemies:
        if player.colliderect(enemy):
            game_state = "game_over"
            score = 0
            enemies.clear()
            bullets.clear()
            spawn_timer = 0
            break

        if game_state == "game_over":
            continue
    #краї вікна
    player.clamp_ip(screen.get_rect())

    #сам гравець
    screen.blit(player_img, player)

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Рахунок: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()