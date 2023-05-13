import random

from backgammon import init_board, game_result
from utils import to_backgammon_color


class Game:
    def __init__(self, agent1, agent2):
        self._agents = [agent1, agent2]
        self._board = init_board()

    def play(self):
        player = random.randint(0, 1)

        while not game_result(self._board)[1] == to_backgammon_color(player):
            player = 1 - player
            self._board = self._agents[player].step(self._board)
            self._agents[player].update_model(self._board)
