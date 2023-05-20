import numpy as np


def to_backgammon_color(color):
    return 1 if color == 1 else -1


def encode_state(board, player):
    state = np.zeros(196)

    for i in range(0, 24):
        checkers = board[i + 1]
        if checkers == 0:
            continue
        elif checkers == 1:
            state[i * 4] = 1
            continue
        elif checkers == 2:
            state[i * 4] = 1
            state[i * 4 + 1] = 1
            continue
        elif checkers > 0:
            state[i * 4] = 1
            state[i * 4 + 1] = 1
            state[i * 4 + 2] = 1
            state[i * 4 + 3] = (checkers - 3) / 12

    for i in range(0, 24):
        checkers = board[i + 1]
        if checkers == 0:
            continue
        elif checkers == -1:
            state[i * 4 + 96] = 1
            continue
        elif checkers == -2:
            state[i * 4 + 96] = 1
            state[i * 4 + 1 + 96] = 1
            continue
        elif checkers < 0:
            state[i * 4 + 96] = 1
            state[i * 4 + 1 + 96] = 1
            state[i * 4 + 2 + 96] = 1
            state[i * 4 + 3 + 96] = (-checkers - 3) / 12

    state[192] = board[25] / 15
    state[193] = board[26] / 15
    state[194] = 1 - player
    state[195] = player
    return state
