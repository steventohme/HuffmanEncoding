import re
import collections
import bisect
import numpy as np
from PIL import Image
codes_file = open("codes1.txt", "w")

class Node:
    def __init__(self, pixel, frequency, left=None, right=None):
        self.pixel = pixel
        self.frequency = frequency
        self.left = left
        self.right = right

class PriorityQueue:
    def __init__(self):
        self.queue = []
    def __len__(self):
        return len(self.queue)
    def isEmpty(self):
        return len(self.queue) == 0
    def insert(self, data):
        l, r = 0, len(self.queue) - 1
        while l <= r:
            m = (l + r) // 2
            if self.queue[m].frequency > data.frequency:
                l = m + 1
            else:
                r = m - 1
        self.queue.insert(l, data)
    def delete(self):
        item = self.queue[-1]
        del self.queue[-1]
        return item

def create_image_array(filename):
    imgArray = np.asarray(Image.open(filename), np.uint8)
    shape = imgArray.shape
    imgArray = imgArray.tolist()
    for i,row in enumerate(imgArray):
        for j, pixel in enumerate(row):
            row[j] = ','.join([str(x) for x in pixel])
        imgArray[i] = row   
    return imgArray, shape

def create_frequency_file(imgArray, frequency_file):
    frequencies = collections.OrderedDict()
    for row in imgArray:
        for pixel in row:
            if pixel not in frequencies:
                frequencies[pixel] = 1
            else:
                frequencies[pixel] += 1

    for i in frequencies:
        frequency_file.write(str(i) + ":" + str(frequencies[i]))
        frequency_file.write("\n")
    
    return frequencies

def round_values(frequencies):
    def list_difference(list1, list2):
        return abs(int(list1[0]) - int(list2[0]) + int(list1[1]) - int(list2[1]) + int(list1[2]) - int(list2[2]))
    average = sum(frequencies.values()) / len(frequencies)
    less_than_average = {k: v for k, v in frequencies.items() if v < average}
    greater_than_average = {k: v for k, v in frequencies.items() if v > average}
    for i in less_than_average:
        i_list = i.split(',')
        greater_than_average[min(greater_than_average.keys(), key = lambda key: list_difference(key.split(','), i_list))] += less_than_average[i]
    
    return greater_than_average

def create_huffman_tree(frequencies):
    pq = PriorityQueue()
    for pixel in frequencies:
        pq.insert(Node(pixel, frequencies[pixel]))
    while len(pq.queue) > 1:
        left = pq.delete()
        right = pq.delete()
        pq.insert(Node(-1, left.frequency + right.frequency, left, right))
    return pq.delete()

code_dict = {}
def create_code_dict(tree, code = ""):
    if tree.pixel != -1:
        code_dict[tree.pixel] = [code, tree.frequency]
    else:
        create_code_dict(tree.left, code + "0")
        create_code_dict(tree.right, code + "1")
    return code_dict

def write_encoded_file(code_dict, imgArray, fh):
    byte = b'\x00'
    count = 7

    for row in imgArray:
        for pixel in row:
            if pixel in code_dict:
                code = code_dict[pixel][0]
            for bit in code:
                bit = int(bit) << count
                byte = (int.from_bytes(byte,'big') | bit).to_bytes(1,'big')
                count -= 1
                if count == -1:
                    fh.write(bytes(byte))
                    count = 7
                    byte = b'\x00'

def write_codes(code_dict):
    #sort the code dictionary so that the most frequent characters are at the top
    code_dict = dict(sorted(code_dict.items(), key=lambda x: x[1][1],reverse=True))
    for i in code_dict: 
        codes_file.write(i + ":" + str(code_dict[i][0]))
        codes_file.write("\n")

  
imgArray, shape = create_image_array('toronto.jpg')
frequency_file = open('frequency1.txt', 'w')
frequencies = create_frequency_file(imgArray, frequency_file)
frequency_file.close()
tree = create_huffman_tree(frequencies)
code_dict = create_code_dict(tree)
write_codes(code_dict)
write_encoded_file(code_dict, imgArray, open('encoded1.bin', 'wb'))

# TODO, image encoding works, however it is not very space efficent (only half as efficient as jpeg). 
# we can make it more space efficient by having unique values, with very long codes, round to any value that is +- 10 of each rgb
# and has a higher frequency than the average. This will make the code more efficient, but will also make the final image less accurate
# https://www.geeksforgeeks.org/python-find-the-closest-key-in-dictionary/
# find the most frequennt codes, split the all frequency dictionary and create new codes
#
# mane fuh dis, allow user to apply compression, 100% encodes pixel for pixel, 50% encodes every other 