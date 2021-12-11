import resources
from config import GHOST_NUMBER_HITS
from objects.gravitational_object import GravitationalObject


class Ghost(GravitationalObject):
    # Public defs
    def __init__(self, *args, **kwargs):
        super(Ghost, self).__init__(img=resources.ghost_idle_animation, *args, **kwargs)

        self.hits = GHOST_NUMBER_HITS
        self.reacts_to_obstacle = False

    def update(self, dt):
        super(Ghost, self).update(dt)

        self.x -= self.speed_x * dt
