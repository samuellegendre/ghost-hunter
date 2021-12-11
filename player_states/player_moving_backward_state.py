import config
import resources
from lib.publisher import Publisher


class PlayerMovingBackwardState:
    # Static data
    EVENT_PLAYER_FIRES = "EVENT_PLAYER_FIRES"
    EVENT_PLAYER_MOVES_BACKWARD = "EVENT_PLAYER_MOVES_BACKWARD"
    EVENT_PLAYER_MOVES_FORWARD = "EVENT_PLAYER_MOVES_FORWARD"
    EVENT_PLAYER_STOPPED_MOVING = "EVENT_PLAYER_STOPPED_MOVING"

    # Public defs
    def __init__(self, _player):
        self._player = _player
        self._publisher = Publisher(
            [self.EVENT_PLAYER_STOPPED_MOVING, self.EVENT_PLAYER_MOVES_FORWARD, self.EVENT_PLAYER_FIRES,
             self.EVENT_PLAYER_MOVES_BACKWARD])

    def update(self, dt):
        if self._player.x > self._player.width:
            self._player.x -= config.PLAYER_SPEED_X
        else:
            self._publisher.dispatch(self.EVENT_PLAYER_MOVES_BACKWARD)

    def start(self):
        try:
            self._player.image = resources.player_running_backward_animation
        except:
            pass

    # - Behaviors or handlers or listeners -
    def on_key_press(self, symbol, modifier):
        if symbol == config.PLAYER_MOVE_FORWARD_KEY:
            self._publisher.dispatch(self.EVENT_PLAYER_MOVES_FORWARD)
        elif symbol == config.PLAYER_FIRE_KEY:
            self._publisher.dispatch(self.EVENT_PLAYER_FIRES)

    def on_key_release(self, symbol, modifier):
        if symbol == config.PLAYER_MOVE_BACKWARD_KEY:
            self._publisher.dispatch(self.EVENT_PLAYER_STOPPED_MOVING)

    # - Utils -
    def get_publisher(self):
        return self._publisher
