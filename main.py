import pygame
import random
import math
from moviepy import VideoFileClip

# ==================================================
# INITIALISATIE
# ==================================================

pygame.init()
pygame.mixer.init()

# ==================================================
# CONSTANTEN
# ==================================================

WIDTH = 900
HEIGHT = 900

FPS = 60

SPELER_SNELHEID = 5
VIJAND_SNELHEID = 2

SPELER_GROOTTE = 64
VIJAND_GROOTTE = 80
MELKFLES_GROOTTE = 40

WIT = (255, 255, 255)
GEEL = (255, 255, 0)
ROOD = (255, 0, 0)
ZWART = (0, 0, 0)

# ==================================================
# SCHERM
# ==================================================

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Videogame 1")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 40)
grote_font = pygame.font.SysFont("Arial", 70)

# ==================================================
# HULPFUNCTIES
# ==================================================

def laad_afbeelding(
    pad: str,
    grootte: tuple[int, int]
) -> pygame.Surface:

    try:

        afbeelding = pygame.image.load(
            pad
        ).convert_alpha()

        afbeelding = pygame.transform.scale(
            afbeelding,
            grootte
        )

        return afbeelding

    except pygame.error:

        print(f"FOUT: afbeelding niet gevonden -> {pad}")

        fallback = pygame.Surface(grootte)

        fallback.fill(ROOD)

        return fallback


def speel_video(
    video_pad: str,
    audio_pad: str
) -> None:

    try:

        pygame.mixer.music.load(audio_pad)

        pygame.mixer.music.play()

        clip = VideoFileClip(video_pad)

        for frame in clip.iter_frames(
            fps=30,
            dtype="uint8"
        ):

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

            screen.blit(frame_surface, (0, 0))

            pygame.display.flip()

            clock.tick(30)

        clip.close()

    except Exception as fout:

        print("Video kon niet afgespeeld worden:")
        print(fout)

# ==================================================
# MAP MANAGER
# ==================================================

class MapManager:

    def __init__(self):

        self.supermarket_map = laad_afbeelding(
            r"assets\supermarket_map.png",
            (WIDTH, HEIGHT)
        )

        self.backrooms_map = laad_afbeelding(
            r"assets\backrooms_map.png",
            (WIDTH, HEIGHT)
        )

        self.supermarket_muren = [

            pygame.Rect(160,170,170,50),
            pygame.Rect(160,170,50,180),

            pygame.Rect(390,210,240,50),

            pygame.Rect(690,170,170,50),
            pygame.Rect(810,170,50,180),

            pygame.Rect(270,330,60,220),

            pygame.Rect(370,380,280,60),

            pygame.Rect(690,330,60,220),

            pygame.Rect(400,540,240,50),

            pygame.Rect(260,650,60,170),
            pygame.Rect(260,760,120,60),

            pygame.Rect(420,690,190,50),

            pygame.Rect(610,690,60,130),
            pygame.Rect(610,760,120,60)

        ]

        self.backrooms_muren = [

            pygame.Rect(0,0,1024,25),
            pygame.Rect(0,999,1024,25),
            pygame.Rect(0,0,25,1024),
            pygame.Rect(999,0,25,1024)

        ]

        self.achtergrond = self.supermarket_map

        self.muren = self.supermarket_muren

    def start_level_2(self) -> None:

        self.achtergrond = self.backrooms_map

        self.muren = self.backrooms_muren

# ==================================================
# SPELER
# ==================================================

class Speler:

    def __init__(
        self,
        x: int,
        y: int
    ):

        self.afbeelding = laad_afbeelding(
            r"assets\Sahur2.webp",
            (SPELER_GROOTTE, SPELER_GROOTTE)
        )

        self.rect = pygame.Rect(
            x,
            y,
            40,
            40
        )

        self.snelheid = SPELER_SNELHEID

    def beweeg(
        self,
        muren: list[pygame.Rect]
    ) -> None:

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

        self.beweeg_horizontaal(dx, muren)

        self.beweeg_verticaal(dy, muren)

        self.blijf_in_scherm()

    def beweeg_horizontaal(
        self,
        dx: int,
        muren: list[pygame.Rect]
    ) -> None:

        self.rect.x += dx

        for muur in muren:

            if self.rect.colliderect(muur):

                self.rect.x -= dx

    def beweeg_verticaal(
        self,
        dy: int,
        muren: list[pygame.Rect]
    ) -> None:

        self.rect.y += dy

        for muur in muren:

            if self.rect.colliderect(muur):

                self.rect.y -= dy

    def blijf_in_scherm(self) -> None:

        self.rect.x = max(
            0,
            min(
                WIDTH - self.rect.width,
                self.rect.x
            )
        )

        self.rect.y = max(
            0,
            min(
                HEIGHT - self.rect.height,
                self.rect.y
            )
        )

    def teken(self) -> None:

        screen.blit(
            self.afbeelding,
            (self.rect.x - 12, self.rect.y - 12)
        )

