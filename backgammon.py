import numpy as np


def init_board():
    # инициализация игровой доски
    board = np.zeros(29, dtype=np.int8)
    board[12] = -13
    board[11] = -1
    board[10] = -1
    board[24] = 13
    board[23] = 1
    board[22] = 1
    return board


def display(board):
    print("Board:")
    print('|%s|' % ' | '.join(('%03s' % i for i in range(1, 13))))
    print('|---------------------------------------------------------------------|')
    print('|%s|' % ' | '.join(('%03s' % i for i in board[1:13])))
    print('|%s|' % ' | '.join(('%03s' % i for i in board[24:12:-1])))
    print('|---------------------------------------------------------------------|')
    print('|%s|' % ' | '.join(('%03s' % i for i in range(14, 26))))
    print('Beard off: [%s]' % ','.join(('%03s' % i for i in board[27:29])))


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
    boards = []

    possible_first_moves = generate_legal_move(board, dice[0], player)
    for move1 in possible_first_moves:
        temp_board = update(board, move1, player)
        possible_second_moves = generate_legal_move(temp_board, dice[1], player)
        for move2 in possible_second_moves:
            boards.append(update(temp_board, move2, player))

    if dice[0] != dice[1]:
        possible_first_moves = generate_legal_move(board, dice[1], player)
        for move1 in possible_first_moves:
            temp_board = update(board, move1, player)
            possible_second_moves = generate_legal_move(temp_board, dice[0], player)
            for move2 in possible_second_moves:
                boards.append(update(temp_board, move2, player))

    boards = delete_illegal_moves(boards, board, dice, player)

    # если нет возможности реализовать 2 хода, реализуем хотя бы один
    if len(boards) == 0:
        # обеспечиваем dice[0] > dice[1] чтобы сделать по возможности больший ход
        if dice[0] < dice[1]:
            temp = dice[1]
            dice[1] = dice[0]
            dice[0] = temp
        possible_first_moves = generate_legal_move(board, dice[0], player)
        for move in possible_first_moves:
            boards.append(update(board, move, player))

        # если нет возможности сделать больший ход, делаем меньший
        if len(boards) == 0:
            if dice[0] != dice[1]:
                possible_first_moves = generate_legal_move(board, dice[1], player)
                for move in possible_first_moves:
                    boards.append(update(board, move, player))

    boards = delete_illegal_moves(boards, board, dice, player)

    return np.unique(boards, axis=0)


def generate_moves(board, dice, player):
    if dice[0] == dice[1]:  # проводим 2 хода если значения на костях совпали
        result_boards = []
        new_boards = generate_all_legal_moves(board, dice, player)
        for new_board in new_boards:
            for result_board in generate_all_legal_moves(new_board, dice, player):
                result_boards.append(result_board)
        result_boards = delete_illegal_moves(result_boards, board, dice, player)
        return np.unique(result_boards, axis=0)
    else:
        result_boards = generate_all_legal_moves(board, dice, player)
        result_boards = delete_illegal_moves(result_boards, board, dice, player)
        return result_boards


def first_move_six_six(board, player):
    result_board = np.copy(board)
    if player == -1:
        result_board[12] += 2
        result_board[6] -= 2
    if player == 1:
        result_board[24] -= 2
        result_board[18] += 2
    return result_board


def delete_illegal_moves(boards, prev_board, dice, player):
    # нельзя снимать 2 шашки с головы, только если это не случаи (3, 3), (4, 4), (6, 6) на первом ходу
    first_checked_boards = []
    special_dices = [[3, 3], [4, 4], [6, 6]]
    for board in boards:
        if prev_board[24] > board[24] + 1 \
                and not (prev_board[24] == 15 and dice in special_dices) \
                or prev_board[12] < board[12] - 1 \
                and not (prev_board[12] == -15 and dice in special_dices) \
                or prev_board[24] > board[24] + 2 \
                or prev_board[12] < board[12] - 2:
            continue  # пропускаем нелегальных ход
        else:
            first_checked_boards.append(board)

    # особвый случай : первый ход и (6, 6) -- можно снять 2 шашки и сделать неполный ход
    if dice == [6, 6] and prev_board[12] == -15 and player == 1:
        first_checked_boards.append(first_move_six_six(prev_board, player))
    if dice == [6, 6] and prev_board[12] == -15 and player == -1:
        first_checked_boards.append(first_move_six_six(prev_board, player))

    second_checks_boards = []

    # Запрещено выставлять блок из 6 шашек, если впереди этого блока нет шашки соперника
    for board in first_checked_boards:
        no_illegal_blocks = True
        for block_start in range(1, 18):
            if np.all(board[block_start:block_start + 6] > 0):
                # проверяем, что впереди блока нет шашки соперника
                if block_start <= 7:
                    if np.all(board[1:block_start] >= 0) and np.all(board[13:24] >= 0):
                        no_illegal_blocks = False
                        break
                if block_start >= 12:
                    if np.all(board[13:block_start] >= 0):
                        no_illegal_blocks = False
                        break
            if np.all(board[block_start:block_start + 6] < 0):
                if block_start <= 7:
                    if np.all(board[1:block_start] <= 0):
                        no_illegal_blocks = False
                        break
                if block_start >= 12:
                    if np.all(board[1:13] <= 0) and np.all(board[14:block_start] <= 0):
                        no_illegal_blocks = False
                        break

        if no_illegal_blocks:
            second_checks_boards.append(board)

    return second_checks_boards


def roll_dice():
    # rolls the dice
    dice = np.random.randint(1, 7, 2)
    return dice


def main():
    board = init_board()
    display(board)
    a = roll_dice()
    print("dice: ", a)
    boards = generate_moves(board, [5, 5], 1)
    for b in boards:
        display(b)

if __name__ == '__main__':
    main()
