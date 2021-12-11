import pyglet

import config
import resources
from lib.publisher import Publisher
from objects.ghost import Ghost
from objects.player import Player
from objects.projectile import Projectile
from objects.wolf import Wolf
from utils import util
from utils.load import player_lives, enemies


class Game:
    # Static data
    EVENT_GAME_END = "EVENT_GAME_END"
    EVENT_LEVEL_RESET = "EVENT_LEVEL_RESET"

    # Public defs
    def __init__(self):
        self._reset()

    def update(self, dt):
        _is_player_dead = False

        self._score_label.x = self._player.x

        for i in range(len(self._game_objects)):
            for j in range(i + 1, len(self._game_objects)):
                _object_1 = self._game_objects[i]
                _object_2 = self._game_objects[j]

                if not _object_1.dead and not _object_2.dead:
                    if _object_1.collides_with(_object_2):
                        if isinstance(_object_1, Projectile) and isinstance(_object_2, Ghost):
                            _object_1.handle_collision_with(_object_2)
                            if _object_2.hits > 1:
                                _object_2.hits -= 1
                            else:
                                _object_2.handle_collision_with(_object_1)
                        elif isinstance(_object_2, Projectile) and isinstance(_object_1, Ghost):
                            _object_2.handle_collision_with(_object_1)
                            if _object_1.hits > 1:
                                _object_1.hits -= 1
                            else:
                                _object_1.handle_collision_with(_object_2)
                        else:
                            _object_1.handle_collision_with(_object_2)
                            _object_2.handle_collision_with(_object_1)
        _objects_to_add = []

        for _object in self._game_objects:
            _object.update(dt)
            _objects_to_add.extend(_object.new_objects)
            _object.new_objects = []

            if isinstance(_object, (Ghost, Wolf)):
                self._difficulty_multiplier += config.DIFFICULTY_MULTIPLIER
                _object.speed_x += config.DIFFICULTY_MULTIPLIER

        for _object_removing in [_object for _object in self._game_objects if _object.dead]:
            if _object_removing == self._player:
                _is_player_dead = True

            _object_removing.delete()
            self._game_objects.remove(_object_removing)

            if isinstance(_object_removing, Ghost) and not _is_player_dead:
                self._score += config.SCORE_EARNED_PER_KILL
                self._score_label.text = str(round(self._score))
                self._enemies = enemies(self._batch, self._middleground_group, self._difficulty_multiplier)
                self._game_objects += self._enemies

        self._game_objects.extend(_objects_to_add)

        if _is_player_dead:
            if len(self._player_lives) > 1:
                for _object in self._game_objects:
                    _object.delete()
                self._reset_level(len(self._player_lives) - 1)
            else:
                self._publisher.dispatch(self.EVENT_GAME_END)

    # - Behaviors or handlers or listeners -
    def on_player_moves_forward(self):
        self._score += 0.1
        self._score_label.text = str(round(self._score))

        for i in self._game_objects:
            if isinstance(i, (Ghost, Wolf)):
                i.x -= self._player.speed_x

        self._background.x -= config.PLAYER_SPEED_X / 7
        self._foreground.x -= config.PLAYER_SPEED_X
        self._ground.x -= config.PLAYER_SPEED_X
        self._repeated_background.x -= config.PLAYER_SPEED_X / 7
        self._repeated_foreground.x -= config.PLAYER_SPEED_X
        self._repeated_ground.x -= config.PLAYER_SPEED_X
        util.check_bounds(self._background)
        util.check_bounds(self._foreground)
        util.check_bounds(self._ground)
        util.check_bounds(self._repeated_background)
        util.check_bounds(self._repeated_foreground)
        util.check_bounds(self._repeated_ground)

    def on_player_moves_backward(self):
        self._score -= 0.1
        self._score_label.text = str(round(self._score))

        for i in self._game_objects:
            if isinstance(i, (Ghost, Wolf)):
                i.x += self._player.speed_x

        self._background.x += config.PLAYER_SPEED_X / 7
        self._foreground.x += config.PLAYER_SPEED_X
        self._ground.x += config.PLAYER_SPEED_X
        self._repeated_background.x += config.PLAYER_SPEED_X / 7
        self._repeated_foreground.x += config.PLAYER_SPEED_X
        self._repeated_ground.x += config.PLAYER_SPEED_X
        util.check_bounds(self._background)
        util.check_bounds(self._foreground)
        util.check_bounds(self._ground)
        util.check_bounds(self._repeated_background)
        util.check_bounds(self._repeated_foreground)
        util.check_bounds(self._repeated_ground)

    def _listen_to_events(self):
        self._player.get_player_moving_forward_state().get_publisher().register(
            self._player.get_player_moving_forward_state().EVENT_PLAYER_MOVES_FORWARD, self,
            self.on_player_moves_forward)
        self._player.get_player_moving_backward_state().get_publisher().register(
            self._player.get_player_moving_backward_state().EVENT_PLAYER_MOVES_BACKWARD, self,
            self.on_player_moves_backward)
        self._player.get_player_jumping().get_publisher().register(
            self._player.get_player_jumping().EVENT_PLAYER_MOVES_OUTSIDE_BORDERS, self,
            self.on_player_moves_forward)

    # - Utils -

    def get_publisher(self):
        return self._publisher

    def get_batch(self):
        return self._batch

    def get_handlers(self):
        return self._handlers

    def get_score(self):
        return round(self._score)

    # Private defs

    def _reset(self):
        # Dynamic data

        self._publisher = Publisher([self.EVENT_GAME_END, self.EVENT_LEVEL_RESET])
        self._batch = pyglet.graphics.Batch()

        # Background
        self._background_group = pyglet.graphics.OrderedGroup(0)
        self._background = pyglet.sprite.Sprite(img=resources.background_image, x=0, y=0,
                                                batch=self._batch, group=self._background_group)
        self._repeated_background = pyglet.sprite.Sprite(img=resources.background_image, x=self._background.width, y=0,
                                                         batch=self._batch, group=self._background_group)
        self._ground = pyglet.sprite.Sprite(img=resources.ground_image, x=0, y=0, batch=self._batch,
                                            group=self._background_group)
        self._repeated_ground = pyglet.sprite.Sprite(img=resources.ground_image, x=self._ground.width, y=0,
                                                     batch=self._batch,
                                                     group=self._background_group)

        # Middle ground
        self._middleground_group = pyglet.graphics.OrderedGroup(1)

        # Foreground
        self._foreground_group = pyglet.graphics.OrderedGroup(2)
        self._foreground = pyglet.sprite.Sprite(img=resources.foreground_image, x=0, y=0, batch=self._batch,
                                                group=self._foreground_group)
        self._repeated_foreground = pyglet.sprite.Sprite(img=resources.foreground_image, x=self._foreground.width, y=0,
                                                         batch=self._batch,
                                                         group=self._foreground_group)

        # HUD
        self._hud_group = pyglet.graphics.OrderedGroup(3)
        self._score = 0
        self._score_label = pyglet.text.Label(text=str(self._score), x=0, y=config.GROUND_LEVEL / 2 - 4,
                                              batch=self._batch, group=self._hud_group, anchor_y="center", font_size=18,
                                              color=(207, 207, 207, 81))
        self._player_lives = []

        self._player = Player()

        self._reset_level(config.PLAYER_LIVES)

    def _reset_level(self, _number_hearts):
        self._difficulty_multiplier = 0

        for _heart in self._player_lives:
            _heart.delete()

        self._player.__init__(x=config.WINDOW_WIDTH // 8, y=config.GROUND_LEVEL, batch=self._batch,
                              group=self._middleground_group)
        self._handlers = [self, self._player, self._player.get_key_handler()]
        self._listen_to_events()

        self._enemies = enemies(self._batch, self._middleground_group, self._difficulty_multiplier)

        self._player_lives = player_lives(_number_hearts, self._batch, self._hud_group)

        self._game_objects = [self._player] + self._enemies
        self._publisher.dispatch(self.EVENT_LEVEL_RESET)