# ==================================================
# VIJAND
# ==================================================

class Vijand:

    def __init__(
        self,
        x: int,
        y: int
    ):

        self.afbeelding = laad_afbeelding(
            r"assets\tractor_player.png",
            (VIJAND_GROOTTE, VIJAND_GROOTTE)
        )

        self.rect = pygame.Rect(
            x,
            y,
            60,
            60
        )

        self.snelheid = VIJAND_SNELHEID

    def beweeg(
        self,
        speler: Speler
    ) -> None:

        vx = (
            speler.rect.centerx -
            self.rect.centerx
        )

        vy = (
            speler.rect.centery -
            self.rect.centery
        )

        afstand = math.hypot(vx, vy)

        if afstand != 0:

            vx /= afstand

            vy /= afstand

        self.rect.x += int(vx * self.snelheid)

        self.rect.y += int(vy * self.snelheid)

    def teken(self) -> None:

        screen.blit(
            self.afbeelding,
            (self.rect.x - 20, self.rect.y - 20)
        )

# ==================================================
# MELKFLES
# ==================================================

class Melkfles:

    def __init__(
        self,
        muren: list[pygame.Rect]
    ):

        self.afbeelding = laad_afbeelding(
            r"assets\milk.png",
            (MELKFLES_GROOTTE, MELKFLES_GROOTTE)
        )

        self.rect = self.genereer_positie(muren)

    def genereer_positie(
        self,
        muren: list[pygame.Rect]
    ) -> pygame.Rect:

        while True:

            x = random.randint(80, WIDTH - 80)

            y = random.randint(80, HEIGHT - 80)

            rect = pygame.Rect(x, y, 30, 30)

            geblokkeerd = False

            for muur in muren:

                if rect.colliderect(muur):

                    geblokkeerd = True

            if not geblokkeerd:

                return rect

    def teken(self) -> None:

        screen.blit(
            self.afbeelding,
            self.rect
        )

# ==================================================
# SPEL
# ==================================================

