import abc
import random

from backgammon import roll_dice, generate_moves
from utils import to_backgammon_color


class Agent(abc.ABC):
    @abc.abstractmethod
    def step(self, board):
        pass

    @abc.abstractmethod
    def update_model(self, board):
        pass


class RandomAgent(Agent):
    def __init__(self, player):
        self._player = player

    def step(self, board):
        rolls = roll_dice()

        available_moves = generate_moves(board, rolls, to_backgammon_color(self._player))
        move_index = random.randint(0, len(available_moves) - 1)
        return available_moves[move_index]

    def update_model(self, board):
        pass


class TDGammonAgent(Agent):
    def __init__(self, model, player):
        self._model = model
        self._player = player

    def step(self, board):
        rolls = roll_dice()
        return self._model.action(board, rolls, self._player)

    def update_model(self, board):
        self._model.update_weights(board, self._player)
