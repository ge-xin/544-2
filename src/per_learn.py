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

def inner_per_learn(features_list, weights, bias):
    random.shuffle(features_list) #WARNING: NEED TO NOTICE HERE, BECAUSE FOR DEBUGING, IT WILL BE COMMENTED.
    for f in features_list:
        alpha = bias[0]
        map = f.hashmap
        for d in map.keys():
            xd = map[d]
            if not(d in weights.keys()): weights[d] = 0
            wd = weights[d]
            alpha += (xd * wd)

        y = f.type
        if y * alpha <= 0:
            for d in map.keys():
                xd = map[d]
                weights[d] += (y * xd)
            bias[0] += y

def per_learn(features_list, weights, bias, max_iter):
    for i in range(0, max_iter):
        inner_per_learn(features_list, weights, bias)

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
    weights = {}
    bias = [0]

    MAX_ITER = 20; #For per_learn.py: 20.

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

    per_learn(features_list, weights, bias, MAX_ITER)

    PACK_NAME = "./per_model.txt"
    pack_model(weights, bias, PACK_NAME)

    # a_weights = {}
    # a_bias = [0]
    # load_model(a_weights, a_bias, PACK_NAME)
    # if weights != a_weights: print("Wrong weights")
    # if bias != a_bias: print("Wrong bias")

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
#     weights = {}
#     bias = [0]
#
#     for file in files_list:
#         feature = Feature()
#         if file.endswith(".ham.txt"):
#             feature.type = -1
#         else:
#             feature.type = 1
#         word_frequency_stat(feature, file)
#         features_map[file] = feature
#     per_learn(features_map, files_list, weights, bias, 2)
#     PACK_NAME = "./per_model.txt"
#     pack_model(weights, bias, PACK_NAME)
#     print()
# __debug()
