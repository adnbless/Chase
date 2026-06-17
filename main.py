# Chased
# Author: Aiden C
# Date: May 19th

import random

import pygame

teleporter = None
teleporter_timer = 0
teleporter_active = False

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIDTH = 900
HEIGHT = 600

FPS = 60
PLAYER_SIZE = 40
PLAYER_SPEED = 4

GRAVITY = 0.5
JUMP_POWER = -10

GAME_TIME = 60

pygame.init()

# audio
pygame.mixer.init()

pygame.mixer.music.load("assets/Sounds/background.mp3")
pygame.mixer.music.set_volume(0.5)  # 0.0 to 1.0
pygame.mixer.music.play(-1)  # -1 = loop forever

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chased")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
title_font = pygame.font.SysFont(None, 100)
menu_font = pygame.font.SysFont(None, 50)
arrow_font = pygame.font.SysFont(None, 30)

# images
player_img = pygame.image.load("assets/Images/player.jpg")
chaser_img = pygame.image.load("assets/Images/chaser.jpg")
game_bg = pygame.image.load("assets/Images/background.jpg")
game_bg = pygame.transform.scale(game_bg, (WIDTH, HEIGHT))

player_img = pygame.transform.scale(player_img, (PLAYER_SIZE, PLAYER_SIZE))
chaser_img = pygame.transform.scale(chaser_img, (PLAYER_SIZE, PLAYER_SIZE))

menu_bg = pygame.image.load("assets/Images/BACKGROUND.jpeg")
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

# platforms
platforms = [
    pygame.Rect(0, 550, 900, 50),
    pygame.Rect(80, 420, 40, 130),
    pygame.Rect(120, 420, 160, 20),
    pygame.Rect(80, 300, 40, 120),
    pygame.Rect(120, 300, 140, 20),
    pygame.Rect(200, 220, 120, 20),
    pygame.Rect(380, 430, 140, 20),
    pygame.Rect(420, 330, 40, 140),
    pygame.Rect(460, 330, 140, 20),
    pygame.Rect(500, 220, 160, 20),
    pygame.Rect(700, 420, 40, 130),
    pygame.Rect(740, 420, 100, 20),
    pygame.Rect(700, 250, 40, 120),
    pygame.Rect(740, 300, 100, 20),
    pygame.Rect(760, 170, 100, 20),
    pygame.Rect(120, 120, 140, 20),
    pygame.Rect(400, 100, 20, 160),
    pygame.Rect(520, 150, 100, 20),
    pygame.Rect(-20, 0, 20, HEIGHT),
    pygame.Rect(WIDTH, 0, 20, HEIGHT),
    pygame.Rect(0, -20, WIDTH, 20),
]

# Player
player_x, player_y = 200, 200
player_vy = 0

# Chaser
chaser_x, chaser_y = 600, 200
chaser_vy = 0

chaser_is_it = True
touching = False
winner = "Player 1 (WASD) Wins!"

start_ticks = pygame.time.get_ticks()


def draw_it_arrow(x, y):
    arrow = arrow_font.render("⬇", True, BLACK)
    screen.blit(arrow, (x + PLAYER_SIZE // 2 - 6, y - 25))


def title_screen():
    waiting = True

    while waiting:
        screen.blit(menu_bg, (0, 0))

        title_text = title_font.render("CHASED", True, BLACK)
        start_text = menu_font.render("Press SPACE to Start", True, BLACK)
        controls_text = menu_font.render("WASD vs Arrow Keys", True, BLACK)

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 150))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 300))
        screen.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, 360))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

        clock.tick(FPS)


screen.blit(menu_bg, (0, 0))
title_screen()

running = True


# TP
def spawn_teleporter():
    global teleporter, teleporter_active, teleporter_timer

    x = random.randint(100, WIDTH - 100)
    y = random.randint(100, HEIGHT - 200)

    teleporter = pygame.Rect(x, y, 40, 40)
    teleporter_active = True
    teleporter_timer = pygame.time.get_ticks()


# MAIN GAME LOOP

