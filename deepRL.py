import tensorflow.compat.v1 as tf
from MyGame import Game
from pygame import Rect, Surface, Color
from Tiles import Tiles
import math
import random
import numpy as np
import pygame

pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 360, 640
WINDOW_SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(WINDOW_SIZE, depth=32)

TILES_RECT_SIZE = 300
TILES_RECT_POS = ((WIDTH-TILES_RECT_SIZE)//2, (HEIGHT - TILES_RECT_SIZE)//2)
TITLE_POS = (WIDTH//2, HEIGHT//2 - 100)
BACKGROUND_COLOR = Color(23, 170, 84)


tf.disable_v2_behavior()

epsilon = 0.02
gamma = 0.999
state = tf.placeholder(tf.float32, shape=[1, 4, 4])
state_vec = tf.reshape(state, [1, (4*4)])
W1 = tf.Variable(tf.truncated_normal(
    [(4*4), 4], stddev=1e-5))
b1 = tf.Variable(tf.constant(0.0, shape=[4]))
z1 = tf.matmul(state_vec, W1) + b1
a1 = tf.nn.silu(z1)
W2 = tf.Variable(tf.truncated_normal(
    [4, 100], stddev=1e-5))
b2 = tf.Variable(tf.constant(0.0, shape=[100]))
z2 = tf.matmul(a1, W2) + b2
a2 = tf.nn.silu(z2)
W3 = tf.Variable(tf.truncated_normal(
    [100, 1000], stddev=1e-5))
b3 = tf.Variable(tf.constant(0.0, shape=[1000]))
z3 = tf.matmul(a2, W3) + b3
a3 = tf.nn.silu(z3)
W4 = tf.Variable(tf.truncated_normal(
    [1000, 5000], stddev=1e-5))
b4 = tf.Variable(tf.constant(0.0, shape=[5000]))
z4 = tf.matmul(a3, W4) + b4
a4 = tf.nn.silu(z4)
W5 = tf.Variable(tf.truncated_normal(
    [5000, 400], stddev=1e-5))
b5 = tf.Variable(tf.constant(0.0, shape=[400]))
z5 = tf.matmul(a4, W5) + b5
a5 = tf.nn.silu(z5)
W6 = tf.Variable(tf.truncated_normal(
    [400, 4], stddev=1e-5))
b6 = tf.Variable(tf.constant(0.0, shape=[4]))
Q4actions = tf.matmul(a5, W6) + b6
Q_n = tf.placeholder(tf.float32, shape=[1, 4])
loss = tf.pow(Q4actions - Q_n, 2)
update = tf.train.GradientDescentOptimizer(1e-10).minimize(loss)

sess = tf.Session()
# sess.run(tf.global_variables_initializer())
new_saver = tf.compat.v1.train.Saver()
new_saver.restore(sess, tf.train.latest_checkpoint('./RL_output/'))
r = 0
for i in range(10000):
    epsilon /= 2
    print('new game')
    tiles_rect = Rect(*TILES_RECT_POS, TILES_RECT_SIZE, TILES_RECT_SIZE)
    tiles = Tiles(TILES_RECT_POS, TILES_RECT_SIZE)

    game = Game(screen, tiles, tiles_rect, 1)
    game.start()
    s = [[math.log2(tile.num) if tile.num > 0 else 0 for tile in row]
         for row in tiles._tiles]  # first move doesn't matter anyway, just get the state
    done = False
    while not done:
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, Color(20, 20, 20), tiles_rect)

        game.update_tiles_state()
        game.draw_tiles()

        all_Qs = sess.run(Q4actions, feed_dict={
                          state: [s]})

        if random.random() < epsilon:
            next_action = random.randint(0, 3)
        else:
            next_action = np.argmax(all_Qs)
        if next_action == 0:
            game.input.down = True
        elif next_action == 1:
            game.input.up = True
        elif next_action == 2:
            game.input.left = True
        else:
            game.input.right = True
        game.move()
        game.input.check_input()
        game.input.reset()

        s_n = [[math.log2(tile.num) if tile.num > 0 else 0 for tile in row]
               for row in tiles._tiles]  # first move doesn't matter anyway, just get the state
        done = next(num == 11 for num in [row for row in s]) or game.over
        r = 0
        if game.over:
            points = max(
                [max(row, key=lambda t: t.num).num for row in tiles._tiles])
            r -= 1/points
            print('last points:', points)
        elif not game.changed:
            r -= 0.1
        Q_corrected = np.copy(all_Qs)
        next_Q = sess.run(Q4actions, feed_dict={
            state: [s_n]})

        Q_corrected[0][next_action] = r + gamma * np.max(next_Q)
        sess.run(update, feed_dict={state: [s], Q_n: Q_corrected})
        s = s_n  # move to the next state
        pygame.display.update()
        clock.tick(60)

saver = tf.compat.v1.train.Saver()
save_path = saver.save(sess, "./RL_output/model")
