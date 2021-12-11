import pyglet.sprite

from config import OBJECT_DEFAULT_SPEED_X
from utils import util


class Object(pyglet.sprite.Sprite):
    # Public defs
    def __init__(self, *args, **kwargs):
        super(Object, self).__init__(*args, **kwargs)

        self.dead = False
        self.is_obstacle = False
        self.is_projectile = False
        self.new_objects = []
        self.reacts_to_obstacle = True
        self.reacts_to_projectile = True
        self.rectangle = pyglet.shapes.Rectangle(x=self.x, y=self.y, width=self.width, height=self.height)
        self.rectangle.anchor_x = self.width / 2
        self.rectangle.anchor_y = self.height / 2
        self.speed_x = OBJECT_DEFAULT_SPEED_X
        self.y += self.height / 2

    def update(self, dt):
        self.rectangle.position = self.position

    def collides_with(self, _object):
        if not self.reacts_to_projectile and _object.is_projectile:
            return False
        if self.is_projectile and not _object.reacts_to_projectile:
            return False
        if not self.reacts_to_obstacle and _object.is_obstacle:
            return False
        if self.is_obstacle and not _object.reacts_to_obstacle:
            return False

        self_rect = util.get_rectangle(self.rectangle)
        object_rect = util.get_rectangle(_object.rectangle)
        self_xs = sorted(xy[0] for xy in self_rect)
        self_ys = sorted(xy[1] for xy in self_rect)
        object_xs = sorted(xy[0] for xy in object_rect)
        object_ys = sorted(xy[1] for xy in object_rect)

        if self_xs[0] <= object_xs[-1] and self_xs[-1] >= object_xs[0]:
            if self_ys[0] <= object_ys[-1] and self_ys[-1] >= object_ys[0]:
                return True

        return False

    def handle_collision_with(self, _object):
        if _object.__class__ == self.__class__:
            self.dead = False
        else:
            self.dead = True
