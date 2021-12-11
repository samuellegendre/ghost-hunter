import random

import pyglet.sprite

import config
import resources
from objects.ghost import Ghost
from objects.wolf import Wolf


def player_lives(_number_hearts, _batch, _group):
    _player_lives = []

    for i in range(_number_hearts):
        _sprite = pyglet.sprite.Sprite(img=resources.heart_image, x=0 + i * 40,
                                       y=config.WINDOW_HEIGHT,
                                       batch=_batch, group=_group)
        _sprite.scale = 0.15

        _player_lives.append(_sprite)

    return _player_lives


def enemies(_batch, _group, _difficulty_multiplier):
    _enemies = []

    _ghost_x = random.randint(config.WINDOW_WIDTH + 100, config.WINDOW_WIDTH + 600)
    _wolf_x = random.randint(config.WINDOW_WIDTH + 400, config.WINDOW_WIDTH + 800)
    _y = config.GROUND_LEVEL

    _ghost = Ghost(x=_ghost_x, y=config.GROUND_LEVEL, batch=_batch, group=_group)
    _ghost.speed_x += _difficulty_multiplier
    _wolf = Wolf(x=_wolf_x, y=config.GROUND_LEVEL, batch=_batch, group=_group)
    _wolf.speed_x += _difficulty_multiplier

    _enemies.append(_ghost)
    _enemies.append(_wolf)

    return _enemies
