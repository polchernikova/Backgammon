import numpy as np


def init_board():
    # инициализация игровой доски
    board = np.zeros(29, dtype=np.int8)
    board[12] = -15
    board[24] = 15
    return board


def display(board):
    print("Board:")
    print(board[1:13])
    print(board[24:12:-1])
    print(board[27:29])


def update(board, move, player):
    temp_board = np.copy(board)

    # if the move is there
    if len(move) > 0:
        start_pos = move[0]
        end_pos = move[1]

        temp_board[start_pos] = temp_board[start_pos] - 1 * player
        temp_board[end_pos] = temp_board[end_pos] + player

    return temp_board


def is_game_over(board):
    return board[27] == 15 or board[28] == -15


def generate_legal_move(board, die, player):
    possible_moves = []

    if player == 1:
        # ходы с выбрасыванием шашки
        if sum(board[7:25] > 0) == 0:
            if board[die] > 0:
                possible_moves.append(np.array([die, 27]))

            elif not is_game_over(board):
                # Если все шашки в доме находятся ближе к краю доски, чем выпавшее число очков, то может выставляться
                # за доску шашка из пункта с наибольшим номером
                start_pos = np.max(np.where(board[1:7] > 0)[0] + 1)
                if start_pos < die:
                    possible_moves.append(np.array([start_pos, 27]))

        possible_start_positions = np.where(board[0:25] > 0)[0]

        # остальные ходы
        for start_pos in possible_start_positions:
            end_pip = start_pos - die
            if end_pip > 0 and board[end_pip] >= 0:
                possible_moves.append(np.array([start_pos, end_pip]))

    elif player == -1:
        # ходы с выбрасыванием шашки
        if sum(board[1:13] < 0) + sum(board[19:25] < 0) == 0:
            if board[13 - die] < 0:
                possible_moves.append(np.array([13 - die, 28]))
            elif not is_game_over(board):  # smá fix
                # Если все шашки в доме находятся ближе к краю доски, чем выпавшее число очков, то может выставляться
                # за доску шашка из пункта с наибольшим номером
                s = np.max(np.where(board[13:19] < 0)[0])
                if s < die:
                    possible_moves.append(np.array([13 + s, 28]))

        # finding all other legal options
        start_positions = np.where(board[0:25] < 0)[0]
        for start_pos in start_positions:
            # корректный переход 1 -> 24
            if start_pos - die <= 0:
                end_pip = (start_pos - die) + 24
            else:
                end_pip = start_pos - die
            if not (start_pos >= 13 > end_pip) and board[end_pip] <= 0:
                possible_moves.append(np.array([start_pos, end_pip]))

    return possible_moves


def generate_all_legal_moves(board, dice, player):
    moves = []
    boards = []

    possible_first_moves = generate_legal_move(board, dice[0], player)
    for move1 in possible_first_moves:
        temp_board = update(board, move1, player)
        possible_second_moves = generate_legal_move(temp_board, dice[1], player)
        for move2 in possible_second_moves:
            if player == -1 and move1[0] == move2[0] == 12 or player == 1 and move1[0] == move2[0] == 24:  # нельзя снимать 2 шашки с головы
                continue
            moves.append(np.array([move1, move2]))
            boards.append(update(temp_board, move2, player))

    if dice[0] != dice[1]:
        possible_first_moves = generate_legal_move(board, dice[1], player)
        for move1 in possible_first_moves:
            temp_board = update(board, move1, player)
            possible_second_moves = generate_legal_move(temp_board, dice[0], player)
            for move2 in possible_second_moves:
                if player == -1 and move1[0] == move2[0] == 12 or player == 1 and move1[0] == move2[0] == 24:  # нельзя снимать 2 шашки с головы
                    continue
                moves.append(np.array([move1, move2]))
                boards.append(update(temp_board, move2, player))

    # если нет возмржности реализовать 2 хода, реализуем хотя бы один
    if len(moves) == 0:
        possible_first_moves = generate_legal_move(board, dice[0], player)
        for move in possible_first_moves:
            moves.append(np.array([move]))
            boards.append(update(board, move, player))

        if dice[0] != dice[1]:
            possible_first_moves = generate_legal_move(board, dice[1], player)
            for move in possible_first_moves:
                moves.append(np.array([move]))
                boards.append(update(board, move, player))

    return moves, np.unique(boards, axis=0)


def roll_dice():
    # rolls the dice
    dice = np.random.randint(1, 7, 2)
    return dice


def main():
    board = init_board()  #
    display(board)
    a = roll_dice()
    print("dice: ", a)
    _, boards = generate_all_legal_moves(board, [5, 3], 1)
    for b in boards:
        display(b)


if __name__ == '__main__':
    main()
