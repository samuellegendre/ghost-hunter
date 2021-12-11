import resources
from config import WOLF_SPEED_X
from objects.gravitational_object import GravitationalObject


class Wolf(GravitationalObject):
    def __init__(self, *args, **kwargs):
        super(Wolf, self).__init__(img=resources.wolf_running, *args, **kwargs)

        self.is_obstacle = True
        self.reacts_to_projectile = False
        self.speed_x = WOLF_SPEED_X

    def update(self, dt):
        super(Wolf, self).update(dt)

        self.x -= self.speed_x * dt
        if self.x < 0 - self.width / 2:
            self.dead = True
