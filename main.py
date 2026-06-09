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

# =========================
# VIJAND KLASSE
# =========================

class Vijand:

    def __init__(self, x, y):

        self.afbeelding = pygame.image.load(
            r"assets\tractor_player.png"
        ).convert_alpha()

        self.afbeelding = pygame.transform.scale(
            self.afbeelding,
            (80,80)
        )

        self.rect = pygame.Rect(x, y, 60, 60)

        self.snelheid = VIJAND_SNELHEID

    def beweeg(self, speler):

        vx = speler.rect.centerx - self.rect.centerx
        vy = speler.rect.centery - self.rect.centery

        afstand = math.hypot(vx, vy)#berekent de afstand tussen de speler en vijand, gevonden in een tutorial

        if afstand != 0:

            vx /= afstand
            vy /= afstand

        self.rect.x += int(vx * self.snelheid)
        self.rect.y += int(vy * self.snelheid)

    def teken(self):

        screen.blit(
            self.afbeelding,
            (self.rect.x - 20, self.rect.y - 20)
        )

# =========================
# MELKFLES KLASSE
# =========================

class Melkfles:

    def __init__(self):

        self.afbeelding = pygame.image.load(
            r"assets\milk.png"
        ).convert_alpha()

        self.afbeelding = pygame.transform.scale(
            self.afbeelding,
            (40,40)
        )

        while True:

            x = random.randint(80, 940)
            y = random.randint(80, 940)

            self.rect = pygame.Rect(x, y, 30, 30)

            geblokkeerd = False

            for muur in muren:

                if self.rect.colliderect(muur):
                    geblokkeerd = True

            if not geblokkeerd:
                break

    def teken(self):

        screen.blit(
            self.afbeelding,
            self.rect
        )

# =========================
# SPEL KLASSE
# =========================

class Spel:

    def __init__(self):

        self.level = 1

        self.score = 0

        self.running = True

        self.speler = Speler(500, 900)

        self.vijand = Vijand(500, 100)

        self.melkflessen = []

        self.maak_melkflessen(10)
    

    def run(self):

        while self.running:

            clock.tick(60)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

            self.update()

            self.teken()

        pygame.quit()

    # =====================
    # MELKFLESSEN MAKEN
    # =====================

    def maak_melkflessen(self, aantal):

        self.melkflessen.clear()

        for i in range(aantal):

            self.melkflessen.append(
                Melkfles()
            )

    # =====================
    # LEVEL 2
    # =====================

    def start_level_2(self):

        speel_video(
            r"assets\Aura of T.mp4",
            r"assets\muziek.mp3"
        )

        pygame.mixer.music.stop()

        pygame.mixer.music.load(
            r"assets\All Of The Lights.mp3"
        )

        pygame.mixer.music.play(-1)

        # nieuwe speler afbeelding
        self.speler.afbeelding = pygame.image.load(
            r"assets\Kirk.png"
        ).convert_alpha()

        self.speler.afbeelding = pygame.transform.scale(
            self.speler.afbeelding,
            (64,64)
        )

        # nieuwe vijand afbeelding
        self.vijand.afbeelding = pygame.image.load(# Verandert de afbeelding van de vijand, van anton naar kanye.
            r"assets\olive delights.png"
        ).convert_alpha()

        self.vijand.afbeelding = pygame.transform.scale(
            self.vijand.afbeelding,
            (100,100)
        )

        # reset posities
        self.speler.rect.x = 500
        self.speler.rect.y = 900

        self.vijand.rect.x = 500
        self.vijand.rect.y = 100

        # sneller maken
        self.vijand.snelheid = 4

        # nieuwe melkflessen
        self.maak_melkflessen(15)

        self.level = 2

    # =====================
    # UPDATE
    # =====================

    def update(self):

        self.speler.beweeg()

        self.vijand.beweeg(self.speler)

        # melkflessen pakken
        for fles in self.melkflessen[:]:

            if self.speler.rect.colliderect(fles.rect):

                self.melkflessen.remove(fles)

                self.score += 25

                tung_geluid.play()

        # level systeem
        if len(self.melkflessen) == 0 and self.level == 1:

            self.start_level_2()

        elif len(self.melkflessen) == 0 and self.level == 2:

            print("JE HEBT GEWONNEN!")

            self.running = False

        # game over
        if self.speler.rect.colliderect(self.vijand.rect):

            print("GAME OVER")

            self.running = False

    # =====================
    # TEKENEN
    # =====================

    def teken(self):

        screen.blit(achtergrond, (0,0))

        # melkflessen
        for fles in self.melkflessen:

            fles.teken()

        # speler
        self.speler.teken()

        # vijand
        self.vijand.teken()

        # score
        score_tekst = font.render(
            f"Score: {self.score}",
            True,
            (255,255,255)
        )

        screen.blit(score_tekst, (20,20))

        # level
        level_tekst = font.render(
            f"Level: {self.level}",
            True,
            (255,255,0)
        )

        screen.blit(level_tekst, (20,70))

        pygame.display.flip()

    # =====================
    # GAME LOOP
    # =====================

    def run(self):

        while self.running:

            clock.tick(60)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

            self.update()

            self.teken()

        pygame.quit()

# =========================
# START SPEL
# =========================

spel = Spel()
spel.run()
