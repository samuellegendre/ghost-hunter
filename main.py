import pyglet.window

import config
from config import FPS
from game_states.game import Game
from game_states.scoreboard import Scoreboard
from game_states.welcome import Welcome
from window import Window


class Main:
    # Public defs
    def __init__(self):
        self._reset()

    def start(self):
        pyglet.app.run()

    # - Behaviors or handlers or listeners -
    def _on_welcome_start_game(self):
        self._set_next_state()
        pyglet.clock.schedule_interval(self._game.update, 1 / FPS)

    def _on_game_end(self):
        pyglet.clock.unschedule(self._game.update)
        self.save_score(self._game.get_score())
        self._scoreboard.set_score(self._game.get_score())
        self._scoreboard.set_highest_score(self.get_highest_score())
        self._scoreboard.update_labels()
        self._game.__init__()
        self._listen_to_events()
        self._set_next_state()

    def _on_scoreboard_return_welcome(self):
        self._set_next_state()

    def _listen_to_events(self):
        self._welcome.get_publisher().register(self._welcome.EVENT_START_GAME, self, self._on_welcome_start_game)
        self._game.get_publisher().register(self._game.EVENT_GAME_END, self, self._on_game_end)
        self._game.get_publisher().register(self._game.EVENT_LEVEL_RESET, self, self._listen_to_handlers)
        self._scoreboard.get_publisher().register(self._scoreboard.EVENT_RETURN_WELCOME, self,
                                                  self._on_scoreboard_return_welcome)

    # Shunting or routing or wiring
    def _listen_to_handlers(self):
        self._window.remove_handlers()

        for handler in self._state.get_handlers():
            self._window.push_handlers(handler)

    # - Utils -
    def _reset(self):
        # Dynamic data

        self._window = Window()
        self._welcome = Welcome()
        self._game = Game()
        self._scoreboard = Scoreboard()
        self._set_state(self._welcome)
        self._next_states = dict()
        self._next_states[self._welcome] = self._game  # welcome -> game
        self._next_states[self._game] = self._scoreboard  # game -> scoreboard
        self._next_states[self._scoreboard] = self._welcome  # scoreboard -> welcome
        self._listen_to_events()

    def _set_state(self, state):
        self._state = state
        self._listen_to_handlers()
        self._window.set_batch(self._get_state().get_batch())

    def _get_state(self):
        return self._state

    def _set_next_state(self):
        self._window.remove_handlers(self._get_state())
        self._set_state(self._next_states[self._get_state()])

    def save_score(self, _score: int):
        if self.get_highest_score() < _score:
            with open(config.SCORE_FILE_NAME, "w") as file:
                file.write(str(_score))

    def get_highest_score(self):
        try:
            with open(config.SCORE_FILE_NAME, "r") as file:
                return int(file.read())
        except:
            return 0
