import pyglet.clock

import config
import resources
from lib.publisher import Publisher


class PlayerFiringState:
    # Static data
    EVENT_PLAYER_MOVES_BACKWARD = "EVENT_PLAYER_MOVES_BACKWARD"
    EVENT_PLAYER_MOVES_FORWARD = "EVENT_PLAYER_MOVES_FORWARD"
    EVENT_PLAYER_STOPPED_FIRING = "EVENT_PLAYER_STOPPED_FIRING"

    # Public defs
    def __init__(self, _player, _key_handler):
        self._key_handler = _key_handler
        self._player = _player
        self._publisher = Publisher(
            [self.EVENT_PLAYER_STOPPED_FIRING, self.EVENT_PLAYER_MOVES_FORWARD, self.EVENT_PLAYER_MOVES_BACKWARD])

    def update(self, dt):
        pass

    def start(self):
        try:
            pyglet.clock.schedule_once(self.stop, 0.65)
            self._player.image = resources.player_attacking_animation
        except:
            pass

    def stop(self, dt):
        try:
            if self._key_handler[config.PLAYER_MOVE_FORWARD_KEY]:
                self._publisher.dispatch(self.EVENT_PLAYER_MOVES_FORWARD)
            elif self._key_handler[config.PLAYER_MOVE_BACKWARD_KEY]:
                self._publisher.dispatch(self.EVENT_PLAYER_MOVES_BACKWARD)
            else:
                self._publisher.dispatch(self.EVENT_PLAYER_STOPPED_FIRING)
        except:
            pass

    # - Behaviors or handlers or listeners -
    def on_key_press(self, symbol, modifier):
        pass

    def on_key_release(self, symbol, modifier):
        pass

    # - Utils -
    def get_publisher(self):
        return self._publisher
