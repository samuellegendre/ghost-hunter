from config import GROUND_LEVEL, GRAVITY
from objects.object import Object


class GravitationalObject(Object):
    # Public defs
    def __init__(self, *args, **kwargs):
        super(GravitationalObject, self).__init__(*args, **kwargs)

    def update(self, dt):
        super(GravitationalObject, self).update(dt)

        if self.y > GROUND_LEVEL + self.height / 2:
            self.y -= GRAVITY * dt
        else:
            self.y = GROUND_LEVEL + self.height / 2
