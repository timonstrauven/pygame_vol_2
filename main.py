import pygame
import math
import random
from moviepy import VideoFileClip

pygame.init()
pygame.mixer.init()

# =========================
# INSTELLINGEN
# =========================

WIDTH = 1024
HEIGHT = 1024

SPELER_SNELHEID = 5
VIJAND_SNELHEID = 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Anton Tractor Supermarket")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 40)

# =========================
# VIDEO FUNCTIE
# =========================

def speel_video(video_pad, audio_pad):

    pygame.mixer.music.load(audio_pad)
    pygame.mixer.music.play()

    clip = VideoFileClip(video_pad)

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

speel_video(
    r"assets\ANTON 5sec.mp4",
    r"assets\muziek.mp3"
)

pygame.mixer.music.play(-1)

# =========================
# MAP
# =========================

achtergrond = pygame.image.load(
    r"assets\supermarket_map.png"
).convert()

achtergrond = pygame.transform.scale(
    achtergrond,
    (WIDTH, HEIGHT)
)

# =========================
# GELUID
# =========================

tung_geluid = pygame.mixer.Sound(
    r"assets\The Tung.mp3"
)

# =========================
# MUREN
# =========================

muren = [

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
# SPELER KLASSE
# =========================

class Speler:

    def __init__(self, x, y):

        self.afbeelding = pygame.image.load(
            r"assets\Sahur2.webp"
        ).convert_alpha()

        self.afbeelding = pygame.transform.scale(
            self.afbeelding,
            (64,64)
        )

        self.rect = pygame.Rect(x, y, 40, 40)

        self.snelheid = SPELER_SNELHEID

    def beweeg(self):

        toetsen = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if toetsen[pygame.K_LEFT]:
            dx = -self.snelheid

        if toetsen[pygame.K_RIGHT]:
            dx = self.snelheid

        if toetsen[pygame.K_UP]:
            dy = -self.snelheid

        if toetsen[pygame.K_DOWN]:
            dy = self.snelheid

        # horizontale collision
        self.rect.x += dx

        for muur in muren:

            if self.rect.colliderect(muur):
                self.rect.x -= dx

        # verticale collision
        self.rect.y += dy

        for muur in muren:

            if self.rect.colliderect(muur):
                self.rect.y -= dy

        # binnen scherm houden
        self.rect.x = max(
            0,
            min(WIDTH - self.rect.width, self.rect.x)
        )

        self.rect.y = max(
            0,
            min(HEIGHT - self.rect.height, self.rect.y)
        )

    def teken(self):

        screen.blit(
            self.afbeelding,
            (self.rect.x - 12, self.rect.y - 12)
        )

