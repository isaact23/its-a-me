from mode import Mode
from colors import *
from settings import *
from sounds import SoundPlayer
from rule import Rule


# Mode 100 - Superclass for attract modes
class Mode100(Mode):
    def __init__(self, controller, grid, screen):
        super().__init__(controller, grid, screen)

        self.image_cloud = pygame.image.load(str(IMAGE_DIR / 'lakitu.png')).convert()
        self.image_cloud = pygame.transform.scale(self.image_cloud, (800, 800))

        # Render cloud GUI
        self.screen.fill(WHITE)
        self.screen.blit(self.image_cloud, (550, 100))
        pygame.display.update()

        # Play attract music
        self.sound_player.set_mode(SoundPlayer.Mode.ATTRACT)

        # Railings are red/orange moving stripes in intro
        self.grid.get_seg(0).set_rule(Rule().stripes((RED, WHITE, BLUE), width=8).animate(10).fade_in(2, 1))
        self.grid.get_seg(1).set_rule(Rule().stripes((RED, WHITE, BLUE), width=8).animate(10).fade_in(2, 1))

    def update(self, pressed_keys):
        if pressed_keys[KEY_START]:
            print("Starting!")
            return Mode200(self.controller, self.grid, self.screen)

        return super().update(pressed_keys)