class Spel:

    def __init__(self):

        self.running = True

        self.game_over = False

        self.gewonnen = False

        self.spel_gestart = False

        self.level = 1

        self.score = 0

        self.map_manager = MapManager()

        self.speler = Speler(500, 760)

        self.vijand = Vijand(500, 100)

        self.startscherm = laad_afbeelding(
            r"assets\Startscherm.png",
            (WIDTH, HEIGHT)
        )

        self.tung_geluid = pygame.mixer.Sound(
            r"assets\The Tung.mp3"
        )

        self.melkflessen = []

        self.maak_melkflessen(10)

    # ==============================================
    # STARTSCHERM
    # ==============================================

    def teken_startscherm(self) -> None:

        screen.blit(self.startscherm, (0, 0))

        titel = grote_font.render(
            "VIDEOGAME 1",
            True,
            WIT
        )

        tekst = font.render(
            "Druk op SPATIE om te starten",
            True,
            WIT
        )

        screen.blit(titel, (220, 100))

        screen.blit(tekst, (180, 750))

        pygame.display.flip()

    # ==============================================
    # MELKFLESSEN
    # ==============================================

    def maak_melkflessen(
        self,
        aantal: int
    ) -> None:

        self.melkflessen.clear()

        for _ in range(aantal):

            self.melkflessen.append(
                Melkfles(
                    self.map_manager.muren
                )
            )

    # ==============================================
    # LEVEL 2
    # ==============================================

    def start_level_2(self) -> None:

        self.level = 2

        speel_video(
            r"assets\Aura of T.mp4",
            r"assets\muziek.mp3"
        )

        pygame.mixer.music.stop()

        pygame.mixer.music.load(
            r"assets\All Of The Lights.mp3"
        )

        pygame.mixer.music.play(-1)

        self.map_manager.start_level_2()

        self.speler.afbeelding = laad_afbeelding(
            r"assets\Kirk.png",
            (SPELER_GROOTTE, SPELER_GROOTTE)
        )

        self.vijand.afbeelding = laad_afbeelding(
            r"assets\olive delights.png",
            (100, 100)
        )

        self.vijand.snelheid = 4

        self.speler.rect.x = 100
        self.speler.rect.y = 100

        self.vijand.rect.x = 850
        self.vijand.rect.y = 850

        self.maak_melkflessen(15)

    # ==============================================
    # UPDATE
    # ==============================================

    def update(self) -> None:

        if self.game_over or self.gewonnen:

            return

        self.update_speler()

        self.update_vijand()

        self.check_melkflessen()

        self.check_level()

        self.check_game_over()

    def update_speler(self) -> None:

        self.speler.beweeg(
            self.map_manager.muren
        )

    def update_vijand(self) -> None:

        self.vijand.beweeg(self.speler)

    def check_melkflessen(self) -> None:

        for fles in self.melkflessen[:]:

            if self.speler.rect.colliderect(
                fles.rect
            ):

                self.melkflessen.remove(fles)

                self.score += 25

                self.tung_geluid.play()

    def check_level(self) -> None:

        if len(self.melkflessen) != 0:

            return

        if self.level == 1:

            self.start_level_2()

        else:

            self.gewonnen = True

    def check_game_over(self) -> None:

        if self.speler.rect.colliderect(
            self.vijand.rect
        ):

            self.game_over = True

    # ==============================================
    # TEKENEN
    # ==============================================

    def teken(self) -> None:

        screen.blit(
            self.map_manager.achtergrond,
            (0, 0)
        )

        self.teken_objecten()

        self.teken_ui()

        self.teken_eindscherm()

        pygame.display.flip()

    def teken_objecten(self) -> None:

        for fles in self.melkflessen:

            fles.teken()

        self.speler.teken()

        self.vijand.teken()

    def teken_ui(self) -> None:

        score_tekst = font.render(
            f"Score: {self.score}",
            True,
            WIT
        )

        level_tekst = font.render(
            f"Level: {self.level}",
            True,
            GEEL
        )

        screen.blit(score_tekst, (20, 20))

        screen.blit(level_tekst, (20, 70))

    def teken_eindscherm(self) -> None:

        if self.game_over:

            tekst = grote_font.render(
                "GAME OVER",
                True,
                ROOD
            )

            restart_tekst = font.render(
                "Druk op R om opnieuw te spelen",
                True,
                WIT
            )

            screen.blit(tekst, (230, 350))

            screen.blit(restart_tekst, (180, 450))

        if self.gewonnen:

            tekst = grote_font.render(
                "JE HEBT GEWONNEN!",
                True,
                GEEL
            )

            afsluit_tekst = font.render(
                "Druk op ENTER om af te sluiten",
                True,
                WIT
            )

            screen.blit(tekst, (120, 350))

            screen.blit(afsluit_tekst, (170, 450))

    # ==============================================
    # EVENTS
    # ==============================================

    def handle_events(self) -> None:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                self.running = False

            if event.type == pygame.KEYDOWN:

                # START SPEL
                if event.key == pygame.K_SPACE:

                    if not self.spel_gestart:

                        self.spel_gestart = True

                        speel_video(
                            r"assets\ANTON 5sec.mp4",
                            r"assets\muziek.mp3"
                        )

                        pygame.mixer.music.play(-1)

                # RESTART
                if event.key == pygame.K_r:

                    if self.game_over:

                        self.restart()

                # AFSLUITEN
                if event.key == pygame.K_RETURN:

                    if self.gewonnen:

                        self.running = False

    # ==============================================
    # RESTART
    # ==============================================

    def restart(self) -> None:

        self.__init__()

    # ==============================================
    # GAME LOOP
    # ==============================================

    def run(self) -> None:

        while self.running:

            clock.tick(FPS)

            self.handle_events()

            if self.spel_gestart:

                self.update()

                self.teken()

            else:

                self.teken_startscherm()

        pygame.quit()

# ==================================================
# START SPEL
# ==================================================

if __name__ == "__main__":

    spel = Spel()

    spel.run()