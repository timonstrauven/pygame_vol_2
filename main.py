import pygame
import math
import random
from moviepy import VideoFileClip

pygame.init()
pygame.mixer.init()

# =========================
# SETTINGS
# =========================

WIDTH = 1024
HEIGHT = 1024

PLAYER_SPEED = 5
ENEMY_SPEED = 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Anton Tractor Supermarket")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 40)

# =========================
# VIDEO FUNCTION
# =========================

def play_video(video_path, audio_path):

    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    clip = VideoFileClip(video_path)

    for frame in clip.iter_frames(fps=30, dtype="uint8"):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        frame_surface = pygame.surfarray.make_surface(
            frame.swapaxes(0, 1)
        )

        frame_surface = pygame.transform.scale(
            frame_surface,
            (WIDTH, HEIGHT)
        )

        screen.blit(frame_surface, (0,0))

        pygame.display.flip()

        clock.tick(30)

    clip.close()

    screen.fill((0,0,0))
    pygame.display.flip()

# =========================
# INTRO VIDEO
# =========================

play_video(
    r"assets\ANTON 5sec.mp4",
    r"assets\muziek.mp3"
)

pygame.mixer.music.play(-1)

# =========================
# MAP
# =========================

bg = pygame.image.load(
    r"assets\supermarket_map.png"
).convert()

bg = pygame.transform.scale(
    bg,
    (WIDTH, HEIGHT)
)

# =========================
# LEVEL 1 PLAYER = SAHUR2
# =========================

player_img = pygame.image.load(
    r"assets\Sahur2.webp"
).convert_alpha()

player_img = pygame.transform.scale(
    player_img,
    (64,64)
)

# =========================
# LEVEL 1 ENEMY = TRACTOR
# =========================

enemy_img = pygame.image.load(
    r"assets\tractor_player.png"
).convert_alpha()

enemy_img = pygame.transform.scale(
    enemy_img,
    (80,80)
)

# =========================
# MELKFLES
# =========================

milk_img = pygame.image.load(
    r"assets\milk.png"
).convert_alpha()

milk_img = pygame.transform.scale(
    milk_img,
    (40,40)
)

# =========================
# GELUIDEN
# =========================

tung_sound = pygame.mixer.Sound(
    r"assets\The Tung.mp3"
)

# =========================
# COLLISION SCHAPPEN
# =========================

walls = [

    pygame.Rect(130,120,250,70),
    pygame.Rect(650,120,250,70),

    pygame.Rect(420,220,200,60),

    pygame.Rect(250,340,70,220),
    pygame.Rect(720,340,70,220),

    pygame.Rect(420,390,220,60),

    pygame.Rect(250,650,180,70),
    pygame.Rect(620,650,180,70),

    pygame.Rect(120,820,300,60),
    pygame.Rect(620,820,300,60)

]

# =========================
# PLAYER HITBOX
# =========================

player = pygame.Rect(
    500,
    900,
    40,
    40
)

# =========================
# ENEMY HITBOX
# =========================

enemy = pygame.Rect(
    500,
    100,
    60,
    60
)

# =========================
# MELKFLESJES
# =========================

def spawn_bottles(amount):

    bottles = []

    for i in range(amount):

        while True:

            x = random.randint(80, 940)
            y = random.randint(80, 940)

            bottle = pygame.Rect(x, y, 30, 30)

            blocked = False

            for wall in walls:

                if bottle.colliderect(wall):
                    blocked = True

            if not blocked:

                bottles.append(bottle)

                break

    return bottles

milk_bottles = spawn_bottles(10)

# =========================
# SCORE
# =========================

score = 0

# =========================
# LEVEL SYSTEM
# =========================

level = 1

# =========================
# GAME LOOP
# =========================

running = True

while running:

    clock.tick(60)

    # =====================
    # EVENTS
    # =====================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # =====================
    # PLAYER MOVEMENT
    # =====================

    keys = pygame.key.get_pressed()

    dx = 0
    dy = 0

    if keys[pygame.K_LEFT]:
        dx = -PLAYER_SPEED

    if keys[pygame.K_RIGHT]:
        dx = PLAYER_SPEED

    if keys[pygame.K_UP]:
        dy = -PLAYER_SPEED

    if keys[pygame.K_DOWN]:
        dy = PLAYER_SPEED

    # horizontale collision
    player.x += dx

    for wall in walls:

        if player.colliderect(wall):
            player.x -= dx

    # verticale collision
    player.y += dy

    for wall in walls:

        if player.colliderect(wall):
            player.y -= dy

    # binnen scherm houden
    player.x = max(0, min(WIDTH - player.width, player.x))
    player.y = max(0, min(HEIGHT - player.height, player.y))

    # =====================
    # ENEMY AI
    # =====================

    vx = player.centerx - enemy.centerx
    vy = player.centery - enemy.centery

    distance = math.hypot(vx, vy)

    if distance != 0:

        vx /= distance
        vy /= distance

    enemy.x += int(vx * ENEMY_SPEED)
    enemy.y += int(vy * ENEMY_SPEED)

    # =====================
    # MELKFLESJES
    # =====================

    for bottle in milk_bottles[:]:

        if player.colliderect(bottle):

            milk_bottles.remove(bottle)

            score += 25

            tung_sound.play()

    # =====================
    # LEVEL 2
    # =====================

    if len(milk_bottles) == 0 and level == 1:

        # level 1 eindvideo
        play_video(
            r"assets\Aura of T.mp4",
            r"assets\muziek.mp3"
        )

        # nieuwe muziek
        pygame.mixer.music.stop()

        pygame.mixer.music.load(
            r"assets\All Of The Lights.mp3"
        )

        pygame.mixer.music.play(-1)

        # LEVEL 2 PLAYER = KIRK
        player_img = pygame.image.load(
            r"assets\Kirk.png"
        ).convert_alpha()

        player_img = pygame.transform.scale(
            player_img,
            (64,64)
        )

        # LEVEL 2 ENEMY = OLIVE DELIGHTS
        enemy_img = pygame.image.load(
            r"assets\olive delights.png"
        ).convert_alpha()

        enemy_img = pygame.transform.scale(
            enemy_img,
            (100,100)
        )

        # speler resetten
        player.x = 500
        player.y = 900

        # enemy resetten
        enemy.x = 500
        enemy.y = 100

        # moeilijker
        ENEMY_SPEED = 4

        # nieuwe melkflesjes
        milk_bottles = spawn_bottles(15)

        level = 2

    # =====================
    # GAME OVER
    # =====================

    if player.colliderect(enemy):

        print("GAME OVER")

        running = False

    # =====================
    # DRAW
    # =====================

    screen.blit(bg, (0,0))

    # melkflesjes
    for bottle in milk_bottles:

        screen.blit(
            milk_img,
            bottle
        )

    # speler
    screen.blit(
        player_img,
        (player.x - 12, player.y - 12)
    )

    # enemy
    screen.blit(
        enemy_img,
        (enemy.x - 20, enemy.y - 20)
    )

    # score
    score_text = font.render(
        f"Score: {score}",
        True,
        (255,255,255)
    )

    screen.blit(score_text, (20,20))

    # level
    level_text = font.render(
        f"Level: {level}",
        True,
        (255,255,0)
    )

    screen.blit(level_text, (20,70))

    pygame.display.flip()

pygame.quit()