import tensorflow.compat.v1 as tf
from MyGame import Game
from pygame import Rect, Surface, Color
from Tiles import Tiles
import math
import random
import numpy as np
import pygame
from Plot import Plot

tf.disable_v2_behavior()

def reshape(s):
    return np.array(s).reshape([1,4,4,1])

WIDTH, HEIGHT = 360, 640
WINDOW_SIZE = (WIDTH, HEIGHT)
TILES_RECT_SIZE = 300
TILES_RECT_POS = ((WIDTH-TILES_RECT_SIZE)//2, (HEIGHT - TILES_RECT_SIZE)//2)
TITLE_POS = (WIDTH//2, HEIGHT//2 - 100)
BACKGROUND_COLOR = Color(23, 170, 84)

SHOW = True

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE, depth=32)

if SHOW:
    clock = pygame.time.Clock()



mavg = 0
d_factor = 0.3
plot = Plot()
plot.plot(0)
# EPS = 5
gamma = 0.999

# Network
state = tf.placeholder(tf.float32, shape= [1, 4, 4, 1])
W_conv = tf.Variable(tf.truncated_normal(
    shape= [3, 3, 1, 10], stddev= 1e-5))
B_conv = tf.Variable(tf.constant(value= 0.0, shape= [10]))
Z_conv = tf.nn.conv2d(state, W_conv, strides= [1, 1, 1, 1], padding= "SAME") + B_conv
A_conv = tf.nn.silu(Z_conv)
# W1_conv = tf.Variable(tf.truncated_normal(
#     shape= [2, 2, 10, 5], stddev= 1e-5))
# B1_conv = tf.Variable(tf.constant(value= 0.0 , shape= [5] ))
# Z1_conv = Z_conv = tf.nn.conv2d(A_conv, W1_conv, strides= [1, 1, 1, 1], padding= "SAME") + B1_conv
# A1_conv = tf.nn.silu(Z1_conv)
A_conv_flat = tf.reshape(A_conv, [1, -1])
W1 = tf.Variable(tf.truncated_normal(
    shape = [A_conv_flat.shape[1], 4], stddev=1e-5))
b1 = tf.Variable(tf.constant(0.0, shape=[4]))
z1 = tf.matmul(A_conv_flat, W1) + b1
a1 = tf.nn.silu(z1)
W2 = tf.Variable(tf.truncated_normal(
    shape = [4, 100], stddev=1e-5))
b2 = tf.Variable(tf.constant(0.0, shape=[100]))
z2 = tf.matmul(a1, W2) + b2
a2 = tf.nn.silu(z2)
W3 = tf.Variable(tf.truncated_normal(
    shape = [100, 1000], stddev=1e-5))
b3 = tf.Variable(tf.constant(0.0, shape=[1000]))
z3 = tf.matmul(a2, W3) + b3
a3 = tf.nn.silu(z3)
W4 = tf.Variable(tf.truncated_normal(
    shape = [1000, 5000], stddev=1e-5))
b4 = tf.Variable(tf.constant(0.0, shape=[5000]))
z4 = tf.matmul(a3, W4) + b4
a4 = tf.nn.silu(z4)
W5 = tf.Variable(tf.truncated_normal(
    shape = [5000, 400], stddev=1e-5))
b5 = tf.Variable(tf.constant(0.0, shape=[400]))
z5 = tf.matmul(a4, W5) + b5
a5 = tf.nn.silu(z5)
W6 = tf.Variable(tf.truncated_normal(
    shape = [400, 4], stddev=1e-5))
b6 = tf.Variable(tf.constant(0.0, shape=[4]))
Q4actions = tf.matmul(a5, W6) + b6
Q_n = tf.placeholder(tf.float32, shape=[1, 4])
loss = tf.pow(Q4actions - Q_n, 2)
update = tf.train.AdamOptimizer(1e-5).minimize(loss)

sess = tf.Session()
sess.run(tf.global_variables_initializer())
# new_saver = tf.compat.v1.train.Saver()
# new_saver.restore(sess, tf.train.latest_checkpoint('./RL_output/'))

r = 0
for i in range(1,10_001):
    # epsilon = EPS/i
    epsilon = 0.1
    print('new game , game number :', i)
    tiles_rect = Rect(*TILES_RECT_POS, TILES_RECT_SIZE, TILES_RECT_SIZE)
    tiles = Tiles(TILES_RECT_POS, TILES_RECT_SIZE)

    game = Game(screen, tiles, tiles_rect, 1)
    game.start()
    s = [[math.log2(tile.num) if tile.num > 0 else 0 for tile in row]
         for row in tiles._tiles]  # first move doesn't matter anyway, just get the state
    done = False
    while not done:
        if SHOW:
            screen.fill(BACKGROUND_COLOR)
            pygame.draw.rect(screen, Color(20, 20, 20), tiles_rect)

        game.update_tiles_state()
        game.draw_tiles()

        all_Qs = sess.run(Q4actions, feed_dict={
                          state: reshape(s)})

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
            r += (points**2)
            print('last points:', points)
            mavg = d_factor*mavg + (1-d_factor)*points
            plot.plot(mavg)

        elif not game.changed:
            r -= 0.1

        Q_corrected = np.copy(all_Qs)
        next_Q = sess.run(Q4actions, feed_dict={
            state: reshape(s_n)})

        Q_corrected[0][next_action] = r + gamma * np.max(next_Q)
        sess.run(update, feed_dict={state: reshape(s), Q_n: Q_corrected})
        s = s_n # move to the next state
        if SHOW:
            pygame.display.update()
            clock.tick(60)

saver = tf.compat.v1.train.Saver()
save_path = saver.save(sess, "./RL_output/model")
