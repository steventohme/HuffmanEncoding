class Node:
    def __init__(self, char, frequency, left = None, right = None):
        self.char = char
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
        self.queue.append(data)
    def delete(self):
        min = 0
        for i in range(len(self.queue)):
            if self.queue[i].frequency <= self.queue[min].frequency:
                min = i
        item = self.queue[min]
        del self.queue[min]
        return item

def recreate_huffman_tree(fh):
    pqueue = PriorityQueue()
    for line in fh:
        char, frequency = line.split(':')
        pqueue.insert(Node(char, int(frequency)))
    while len(pqueue) > 1:
        left = pqueue.delete()
        right = pqueue.delete()
        pqueue.insert(Node(-1, left.frequency + right.frequency, left, right))
    return pqueue.delete()
  
def fill_with_zeros(bin_string):
  while len(bin_string) < 8:
    bin_string = '0' + bin_string
  return bin_string
def decode_file(tree, input_file, output_file):
  curr = tree
  while True:
    byte = input_file.read(1)
    if not byte:
      break
    byte_bin = bin(int.from_bytes(byte, 'big'))
    bin_string = fill_with_zeros(byte_bin[2:])
    for i in bin_string:
      #ignore first two indexes, they are 0b
      if i == '0':
        curr = curr.left
      else:
        curr = curr.right
      if curr.char != -1:
        output_file.write(curr.char)
        curr = tree






fh = open("testFiles/frequency.txt", "r")
fp = open("testFiles/compressed.bin", "rb")
output_file = open("testFiles/decoded.txt", "w")

tree = recreate_huffman_tree(fh)
decode_file(tree, fp,output_file)

