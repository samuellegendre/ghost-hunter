import pyglet.clock

import resources
from config import PLAYER_PROJECTILE_LIVING_TIME
from objects.object import Object


class Projectile(Object):
    # Public defs
    def __init__(self, *args, **kwargs):
        super(Projectile, self).__init__(resources.fireball_animation, *args, **kwargs)

        pyglet.clock.schedule_once(self._die, PLAYER_PROJECTILE_LIVING_TIME)
        self.is_projectile = True

    def update(self, dt):
        super(Projectile, self).update(dt)

        self.x += self.speed_x * dt

    # Private defs
    def _die(self, dt):
        self.dead = True
