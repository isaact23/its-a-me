from mode import Mode
from mode100 import Mode100
from mode101 import Mode101
from mode102 import Mode102
from mode103 import Mode103
from mode104 import Mode104
from mode105 import Mode105
from mode200 import Mode200


# Get mode by mode number.
def get_mode(mode, controller, grid, screen):
    if mode == 100:
        return Mode100(controller, grid, screen)
    elif mode == 101:
        return Mode101(controller, grid, screen)
    elif mode == 102:
        return Mode102(controller, grid, screen)
    elif mode == 103:
        return Mode103(controller, grid, screen)
    elif mode == 104:
        return Mode104(controller, grid, screen)
    elif mode == 105:
        return Mode105(controller, grid, screen)
    elif mode == 200:
        return Mode200(controller, grid, screen)
