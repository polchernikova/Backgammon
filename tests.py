from backgammon import *
import unittest
import numpy as np


class TestStringMethods(unittest.TestCase):
    def test_basic_moves(self):
        board = np.zeros(29, dtype=np.int8)
        board[12] = -5
        board[10] = -5
        board[8] = -5
        board[24] = 15

        expected = np.array([
            [0, 0, 0, 0, 0, -1, 0, 0, -4, 0, -5, 0, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, -1, -1, -3, 0, -5, 0, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, -1, 0, -4, -1, -4, 0, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, -1, 0, -4, 0, -5, -1, -4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, -1, -5, 0, -4, 0, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, -1, -4, 0, -6, 0, -4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, -6, -1, -3, 0, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, -6, 0, -4, -1, -4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, -5, -1, -5, 0, -4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0]
        ])

        np.testing.assert_array_equal(generate_moves(board, [1, 2], -1), expected)

    def test_first_move(self):
        board = np.zeros(29, dtype=np.int8)
        board[12] = -15
        board[24] = 15

        expected = np.array(
            [[0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, -14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0]])

        np.testing.assert_array_equal(generate_moves(board, [1, 2], -1), expected)

        expected = np.array(
            [[0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, -14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0]])

        np.testing.assert_array_equal(generate_moves(board, [1, 1], -1), expected)

        expected = np.array(
            [[0, 0, 0, -1, 0, 0, 0, 0, 0, -1, 0, 0, -13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0]])

        np.testing.assert_array_equal(generate_moves(board, [3, 3], -1), expected)

        expected = np.array(
            [[0, 0, 0, 0, -2, 0, 0, 0, 0, 0, 0, 0, -13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0]])

        np.testing.assert_array_equal(generate_moves(board, [4, 4], -1), expected)

        expected = np.array(
            [[0, 0, 0, 0, 0, 0, -2, 0, 0, 0, 0, 0, -13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0]])

        np.testing.assert_array_equal(generate_moves(board, [6, 6], -1), expected)

        expected = np.array(
            [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -15, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 14, 0, 0, 0, 0]])

        np.testing.assert_array_equal(generate_moves(board, [1, 2], 1), expected)

        expected = np.array(
            [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -15, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 14, 0, 0, 0, 0]])

        np.testing.assert_array_equal(generate_moves(board, [1, 1], 1), expected)

        expected = np.array(
            [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -15, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 13, 0, 0, 0, 0]])

        np.testing.assert_array_equal(generate_moves(board, [3, 3], 1), expected)

        expected = np.array(
            [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -15, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0]])

        np.testing.assert_array_equal(generate_moves(board, [4, 4], 1), expected)

        expected = np.array(
            [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -15, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0]])

        np.testing.assert_array_equal(generate_moves(board, [6, 6], 1), expected)

    def test_no_blocks(self):
        board = np.zeros(29, dtype=np.int8)
        board[12] = -15
        board[24] = 10
        board[16] = 1
        board[18] = 1
        board[19] = 1
        board[20] = 1
        board[21] = 1

        unexpected = np.copy(board)
        unexpected[17] = 1
        unexpected[24] -= 1

        for b in generate_moves(board, [2, 1], 1):
            self.assertFalse(np.array_equal(unexpected, b))

        board = np.zeros(29, dtype=np.int8)
        board[24] = 15
        board[9] = -10
        board[1] = -1
        board[2] = -1
        board[3] = -1
        board[4] = -1
        board[5] = -1

        unexpected = np.copy(board)
        unexpected[6] = -1
        unexpected[9] += 1

        for b in generate_moves(board, [2, 1], -1):
            self.assertFalse(np.array_equal(unexpected, b))

    def test_one_available_move(self):
        board = np.zeros(29, dtype=np.int8)
        board[12] = -11
        board[24] = 14
        board[11] = -1
        board[10] = -1
        board[9] = -1
        board[13] = -1
        board[16] = 1

        expected = np.array(
            [[0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -11, -1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0]])

        np.testing.assert_array_equal(generate_moves(board, [5, 6], 1), expected)

    def test_second_move(self):
        board = np.zeros(29, dtype=np.int8)
        board[12] = -15
        board[24] = 14
        board[21] = 1

        expected = np.array(
            [[0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -14, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 14, 0, 0, 0, 0]])

        np.testing.assert_array_equal(generate_moves(board, [5, 5], -1), expected)


if __name__ == '__main__':
    unittest.main()
