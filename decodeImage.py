import numpy as np
from PIL import Image

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

def recreate_huffman_tree(fh):
    pqueue = PriorityQueue()
    shapeFlag = True
    for line in fh:
        if shapeFlag:
          shape = tuple(map(int, line.strip().split(', ')))
          shapeFlag = False
        else:
          pixel, frequency = line.split(':')
          pqueue.insert(Node(pixel, int(frequency)))
    while len(pqueue) > 1:
        left = pqueue.delete()
        right = pqueue.delete()
        pqueue.insert(Node(-1, left.frequency + right.frequency, left, right))
    return pqueue.delete(), shape
  
def fill_with_zeros(bin_string):
  while len(bin_string) < 8:
    bin_string = '0' + bin_string
  return bin_string

def decode_file(tree, shape, input_file):
  img_list = []
  curr = tree
  count = 0
  while True:
    if count == shape[0] * shape[1]:
       break
    byte = input_file.read(1)
    byte_bin = bin(int.from_bytes(byte, 'big'))
    bin_string = fill_with_zeros(byte_bin[2:])
    for i in bin_string:
      #ignore first two indexes, they are 0b
      if i == '0':
        curr = curr.left
      else:
        curr = curr.right
      if curr.pixel != -1:
        count += 1
        curr_list = list(map(int,curr.pixel.split(',')))
        img_list.append(curr_list)
        curr = tree
  return img_list,
  
def save_image(img_list, shape, output):
  img_list = np.array(img_list)
  img_list = img_list.astype(np.uint8)
  img_list = np.reshape(img_list, shape)
  Image.fromarray(img_list).save(output)

def main():
  fh = open("./testFiles/frequencyImage.txt", "r")
  fp = open("./testFiles/encodedImage.bin", "rb")


  tree, shape = recreate_huffman_tree(fh)
  img_list = decode_file(tree, shape, fp)
  save_image(img_list, shape, './testFiles/decodedImage.png')

if __name__ == '__main__':
  main()