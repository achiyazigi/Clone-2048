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
    return np.array(s).reshape([1, 4, 4, 1])


WIDTH, HEIGHT = 360, 640
WINDOW_SIZE = (WIDTH, HEIGHT)
TILES_RECT_SIZE = 300
TILES_RECT_POS = ((WIDTH - TILES_RECT_SIZE) // 2, (HEIGHT - TILES_RECT_SIZE) // 2)
TITLE_POS = (WIDTH // 2, HEIGHT // 2 - 100)
BACKGROUND_COLOR = Color(23, 170, 84)

SHOW = True

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE, depth=32)

if SHOW:
    clock = pygame.time.Clock()

# mavg = 0
# d_factor = 0.3
plots = [Plot(), Plot(), Plot(), Plot()]
# EPS = 5
gamma = 0.999

# Network actor
Astate = tf.placeholder(tf.float32, shape=[1, 4, 4, 1])

AW_conv = tf.Variable(tf.truncated_normal(
    shape=[3, 3, 1, 40], stddev=0.1))
AB_conv = tf.Variable(tf.constant(value=0.5, shape=[40]))
AZ_conv = tf.nn.conv2d(Astate, AW_conv, strides=[1, 1, 1, 1], padding="SAME") + AB_conv
AA_conv = tf.nn.silu(AZ_conv)
AA_conv_flat = tf.reshape(AA_conv, [1, -1])

AW1 = tf.Variable(tf.truncated_normal(
    shape=[AA_conv_flat.shape[1], 4000], stddev=0.1))
Ab1 = tf.Variable(tf.constant(0.5, shape=[4000]))
Az1 = tf.matmul(AA_conv_flat, AW1) + Ab1
Aa1 = tf.nn.silu(Az1)

AW2 = tf.Variable(tf.truncated_normal(
    shape=[4000, 400], stddev=0.1))
Ab2 = tf.Variable(tf.constant(0.0, shape=[400]))
Az2 = tf.matmul(Aa1, AW2) + Ab2
Aa2 = tf.nn.silu(Az2)

AW3 = tf.Variable(tf.truncated_normal(
    shape=[400, 40], stddev=0.1))
Ab3 = tf.Variable(tf.constant(0.0, shape=[40]))
Az3 = tf.matmul(Aa2, AW3) + Ab3
Aa3 = tf.nn.silu(Az3)

AW4 = tf.Variable(tf.truncated_normal(
    shape=[40, 10], stddev=0.1))
Ab4 = tf.Variable(tf.constant(0.5, shape=[10]))
Az4 = tf.matmul(Aa3, AW4) + Ab4
Aa4 = tf.nn.silu(Az4)

AW5 = tf.Variable(tf.truncated_normal(
    shape=[10, 4], stddev=0.1))
Ab5 = tf.Variable(tf.constant(0.5, shape=[4]))
Ah = tf.matmul(Aa4, AW5) + Ab5
actions = tf.nn.softmax(Ah)

# Network critic
Cstate = tf.placeholder(tf.float32, shape=[1, 4, 4, 1])
Caction = tf.placeholder(tf.float32, shape=[1, 1])

CW_conv = tf.Variable(tf.truncated_normal(
    shape=[3, 3, 1, 40], stddev=0.1))
CB_conv = tf.Variable(tf.constant(value=0.5, shape=[40]))
CZ_conv = tf.nn.conv2d(Cstate, CW_conv, strides=[1, 1, 1, 1], padding="SAME") + CB_conv
CA_conv = tf.nn.silu(CZ_conv)

CW_action = tf.Variable(tf.truncated_normal(
    shape=[1,CA_conv.shape[0]*CA_conv.shape[0]], stddev=0.1)
    )
Cb_action = tf.Variable(tf.constant(0.5, shape=[CA_conv.shape[0]*CA_conv.shape[0]]))
Cz_action = tf.matmul(Caction, CW_action) + Cb_action
Ca_action = tf.nn.silu(Cz_action)

CA_conv_flat = tf.concat([tf.reshape(CA_conv, [1, -1]), Ca_action], 1)

CW1 = tf.Variable(tf.truncated_normal(
    shape=[CA_conv_flat.shape[1], 1000], stddev=0.1))
Cb1 = tf.Variable(tf.constant(0.5, shape=[1000]))
Cz1 = tf.matmul(CA_conv_flat, CW1) + Cb1
Ca1 = tf.nn.silu(Cz1)

CW2 = tf.Variable(tf.truncated_normal(
    shape=[1000, 500], stddev=0.1))
Cb2 = tf.Variable(tf.constant(0.0, shape=[500]))
Cz2 = tf.matmul(Ca1, CW2) + Cb2
Ca2 = tf.nn.silu(Cz2)

CW3 = tf.Variable(tf.truncated_normal(
    shape=[500, 50], stddev=0.1))
Cb3 = tf.Variable(tf.constant(0.0, shape=[50]))
Cz3 = tf.matmul(Ca2, CW3) + Cb3
Ca3 = tf.nn.silu(Cz3)

CW4 = tf.Variable(tf.truncated_normal(
    shape=[50, 10], stddev=0.1))
Cb4 = tf.Variable(tf.constant(0.5, shape=[10]))
Cz4 = tf.matmul(Ca3, CW4) + Cb4
Ca4 = tf.nn.silu(Cz4)

CW5 = tf.Variable(tf.truncated_normal(
    shape=[10, 1], stddev=0.1))
Cb5 = tf.Variable(tf.constant(0.5, shape=[1]))
CQ_val = tf.matmul(Ca4, CW5) + Cb5

# critic target
# TCW_conv = tf.Variable(tf.truncated_normal(
#     shape=[3, 3, 1, 40], stddev=0.1))
# TCB_conv = tf.Variable(tf.constant(value=0.5, shape=[40]))
# TCZ_conv = tf.nn.conv2d(Cstate, TCW_conv, strides=[1, 1, 1, 1], padding="SAME") + TCB_conv
# TCA_conv = tf.nn.silu(TCZ_conv)
# TCA_conv_flat = tf.concat([tf.reshape(TCA_conv, [1, -1]), Caction], 1)
#
# TCW1 = tf.Variable(tf.truncated_normal(
#     shape=[TCA_conv_flat.shape[1], 400], stddev=0.1))
# TCb1 = tf.Variable(tf.constant(0.5, shape=[400]))
# TCz1 = tf.matmul(TCA_conv_flat, TCW1) + TCb1
# TCa1 = tf.nn.silu(TCz1)
#
# TCW2 = tf.Variable(tf.truncated_normal(
#     shape=[400, 100], stddev=0.1))
# TCb2 = tf.Variable(tf.constant(0.0, shape=[100]))
# TCz2 = tf.matmul(TCa1, TCW2) + TCb2
# TCa2 = tf.nn.silu(TCz2)
#
# TCW3 = tf.Variable(tf.truncated_normal(
#     shape=[100, 50], stddev=0.1))
# TCb3 = tf.Variable(tf.constant(0.0, shape=[50]))
# TCz3 = tf.matmul(TCa2, TCW3) + TCb3
# TCa3 = tf.nn.silu(TCz3)
#
# TCW4 = tf.Variable(tf.truncated_normal(
#     shape=[50, 10], stddev=0.1))
# TCb4 = tf.Variable(tf.constant(0.5, shape=[10]))
# TCz4 = tf.matmul(TCa3, TCW4) + Cb4
# TCa4 = tf.nn.silu(TCz4)
#
# TCW5 = tf.Variable(tf.truncated_normal(
#     shape=[10, 1], stddev=0.1))
# TCb5 = tf.Variable(tf.constant(0.5, shape=[1]))
# TCQ_val = tf.matmul(TCa4, TCW5) + TCb5

# loss functions

# critic
CQ_n = tf.placeholder(tf.float32, shape=[1, 1])
Closs = tf.pow(CQ_n - CQ_val, 2)
Cupdate = tf.train.AdamOptimizer(1e-5).minimize(Closs)

# actor
Qactions = tf.placeholder(tf.float32, shape=[4])
Aloss = -tf.log(actions) * Qactions
Aupdate = tf.train.AdamOptimizer(1e-5).minimize(Aloss)

# start session
sess = tf.Session()
sess.run(tf.global_variables_initializer())
# new_saver = tf.compat.v1.train.Saver()
# new_saver.restore(sess, tf.train.latest_checkpoint('./RL_output/'))

action_map = ["-", "^", "<", ">"]

mean_prob = [0.25, 0.25, 0.25, 0.25, 1]
for i in range(1, 10_001):
    # if i % 100 == 0:
    #     saver = tf.compat.v1.train.Saver()
    #     save_path = saver.save(sess, f"./RL_output/model_{i}")

    print('new game , game number :', i)
    tiles_rect = Rect(*TILES_RECT_POS, TILES_RECT_SIZE, TILES_RECT_SIZE)
    tiles = Tiles(TILES_RECT_POS, TILES_RECT_SIZE)

    game = Game(screen, tiles, tiles_rect, 1)
    game.start()
    s = [[math.log2(tile.num) if tile.num > 0 else 0 for tile in row]
         for row in tiles._tiles]  # first move doesn't matter anyway, just get the state
    done = False
    num_of_turns = 0

    plots[-1].clear()
    for i in range(4):
        plots[i].plot(mean_prob[i]/mean_prob[4], action_map[i])
    plots[-1].draw()
    mean_prob = [0, 0, 0, 0, 1]

    actions_prob = sess.run(actions, feed_dict={
        Astate: reshape(s)})

    prob = np.array(actions_prob).flatten()

    action = np.random.choice([0, 1, 2, 3], p=prob)

    while not done:
        if SHOW:
            screen.fill(BACKGROUND_COLOR)
            pygame.draw.rect(screen, Color(20, 20, 20), tiles_rect)

        game.update_tiles_state()
        game.draw_tiles()

        if action == 0:
            game.input.down = True
        elif action == 1:
            game.input.up = True
        elif action == 2:
            game.input.left = True
        else:
            game.input.right = True
        game.move()
        game.input.check_input()
        game.input.reset()

        # next state
        s_n = [[math.log2(tile.num) if tile.num > 0 else 0 for tile in row]
               for row in tiles._tiles]  # first move doesn't matter anyway, just get the state
        done = next(num == 11 for num in [row for row in s]) or game.over

        # reward
        r = 0
        if game.over:
            points = max(
                [max(row, key=lambda t: t.num).num for row in tiles._tiles])
            r -= 2048 / points
            print('last points:', points)
            # mavg = d_factor * mavg + (1 - d_factor) * points
            # print("mavg : ", mavg)
            # plot.plot(mavg)

        elif not game.changed:
            r -= 100
        else:
            r = max(
                [max(row, key=lambda t: t.num).num for row in tiles._tiles])

        next_actions_prob = sess.run(actions, feed_dict={
            Astate: reshape(s_n)})
        next_action = np.random.choice([0, 1, 2, 3], p=np.array(next_actions_prob).flatten())
        prob_next = np.array(next_actions_prob).flatten()

        # plots[-1].clear()
        for i, p in enumerate(prob_next):
            mean_prob[i] += p
        #     plots[i].plot(p, action_map[i])
        #
        # plots[-1].draw()
        mean_prob[4] += 1
        Q_val = sess.run(CQ_val, feed_dict={
            Cstate: reshape(s), Caction: [[action]]})

        Q_val_next = sess.run(CQ_val, feed_dict={
            Cstate: reshape(s_n), Caction: [[next_action]]})

        Q_corrected = np.zeros(4)
        Q_corrected[action] = Q_val

        # print("Q value = ", Q_val, "reward= ", r, "Q value next=", Q_val_next, "delta = ", r + gamma * Q_val_next,
        #       "diff = ", (r + gamma * Q_val_next) - Q_val)

        sess.run(Aupdate, feed_dict={Astate: reshape(s), Qactions: Q_corrected})

        sess.run(Cupdate, feed_dict={Cstate: reshape(s), Caction: [[action]], CQ_n: r + gamma * Q_val_next})

        # TCQ_val = 0.999*TCQ_val + 0.001*CQ_val
        s = s_n  # move to the next state
        action = next_action
        if SHOW:
            pygame.display.update()
            clock.tick(60)
