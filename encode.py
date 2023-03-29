# open the files
filename = input("Enter the name of the file to be encoded: ")
test_file = open('testFiles/'+ filename, "r")
frequency_file = open("testFiles/frequency.txt", "w")
codes_file = open("testFiles/codes.txt", "w")
compressed_file = open("testFiles/compressed.bin", "wb")

#create a node class
class Node:
    def __init__(self, char, frequency, left = None, right = None):
        self.char = char
        self.frequency = frequency
        self.left = left
        self.right = right

#create a pririty queue class
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

def create_frequency_file(fh, frequency_file):
    frequencies = {}
    test_list = []
    # create the frequency file and save the file in a list of lines
    for line in fh:
        test_list.append(line)
        for char in line:

            if char not in frequencies:
                frequencies[char] = 1
            else:
                frequencies[char] += 1

    for i in frequencies:
        if i == "\n":
            frequency_file.write(r"\n" + ":" + str(frequencies[i]))
            frequency_file.write("\n")
        elif i == "\t":
            frequency_file.write(r"\t" + ":" + str(frequencies[i]))
            frequency_file.write("\n")
        else:
            frequency_file.write(i + ":" + str(frequencies[i]))
            frequency_file.write("\n")
    return frequencies, test_list



#create a huffman tree using the frequency dictionary and the priority queue
def create_huffman_tree(frequencies):
    pqueue = PriorityQueue()
    for char in frequencies:
        pqueue.insert(Node(char, frequencies[char]))
    while len(pqueue) > 1:
        left = pqueue.delete()
        right = pqueue.delete()
        pqueue.insert(Node(-1, left.frequency + right.frequency, left, right))
    return pqueue.delete()

# create the code dictionary using the huffman tree
code_dict = {}
def create_code_dict(tree, code = ""):
    if tree.char != -1:
        code_dict[tree.char] = [code, tree.frequency]
    else:
        create_code_dict(tree.left, code + "0")
        create_code_dict(tree.right, code + "1")
    return code_dict

def write_codes(code_dict):

    #sort the code dictionary so that the most frequent characters are at the top
    code_dict = dict(sorted(code_dict.items(), key=lambda x: x[1][1],reverse=True))
    for i in code_dict:
        if i == "\n":
            codes_file.write(r"\n" + ":" + str(code_dict[i][0]))
            codes_file.write("\n")
        elif i == "\t":
            codes_file.write(r"\t" + ":" + str(code_dict[i][0]))
            codes_file.write("\n")
        else:    
            codes_file.write(i + ":" + str(code_dict[i][0]))
            codes_file.write("\n")


def write_compressed_file(code_dict, test_list, fh):

    byte = b'\x00'
    count = 7
    # compress test1.txt using the huffman codes, call the new file compressed.bin
    
    for line in test_list:
        for char in line:
            if char in code_dict:
                code = code_dict[char][0]
            for bit in code:
                bit = int(bit) << count
                byte = (int.from_bytes(byte,'big') | bit).to_bytes(1,'big')
                count -= 1
                if count == -1:
                    fh.write(bytes(byte))
                    count = 7
                    byte = b'\x00'

    if count != 0:
        fh.write(bytes(byte))

frequencies, test_list = create_frequency_file(test_file, frequency_file)
tree = create_huffman_tree(frequencies)
code_dict = create_code_dict(tree)
write_codes(code_dict)
write_compressed_file(code_dict, test_list, compressed_file)