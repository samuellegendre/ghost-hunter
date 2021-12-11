import config
import resources
from lib.publisher import Publisher


class PlayerJumpingState:
    # Static data
    EVENT_PLAYER_MOVES_BACKWARD = "EVENT_PLAYER_MOVES_BACKWARD"
    EVENT_PLAYER_MOVES_FORWARD = "EVENT_PLAYER_MOVES_FORWARD"
    EVENT_PLAYER_MOVES_OUTSIDE_BORDERS = "EVENT_PLAYER_MOVES_OUTSIDE_BORDERS"
    EVENT_PLAYER_ON_GROUND = "EVENT_PLAYER_ON_GROUND"

    # Public defs
    def __init__(self, _player, _key_handler):
        self._key_handler = _key_handler
        self._player = _player
        self._publisher = Publisher(
            [self.EVENT_PLAYER_ON_GROUND, self.EVENT_PLAYER_MOVES_FORWARD, self.EVENT_PLAYER_MOVES_BACKWARD,
             self.EVENT_PLAYER_MOVES_OUTSIDE_BORDERS])

    def update(self, dt):
        if self._player.y == config.GROUND_LEVEL + self._player.height / 2:
            if self._key_handler[config.PLAYER_MOVE_FORWARD_KEY]:
                self._publisher.dispatch(self.EVENT_PLAYER_MOVES_FORWARD)
            elif self._key_handler[config.PLAYER_MOVE_BACKWARD_KEY]:
                self._publisher.dispatch(self.EVENT_PLAYER_MOVES_BACKWARD)
            else:
                self._publisher.dispatch(self.EVENT_PLAYER_ON_GROUND)

        if self._key_handler[config.PLAYER_MOVE_FORWARD_KEY]:
            if self._player.x <= config.WINDOW_WIDTH // 8 * 4:
                self._player.x += config.PLAYER_SPEED_X
            else:
                self._publisher.dispatch(self.EVENT_PLAYER_MOVES_OUTSIDE_BORDERS)

    def start(self):
        try:
            self._player.image = resources.player_falling_animation
            self._player.y += config.PLAYER_JUMP_HEIGHT
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
