import numpy as np
from enum import Enum


def init_board():
    # инициализация игровой доски
    board = np.zeros(29, dtype=np.int8)
    board[12] = -10
    board[10] = -1
    board[24] = 12
    board[21] = -1
    board[13] = 1
    board[14] = 1
    board[15] = 1
    board[16] = 1
    board[17] = 1
    board[19] = 2
    board[20] = -1
    return board


def display(board):
    print("Доска:")
    print('|%s|' % ' | '.join(('%03s' % i for i in range(1, 13))))
    print('|---------------------------------------------------------------------|')
    print('|%s|' % ' | '.join(('%03s' % i for i in board[1:13])))
    print('|%s|' % ' | '.join(('%03s' % i for i in board[24:12:-1])))
    print('|---------------------------------------------------------------------|')
    print('|%s|' % ' | '.join(('%03s' % i for i in range(24, 12, -1))))
    print('Выкинуто: [%s]' % ','.join(('%03s' % i for i in board[27:29])))


def update(board, move, player):
    temp_board = np.copy(board)

    # if the move is there
    if len(move) > 0:
        start_pos = move[0]
        end_pos = move[1]

        temp_board[start_pos] = temp_board[start_pos] - 1 * player
        temp_board[end_pos] = temp_board[end_pos] + player

    return temp_board


class GameResult(Enum):
    NOT_OVER = 1
    OIN = 2
    MARS = 3


def game_result(board):
    if board[27] != 15 and board[28] != -15:
        return GameResult.NOT_OVER, 0
    if board[27] == 15 and board[28] == 0:
        return GameResult.MARS, 1
    if board[28] == -15 and board[27] == 0:
        return GameResult.MARS, -1
    if board[27] == 15:
        return GameResult.OIN, 1
    else:
        return GameResult.OIN, -1


def is_game_over(board):
    return game_result(board)[0] != GameResult.NOT_OVER


# рассмотреть случай марса
# сделать енам статусов игры: не звершена, марс, норм завершена
# и поменять реализацию is_game_over

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
            elif not is_game_over(board):
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


def generate_all_legal_moves(board, initial_board, dice, player):
    boards = []

    possible_first_moves = generate_legal_move(board, dice[0], player)
    for move1 in possible_first_moves:
        temp_board = update(board, move1, player)
        if not is_move_legal(temp_board, board, dice, player):
            continue
        possible_second_moves = generate_legal_move(temp_board, dice[1], player)
        for move2 in possible_second_moves:
            boards.append(update(temp_board, move2, player))

    if dice[0] != dice[1]:
        possible_first_moves = generate_legal_move(board, dice[1], player)
        for move1 in possible_first_moves:
            temp_board = update(board, move1, player)
            if not is_move_legal(temp_board, board, dice, player):
                continue
            possible_second_moves = generate_legal_move(temp_board, dice[0], player)
            for move2 in possible_second_moves:
                boards.append(update(temp_board, move2, player))

    boards = delete_illegal_moves(boards, initial_board, dice, player)

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

        boards = delete_illegal_moves(boards, initial_board, dice, player)

        # если нет возможности сделать больший ход, делаем меньший
        if len(boards) == 0:
            if dice[0] != dice[1]:
                possible_first_moves = generate_legal_move(board, dice[1], player)
                for move in possible_first_moves:
                    boards.append(update(board, move, player))

    boards = delete_illegal_moves(boards, initial_board, dice, player)

    if len(boards) == 0:
        boards.append(board)

    return np.unique(boards, axis=0)


def generate_moves(board, dice, player):
    if dice[0] == dice[1]:  # проводим 2 хода если значения на костях совпали
        result_boards = []
        new_boards = generate_all_legal_moves(board, board, dice, player)
        new_boards = delete_illegal_moves(new_boards, board, dice, player)
        for new_board in new_boards:
            for result_board in generate_all_legal_moves(new_board, board, dice, player):
                result_boards.append(result_board)
        result_boards = delete_illegal_moves(result_boards, board, dice, player)
        return np.unique(result_boards, axis=0)
    else:
        result_boards = generate_all_legal_moves(board, board, dice, player)
        result_boards = delete_illegal_moves(result_boards, board, dice, player)
        return result_boards


