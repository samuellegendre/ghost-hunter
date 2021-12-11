import pyglet.window

import config
import resources


class Window(pyglet.window.Window):
    # Public defs
    def __init__(self):
        super(Window, self).__init__(config.WINDOW_WIDTH, config.WINDOW_HEIGHT, caption=config.GAME_TITLE)
        self.set_icon(resources.icon_16_image, resources.icon_32_image)
        self._reset()

    # - Behaviors or handlers or listeners -
    def on_draw(self):
        self.clear()
        self._batch.draw()

    # - Utils -
    def set_batch(self, scene):
        self._batch = scene
        self.on_draw()

    # Private defs
    def _reset(self):
        # Dynamic data
        self._batch = pyglet.graphics.Batch()
