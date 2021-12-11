from pyglet.window import key

import resources
from config import PLAYER_PROJECTILE_SPEED, PLAYER_SPEED_X
from lib.publisher import Publisher
from objects.gravitational_object import GravitationalObject
from objects.projectile import Projectile
from player_states.player_firing_state import PlayerFiringState
from player_states.player_idle_state import PlayerIdleState
from player_states.player_jumping_state import PlayerJumpingState
from player_states.player_moving_backward_state import PlayerMovingBackwardState
from player_states.player_moving_forward_state import PlayerMovingForwardState


class Player(GravitationalObject):
    # Static data
    EVENT_PLAYER_MOVES_BACKWARD = "EVENT_PLAYER_MOVES_BACKWARD"
    EVENT_PLAYER_MOVES_FORWARD = "EVENT_PLAYER_MOVES_FORWARD"

    # Public defs
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(img=resources.player_idle_animation, *args, **kwargs)

        self._can_fire = True
        self._can_jump = True
        self._fireball_speed = PLAYER_PROJECTILE_SPEED
        self._key_handler = key.KeyStateHandler()
        self._player_firing_state = PlayerFiringState(self, self._key_handler)
        self._player_idle_state = PlayerIdleState(self)
        self._player_jumping_state = PlayerJumpingState(self, self._key_handler)
        self._player_moving_backward_state = PlayerMovingBackwardState(self)
        self._player_moving_forward_state = PlayerMovingForwardState(self)
        self._publisher = Publisher([self.EVENT_PLAYER_MOVES_FORWARD, self.EVENT_PLAYER_MOVES_BACKWARD])
        self._set_state(self._player_idle_state)
        self.reacts_to_projectile = False
        self.speed_x = PLAYER_SPEED_X

        self._listen_to_events()

    def update(self, dt):
        super(Player, self).update(dt)

        self.state.update(dt)

    # - Behaviors or handlers or listeners -
    def on_player_moves_forward(self):
        self._set_state(self._player_moving_forward_state)

    def on_player_moves_backward(self):
        self._set_state(self._player_moving_backward_state)

    def on_player_idle(self):
        self._set_state(self._player_idle_state)

    def on_player_jumps(self):
        self._set_state(self._player_jumping_state)

    def on_player_firing(self):
        self._set_state(self._player_firing_state)
        self._fire()

    def on_key_press(self, symbol, modifier):
        try:
            self.state.on_key_press(symbol, modifier)
        except:
            pass

    def on_key_release(self, symbol, modifier):
        try:
            self.state.on_key_release(symbol, modifier)
        except:
            pass

    # - Utils -
    def get_key_handler(self):
        return self._key_handler

    def get_publisher(self):
        return self._publisher

    def get_player_moving_forward_state(self):
        return self._player_moving_forward_state

    def get_player_moving_backward_state(self):
        return self._player_moving_backward_state

    def get_player_jumping(self):
        return self._player_jumping_state

    def _set_state(self, _state):
        self.state = _state
        self.state.start()

    # Private defs
    def _fire(self):
        _fireball = Projectile(self.x + self.width // 4.7, self.y, batch=self.batch, group=self.group)
        _fireball.speed_x = self.speed_x + self._fireball_speed
        _fireball.scale = 0.8

        self.new_objects.append(_fireball)

    # - Utils -

    def _listen_to_events(self):
        # Firing
        self._player_firing_state.get_publisher().register(self._player_firing_state.EVENT_PLAYER_MOVES_BACKWARD, self,
                                                           self.on_player_moves_backward)
        self._player_firing_state.get_publisher().register(self._player_firing_state.EVENT_PLAYER_MOVES_FORWARD, self,
                                                           self.on_player_moves_forward)
        self._player_firing_state.get_publisher().register(self._player_firing_state.EVENT_PLAYER_STOPPED_FIRING, self,
                                                           self.on_player_idle)

        # Idle
        self._player_idle_state.get_publisher().register(self._player_idle_state.EVENT_PLAYER_FIRES, self,
                                                         self.on_player_firing)
        self._player_idle_state.get_publisher().register(self._player_idle_state.EVENT_PLAYER_JUMPS, self,
                                                         self.on_player_jumps)
        self._player_idle_state.get_publisher().register(self._player_idle_state.EVENT_PLAYER_MOVES_BACKWARD, self,
                                                         self.on_player_moves_backward)
        self._player_idle_state.get_publisher().register(self._player_idle_state.EVENT_PLAYER_MOVES_FORWARD, self,
                                                         self.on_player_moves_forward)

        # Jumping
        self._player_jumping_state.get_publisher().register(self._player_jumping_state.EVENT_PLAYER_ON_GROUND, self,
                                                            self.on_player_idle)
        self._player_jumping_state.get_publisher().register(self._player_jumping_state.EVENT_PLAYER_MOVES_FORWARD, self,
                                                            self.on_player_moves_forward)
        self._player_jumping_state.get_publisher().register(self._player_jumping_state.EVENT_PLAYER_MOVES_BACKWARD,
                                                            self, self.on_player_moves_backward)

        # Moving backward
        self._player_moving_backward_state.get_publisher().register(
            self._player_moving_backward_state.EVENT_PLAYER_MOVES_FORWARD, self, self.on_player_moves_forward)
        self._player_moving_backward_state.get_publisher().register(
            self._player_moving_backward_state.EVENT_PLAYER_STOPPED_MOVING, self, self.on_player_idle)
        self._player_moving_backward_state.get_publisher().register(
            self._player_moving_backward_state.EVENT_PLAYER_FIRES, self, self.on_player_firing)

        # Moving forward
        self._player_moving_forward_state.get_publisher().register(self._player_moving_forward_state.EVENT_PLAYER_FIRES,
                                                                   self, self.on_player_firing)
        self._player_moving_forward_state.get_publisher().register(self._player_moving_forward_state.EVENT_PLAYER_JUMPS,
                                                                   self, self.on_player_jumps)
        self._player_moving_forward_state.get_publisher().register(
            self._player_moving_forward_state.EVENT_PLAYER_MOVES_BACKWARD, self, self.on_player_moves_backward)
        self._player_moving_forward_state.get_publisher().register(
            self._player_moving_forward_state.EVENT_PLAYER_STOPPED_MOVING, self, self.on_player_idle)
