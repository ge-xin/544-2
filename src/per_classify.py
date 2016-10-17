import argparse
import os

def load_model(weights, bias, pack_name):
    f = open(pack_name, "r", encoding="latin1")
    bias[0] = int(f.readline())
    size = int(f.readline())
    for i in range(0, size):
        line = f.readline()
        param = line.split()
        word = param[0]
        weight = int(param[1])
        weights[word] = weight
    f.close()

def per_classify(file_path, weights, bias):
    f = open(file_path, "r", encoding="latin1")
    alpha = 0
    for line in f:
        for word in line.split():
            if not(word in weights.keys()):
                continue
            wd = weights[word]
            alpha += wd #for each time only encounter word for one time

    alpha += bias[0]
    f.close()
    if alpha > 0:  return 1
    else: return -1

def __main():
    parser = argparse.ArgumentParser()

    parser.add_argument("path_to_input", help="the path as input to classify")
    parser.add_argument("output_filename", help="assign the output name for the file")

    param = parser.parse_args()
    path_to_input = param.path_to_input
    output_filename = param.output_filename

    weights = {}
    bias = [0]
    PACK_NAME = "./per_model.txt"
    load_model(weights, bias, PACK_NAME)

    f = open(output_filename, "w", encoding="latin1")

    for root, dirs, files in os.walk(path_to_input):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith(".txt"):
                result = per_classify(file_path, weights, bias)
                if result == 1:
                    f.write("spam" + " " + file_path + "\n")
                elif result == -1:
                    f.write("ham" + " " + file_path + "\n")
                else: raise NameError("err in per_classify function.")
    f.close()

__main()

# def __debug():
#     weights = {}
#     bias = [0]
#     PACK_NAME = "./per_model.txt"
#     load_model(weights, bias, PACK_NAME)
#
#     output_filename = "output.txt"
#     f = open(output_filename, "w", encoding="latin1")
#
#     file_path = "/Users/Xin/Desktop/debug/test1.txt";
#     result = per_classify(file_path, weights, bias)
#     if result == 1:
#         f.write("spam" + " " + file_path + "\n")
#     elif result == -1:
#         f.write("ham" + " " + file_path + "\n")
#     else: raise NameError("err in per_classify function.")
#
#     file_path = "/Users/Xin/Desktop/debug/test2.txt";
#     result = per_classify(file_path, weights, bias)
#     if result == 1:
#         f.write("spam" + " " + file_path + "\n")
#     elif result == -1:
#         f.write("ham" + " " + file_path + "\n")
#     else: raise NameError("err in per_classify function.")
#
#     f.close()
#
# __debug()