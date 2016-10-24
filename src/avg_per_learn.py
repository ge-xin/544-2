import argparse
import os
import random

class Feature:
    def __init__(self):
        self.hashmap = {}

def word_frequency_stat(feature, file_path):
    f = open(file_path, "r", encoding="latin1")
    map = feature.hashmap
    for line in f:
        for word in line.split():
            if word in map.keys(): map[word] += 1
            else: map[word] = 1
    f.close()

def inner_avg_per_learn(features_list, weights, bias, u_weights, beta, c):
    random.shuffle(features_list) #WARNING: NEED TO NOTICE HERE, BECAUSE FOR DEBUGING, IT WILL BE COMMENTED.
    for f in features_list:
        alpha = 0
        map = f.hashmap
        for d in map.keys():
            xi = map[d]
            if not(d in weights.keys()): weights[d] = 0
            if not(d in u_weights.keys()): u_weights[d] = 0
            wi = weights[d]
            alpha += (xi * wi)
        alpha += bias[0]

        y = f.type
        if y * alpha <= 0:
            for key in map.keys():
                xd = map[key]
                weights[key] += (y * xd)
            bias[0] += y

            for key in map.keys():
                xd = map[key]
                u_weights[key] += y * c[0] * xd
            beta[0] += y * c[0]

        c[0] += 1

def avg_per_learn(features_list, u_weights, beta, max_iter):
    weights = {}
    b = [0]
    c = [1]

    for i in range(0, max_iter):
        inner_avg_per_learn(features_list, weights, b, u_weights, beta, c)

    for d in u_weights.keys():
        u_weights[d] = weights[d] - (1/c[0]) * u_weights[d]

    beta[0] = b[0] - (1/c[0]) * beta[0]
    # print()


def pack_model(weights, bias, pack_name):
    try:
        f = open(pack_name, "x+", encoding="latin1")
    except FileExistsError:
        f = open(pack_name, 'w', encoding="latin1")
    f.write(str(bias[0]) + "\n")
    f.write(str(len(weights)) + "\n")
    for word in weights.keys():
        f.write(word + " " + str(weights[word]) + "\n")
    f.close()

def __main():
    parser = argparse.ArgumentParser()

    parser.add_argument("path_to_input", help="a data directory containing no spaces act as input")
    arg = parser.parse_args()
    input_path = arg.path_to_input

    features_list = []
    u_weights = {}
    beta = [0]

    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.endswith("txt"):
                file_path = os.path.join(root, file)
                feature = Feature()
                feature.file_name = file_path
                if root.endswith("ham"):
                    feature.type = -1
                elif root.endswith("spam"):
                    feature.type = 1
                word_frequency_stat(feature, file_path)
                features_list.append(feature)

    MAX_ITER = 30; #For avg_per_learn.py: 30.
    avg_per_learn(features_list, u_weights, beta, MAX_ITER)

    PACK_NAME = "./per_model.txt"
    pack_model(u_weights, beta, PACK_NAME)

    # a_u_weights = {}
    # a_beta = [0]
    # load_model(a_u_weights, a_beta, PACK_NAME)
    # if u_weights != a_u_weights: print("Wrong u_weights")
    # if beta != a_beta: print("Wrong beta")

    # print("done")

__main()

# def __debug():
#     features_map = {}
#     files_list = ['/Users/Xin/Desktop/debug/1.spam.txt',
#                  '/Users/Xin/Desktop/debug/2.ham.txt',
#                  '/Users/Xin/Desktop/debug/3.spam.txt',
#                  '/Users/Xin/Desktop/debug/4.ham.txt',
#                  '/Users/Xin/Desktop/debug/5.ham.txt',
#                  '/Users/Xin/Desktop/debug/6.spam.txt',
#                  '/Users/Xin/Desktop/debug/7.ham.txt',
#                  '/Users/Xin/Desktop/debug/8.ham.txt']
#     u_weights = {}
#     beta = [0]
#
#     for file in files_list:
#         feature = Feature()
#         if file.endswith(".ham.txt"):
#             feature.type = -1
#         else:
#             feature.type = 1
#         word_frequency_stat(feature, file)
#         features_map[file] = feature
#     avg_per_learn(features_map, files_list, u_weights, beta, 2)
#     PACK_NAME = "./per_model.txt"
#     pack_model(u_weights, beta, PACK_NAME)
#     print()
# __debug()