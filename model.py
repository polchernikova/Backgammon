import datetime
import os
import random

import numpy as np
import tensorflow as tf

from game import Game
from agents import RandomAgent, TDGammonAgent
from backgammon import game_result, generate_moves

from utils import to_backgammon_color, encode_state


class Model:

    def __init__(self, path=None):
        inputs = tf.keras.Input(shape=(196,))
        x = tf.keras.layers.Dense(40, activation="sigmoid")(inputs)
        outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)
        self._model = tf.keras.Model(inputs=inputs, outputs=outputs)

        self._trace = []

        game = Game(TDGammonAgent(self, 0), TDGammonAgent(self, 1))
        self._state = encode_state(game._board, 0)
        self._value = tf.Variable(self._model(self._state[np.newaxis]))

        # self.load(path)

    def train(self, n_episodes=2000):
        print("Training started")
        for episode in range(1, n_episodes + 1):
            player = random.randint(0, 1)
            game = Game(TDGammonAgent(self, player), TDGammonAgent(self, 1 - player))
            game.play()
            self.reset_trace()

            if episode % 500 == 0:
                self.test()
                self.save()

        self.save()
        print("Training ended")

    def test(self):
        print("Testing started")
        wins = 0
        games = 0
        for episode in range(1, 1001):
            player = random.randint(0, 1)
            game = Game(TDGammonAgent(self, player), RandomAgent(1 - player))
            game.play()

            if game_result(game._board)[1] == to_backgammon_color(player):
                wins += 1
            games += 1

        print("Testing ended, result:", wins / games)

    def action(self, board, roll, player):
        best_move = None
        best_win_prob = -np.inf
        available_moves = generate_moves(board, roll, to_backgammon_color(player))
        for available_move in available_moves:
            state = encode_state(available_move, player)[np.newaxis]
            win_prob = tf.reduce_sum(self._model(state))
            win_prob = 1 - win_prob if player == 1 else win_prob

            if win_prob > best_win_prob:
                best_win_prob = win_prob
                best_move = available_move

        return best_move

    def update_weights(self, board, player):
        state = encode_state(board, player)
        with tf.GradientTape() as tape:
            value = self._model(state[np.newaxis])

        trainable_vars = self._model.trainable_variables
        grads = tape.gradient(value, trainable_vars)

        if len(self._trace) == 0:
            for grad in grads:
                self._trace.append(tf.Variable(
                    tf.zeros(grad.get_shape()), trainable=False
                ))

        if player == 0 and game_result(board)[1] == to_backgammon_color(player):
            reward = 1
        else:
            reward = 0

        error = tf.reduce_sum(reward + value - self._value)
        for i in range(len(grads)):
            self._trace[i].assign((0.7 * self._trace[i]) + grads[i])

            grad_trace = 0.1 * error * self._trace[i]
            self._model.trainable_variables[i].assign_add(grad_trace)

        self._state = tf.Variable(state)
        self._value = tf.Variable(value)

    def load(self, path):
        checkpoint = tf.train.Checkpoint(model=self._model, state=self._state, value=self._value)
        checkpoint.restore(path)

    def save(self):
        if not os.path.exists('checkpoint'):
            os.mkdir('checkpoint')

        directory = 'checkpoint/' + str(datetime.datetime.now()).replace(' ', '_')
        if not os.path.exists(directory):
            os.mkdir(directory)

        checkpoint = tf.train.Checkpoint(model=self._model, state=self._state, value=self._value)
        path = checkpoint.save(directory)

        return path

    def reset_trace(self):
        for i in range(len(self._trace)):
            self._trace[i].assign(tf.zeros(self._trace[i].get_shape()))
