from mode100 import Mode100


# Mode 101 - Attract sequence mode 1
class Mode101(Mode100):
    def __init__(self, controller, grid, screen):
        super().__init__(controller, grid, screen)

    def update(self, pressed_keys):
        super().update(pressed_keys)