while running:
    clock.tick(FPS)

    if not teleporter_active:
        if random.randint(1, 300) == 1:
            spawn_teleporter()

    if teleporter_active:
        if pygame.time.get_ticks() - teleporter_timer > 5000:
            teleporter_active = False
            teleporter = None

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # input
    keys = pygame.key.get_pressed()

    # timer
    time_left = max(0, GAME_TIME - (pygame.time.get_ticks() - start_ticks) / 1000)
    if time_left <= 0:
        running = False
        if chaser_is_it:
            winner = "Player 1 (WASD) Wins!"
        else:
            winner = "Player 2 (Arrows) Wins!"

    # hitboxes
    player_hitbox = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
    chaser_hitbox = pygame.Rect(chaser_x, chaser_y, PLAYER_SIZE, PLAYER_SIZE)

    # player
    player_x += (keys[pygame.K_d] - keys[pygame.K_a]) * PLAYER_SPEED
    player_hitbox.x = player_x

    player_touch_left = False
    player_touch_right = False

    for p in platforms:
        if player_hitbox.colliderect(p):
            if player_hitbox.centerx < p.centerx:
                player_x = p.left - PLAYER_SIZE
                player_touch_right = True
            else:
                player_x = p.right
                player_touch_left = True
            player_hitbox.x = player_x

    player_vy += GRAVITY
    player_y += player_vy
    player_hitbox.y = player_y

    player_on_ground = False

    for p in platforms:
        if player_hitbox.colliderect(p):
            if player_vy > 0:
                player_y = p.top - PLAYER_SIZE
                player_vy = 0
                player_on_ground = True
            elif player_vy < 0:
                player_y = p.bottom
                player_vy = 0
            player_hitbox.y = player_y

    if keys[pygame.K_w]:
        if player_on_ground:
            player_vy = JUMP_POWER
        elif player_touch_left:
            player_vy = JUMP_POWER
            player_x += 10
        elif player_touch_right:
            player_vy = JUMP_POWER
            player_x -= 10

    # chaser
    chaser_x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * PLAYER_SPEED
    chaser_hitbox.x = chaser_x

    chaser_touch_left = False
    chaser_touch_right = False

    for p in platforms:
        if chaser_hitbox.colliderect(p):
            if chaser_hitbox.centerx < p.centerx:
                chaser_x = p.left - PLAYER_SIZE
                chaser_touch_right = True
            else:
                chaser_x = p.right
                chaser_touch_left = True
            chaser_hitbox.x = chaser_x

    chaser_vy += GRAVITY
    chaser_y += chaser_vy
    chaser_hitbox.y = chaser_y

    chaser_on_ground = False

    for p in platforms:
        if chaser_hitbox.colliderect(p):
            if chaser_vy > 0:
                chaser_y = p.top - PLAYER_SIZE
                chaser_vy = 0
                chaser_on_ground = True
            elif chaser_vy < 0:
                chaser_y = p.bottom
                chaser_vy = 0
            chaser_hitbox.y = chaser_y

    if keys[pygame.K_UP]:
        if chaser_on_ground:
            chaser_vy = JUMP_POWER
        elif chaser_touch_left:
            chaser_vy = JUMP_POWER
            chaser_x += 10
        elif chaser_touch_right:
            chaser_vy = JUMP_POWER
            chaser_x -= 10

    # tag system
    if player_hitbox.colliderect(chaser_hitbox):
        if not touching:
            chaser_is_it = not chaser_is_it
            touching = True
    else:
        touching = False

    if teleporter_active and teleporter:
        if player_hitbox.colliderect(teleporter):
            player_x = random.randint(100, 800)
            player_y = random.randint(100, 400)
            teleporter_active = False
            teleporter = None

        elif chaser_hitbox.colliderect(teleporter):
            chaser_x = random.randint(100, 800)
            chaser_y = random.randint(100, 400)
            teleporter_active = False
            teleporter = None

    # draw
    screen.blit(game_bg, (0, 0))

    for p in platforms:
        pygame.draw.rect(screen, BLACK, p)

    screen.blit(player_img, (player_x, player_y))
    screen.blit(chaser_img, (chaser_x, chaser_y))

    if chaser_is_it:
        draw_it_arrow(chaser_x, chaser_y)
    else:
        draw_it_arrow(player_x, player_y)

    timer_text = font.render(f"Time Left: {int(time_left)}", True, BLACK)
    screen.blit(timer_text, (20, 20))

    if teleporter_active and teleporter:
        pygame.draw.circle(
            screen,
            (0, 255, 255),
            (
                teleporter.x + teleporter.width // 2,
                teleporter.y + teleporter.height // 2,
            ),
            20,
        )

    pygame.display.flip()

# end screen
end_screen = True
while end_screen:
    screen.blit(menu_bg, (0, 0))

    win_text = title_font.render(winner, True, BLACK)
    sub_text = menu_font.render("The 'it' player lost!", True, BLACK)
    quit_text = menu_font.render("Press SPACE to quit", True, BLACK)

    screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, 150))
    screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, 300))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 370))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_screen = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                end_screen = False

    clock.tick(FPS)

pygame.quit()
