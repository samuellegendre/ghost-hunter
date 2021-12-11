import config
import resources
from lib.publisher import Publisher


class PlayerIdleState:
    # Static data
    EVENT_PLAYER_FIRES = "EVENT_PLAYER_FIRES"
    EVENT_PLAYER_JUMPS = "EVENT_PLAYER_JUMPS"
    EVENT_PLAYER_MOVES_BACKWARD = "EVENT_PLAYER_MOVES_BACKWARD"
    EVENT_PLAYER_MOVES_FORWARD = "EVENT_PLAYER_MOVES_FORWARD"

    # Public defs
    def __init__(self, _player):
        self._player = _player
        self._publisher = Publisher(
            [self.EVENT_PLAYER_MOVES_FORWARD, self.EVENT_PLAYER_MOVES_BACKWARD, self.EVENT_PLAYER_JUMPS,
             self.EVENT_PLAYER_FIRES])

    def update(self, dt):
        pass

    def start(self):
        try:
            self._player.image = resources.player_idle_animation
        except:
            pass

    # - Behaviors or handlers or listeners -
    def on_key_press(self, symbol, modifier):
        if symbol == config.PLAYER_MOVE_FORWARD_KEY:  # Moving forward
            self._publisher.dispatch(self.EVENT_PLAYER_MOVES_FORWARD)

        elif symbol == config.PLAYER_MOVE_BACKWARD_KEY:  # Moving backward
            self._publisher.dispatch(self.EVENT_PLAYER_MOVES_BACKWARD)

        elif symbol == config.PLAYER_JUMP_KEY:  # Jumping
            self._publisher.dispatch(self.EVENT_PLAYER_JUMPS)

        elif symbol == config.PLAYER_FIRE_KEY:  # Firing
            self._publisher.dispatch(self.EVENT_PLAYER_FIRES)

    def on_key_release(self, symbol, modifier):
        pass

    # - Utils -
    def get_publisher(self):
        return self._publisher
