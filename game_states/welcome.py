import pyglet.graphics

import config
import resources
from lib.publisher import Publisher


class Welcome:
    # Static data
    EVENT_START_GAME = "EVENT_START_GAME"

    # Public defs
    def __init__(self):
        self._reset()

    # - Behaviors or handlers or listeners -
    def on_key_press(self, symbol, modifiers):
        self._publisher.dispatch(self.EVENT_START_GAME)

    # - Utils -
    def get_publisher(self):
        return self._publisher

    def get_batch(self):
        return self._batch

    def get_handlers(self):
        return self._handlers

    # Private defs
    def _reset(self):
        # Dynamic data

        self._publisher = Publisher([self.EVENT_START_GAME])
        self._batch = pyglet.graphics.Batch()

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
        self._game_label = pyglet.text.Label(config.GAME_TITLE, font_size=30, x=config.WINDOW_WIDTH // 2,
                                             y=config.WINDOW_HEIGHT // 8 * 6, anchor_x="center", anchor_y="center",
                                             batch=self._batch, group=self._hud_group)
        self._start_label = pyglet.text.Label(config.WELCOME_LABEL, font_size=18,
                                              x=config.WINDOW_WIDTH // 2, y=config.WINDOW_HEIGHT // 8,
                                              anchor_x="center",
                                              anchor_y="center", batch=self._batch, group=self._hud_group)
        self._version_label = pyglet.text.Label(config.VERSION, batch=self._batch, group=self._hud_group)

        self._handlers = [self]