def first_move_6_6(board, player):
    result_board = np.copy(board)
    if player == -1:
        result_board[12] += 2
        result_board[6] -= 2
    if player == 1:
        result_board[24] -= 2
        result_board[18] += 2
    return result_board


def first_move_3_3(board, player):
    result_board = np.copy(board)
    if player == -1:
        result_board[12] += 2
        result_board[3] -= 1
        result_board[9] -= 1
    if player == 1:
        result_board[24] -= 2
        result_board[21] += 1
        result_board[15] += 1
    return result_board


def is_move_legal(board, prev_board, dice, player):
    return len(delete_illegal_moves([board], prev_board, dice, player)) != 0


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
            continue  # пропускаем нелегальный ход
        else:
            first_checked_boards.append(board)

    # особвый случай : первый ход и (6, 6) -- можно снять 2 шашки и сделать неполный ход
    if dice == [6, 6] and prev_board[12] == -15 and player == 1:
        first_checked_boards.append(first_move_6_6(prev_board, player))
    if dice == [6, 6] and prev_board[12] == -15 and player == -1:
        first_checked_boards.append(first_move_6_6(prev_board, player))

    # особый случай: первый ход и (3, 3) -- надо ходить именно на позиции 9 и 3 (21 и 15)
    if dice == [3, 3] and prev_board[12] == -15 and player == 1:
        first_checked_boards.clear()
        first_checked_boards.append(first_move_3_3(prev_board, player))
    if dice == [3, 3] and prev_board[12] == -15 and player == -1:
        first_checked_boards.clear()
        first_checked_boards.append(first_move_3_3(prev_board, player))

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
    # бросок костей
    dice = np.random.randint(1, 7, 2)
    return list(dice)


def input_moves():
    while True:
        try:
            yield list(int(input()))
        except ValueError:
            break


def play_game(player):
    board = init_board()
    display(board)
    while not is_game_over(board):
        print("Ход первого игрока...")
        dice = roll_dice()
        print("Кости: ", dice)
        moves = generate_moves(board, dice, player)
        move_index = np.random.randint(0, len(moves))
        board = moves[move_index]
        display(board)
        print("Ход второго игрока...")
        dice = roll_dice()
        print("Кости: ", dice)
        moves = generate_moves(board, dice, -player)
        move_index = np.random.randint(0, len(moves))
        board = moves[move_index]
        display(board)
    result, winner = game_result(board)
    print("Результат -", result)
    print("Победил", winner)


def play_game_with_bot(player):
    board = init_board()
    display(board)
    while not is_game_over(board):
        print("Ваш ход...")
        dice = roll_dice()
        print("Кости: ", dice)
        print("Наберите свой ход в формате: <from> <to>")
        print("Каждый новый ход набирайте в отдельной строке")
        print("По окончанию набора введите пустую строку")
        while True:  # цикл "пока пользователь не введет корректные ходы"
            new_board = board
            while True:
                move = list(map(int, input().split()))
                if len(move) == 0:
                    break
                if len(move) == 1 or len(move) > 2:
                    print("Неправильный формат ввода. Попробуйте ещё раз")
                    continue
                new_board = update(new_board, move, player)
            allowed_board = False
            for possible_board in generate_moves(board, dice, player):
                if list(new_board) == list(possible_board):
                    allowed_board = True
                    break
            if not allowed_board:
                print("Кто-то пытается жульничать. Введите ход, соответствующий правилам")
                continue
            else:
                break
        board = new_board
        display(board)
        print("Соперник делает ход:")
        dice = roll_dice()
        print("Кости: ", dice)
        moves = generate_moves(board, dice, -player)
        move_index = np.random.randint(0, len(moves))
        board = moves[move_index]
        display(board)


def main():
    board = init_board()
    display(board)
    for b in generate_moves(board, [1, 1], 1):
        if b[17] == 2 and b[19] == 1 and b[24] == 11 and b[22] == 1:
            display(b)

    # play_game_with_bot(1)

    # play_game(1)
    # play_game(-1)


if __name__ == '__main__':
    main()
