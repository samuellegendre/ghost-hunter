import pyglet
from pyglet.window import key

import config
import resources
from lib.publisher import Publisher


class Scoreboard:
    # Static data
    EVENT_RETURN_WELCOME = "EVENT_RETURN_WELCOME"

    # Public defs
    def __init__(self):
        self._reset()

    # - Behaviors or handlers or listeners -
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ENTER:
            self._publisher.dispatch(self.EVENT_RETURN_WELCOME)

    # - Utils -
    def get_publisher(self):
        return self._publisher

    def get_batch(self):
        return self._batch

    def get_handlers(self):
        return self._handlers

    def set_highest_score(self, _highest_score):
        self._highest_score = _highest_score

    def set_score(self, _score):
        self._score = _score

    def update_labels(self):
        self._highest_score_label.text = config.HIGHEST_SCORE_LABEL.format(self._highest_score)
        self._score_label.text = config.SCORE_LABEL.format(self._score)

    # Private defs
    def _reset(self):
        # Dynamic data

        self._publisher = Publisher([self.EVENT_RETURN_WELCOME])
        self._batch = pyglet.graphics.Batch()
        self._highest_score = 0
        self._score = 0

        # Background
        self._background_group = pyglet.graphics.OrderedGroup(0)
        self._background = pyglet.sprite.Sprite(img=resources.background_image, x=0, y=0,
                                                batch=self._batch, group=self._background_group)
        self._ground = pyglet.sprite.Sprite(img=resources.ground_image, x=0, y=0, batch=self._batch,
                                            group=self._background_group)

        # Foreground
        self._foreground_group = pyglet.graphics.OrderedGroup(1)
        self._foreground = pyglet.sprite.Sprite(img=resources.foreground_image, x=0, y=0, batch=self._batch,
                                                group=self._foreground_group)

        # HUD
        self._hud_group = pyglet.graphics.OrderedGroup(2)
        self._game_label = pyglet.text.Label(config.DEATH_LABEL, font_size=30, x=config.WINDOW_WIDTH // 2,
                                             y=config.WINDOW_HEIGHT // 8 * 6, anchor_x="center", anchor_y="center",
                                             batch=self._batch, group=self._hud_group)
        self._highest_score_label = pyglet.text.Label(config.HIGHEST_SCORE_LABEL.format(self._highest_score),
                                                      font_size=18, x=config.WINDOW_WIDTH / 2,
                                                      y=config.WINDOW_HEIGHT / 8 * 4.5, anchor_x="center",
                                                      anchor_y="center", batch=self._batch, group=self._hud_group)
        self._score_label = pyglet.text.Label(config.SCORE_LABEL.format(self._score),
                                              font_size=18, x=config.WINDOW_WIDTH / 2,
                                              y=config.WINDOW_HEIGHT / 8 * 4, anchor_x="center",
                                              anchor_y="center", batch=self._batch, group=self._hud_group)
        self._start_label = pyglet.text.Label(config.SCOREBOARD_LABEL, font_size=18,
                                              x=config.WINDOW_WIDTH // 2, y=config.WINDOW_HEIGHT // 8,
                                              anchor_x="center",
                                              anchor_y="center", batch=self._batch, group=self._hud_group)

        self._handlers = [self]
