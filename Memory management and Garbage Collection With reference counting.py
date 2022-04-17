class node:
    def __init__(self, num):
        #instance fields found by C++ to Python Converter:
        self.data = 0
        self.count = 0
        self.adjacent1 = None
        self.adjacent2 = None
        self.adjacent3 = None

        self.data = num
        self.adjacent1 = None
        self.adjacent2 = None
        self.adjacent3 = None
        self.count = 0 #3 connections are present
class root_tag:

    def __init__(self):
        #instance fields found by C++ to Python Converter:
        self.pointer = None

class Globals:
    heap = [None for _ in range(8)]
    #
    #root1->5 7 3
    #       |/|/|
    #root2->1 8 | 
    #       |\| |
    #       | |\|
    #       |\| |
    #       2 9 10
    #
    @staticmethod
    def initialize(root1, root2):
        temp = node(5)
        Globals.heap[0] = temp
        temp = node(1)
        Globals.heap[1] = temp
        temp = node(2)
        Globals.heap[2] = temp
        temp = node(9)
        Globals.heap[3] = temp
        temp = node(10)
        Globals.heap[4] = temp
        temp = node(7)
        Globals.heap[5] = temp
        temp = node(8)
        Globals.heap[6] = temp
        temp = node(3)
        Globals.heap[7] = temp
        temp = None
        #now all nodes are in the 'heap',to create connections now
        #while making connections, update reference counts
        root1.pointer = Globals.heap[0] #root1->5
        Globals.heap[0].count+=1
        Globals.heap[0].adjacent1 = Globals.heap[1] #5->1
        Globals.heap[1].count+=1
        root2.pointer = Globals.heap[1] #root2->1
        Globals.heap[1].count+=1
        Globals.heap[1].adjacent1 = Globals.heap[2] #1->2
        Globals.heap[2].count+=1
        Globals.heap[1].adjacent2 = Globals.heap[3] #1->9
        Globals.heap[3].count+=1
        Globals.heap[1].adjacent3 = Globals.heap[4] #1->10
        Globals.heap[4].count+=1
        Globals.heap[5].adjacent1 = Globals.heap[1] #7->1
        Globals.heap[1].count+=1
        Globals.heap[5].adjacent2 = Globals.heap[6] #7->8
        Globals.heap[6].count+=1
        Globals.heap[6].adjacent1 = Globals.heap[4] #8->10
        Globals.heap[4].count+=1
        Globals.heap[7].adjacent1 = Globals.heap[6] #3->8
        Globals.heap[6].count+=1
        Globals.heap[7].adjacent2 = Globals.heap[4] #3->10
        Globals.heap[4].count+=1
        #connections done
    @staticmethod
    def print_node(node):
        if node is None:
            return
        print(" ", end = '')
        print(node.data, end = '')
        print("(rfc=", end = '')
        print(node.count, end = '')
        print(")", end = '')
        if node.adjacent1 is not None or node.adjacent2 is not None or node.adjacent3 is not None:
            print("-{", end = '')
            Globals.print_node(node.adjacent1)
            Globals.print_node(node.adjacent2)
            Globals.print_node(node.adjacent3)
            print(" }", end = '')
    @staticmethod
    def print_heap(arr):
        for i in range(0, 8):
            if arr[i] is not None:
                Globals.print_node(arr[i])
                print("\n", end = '')
    @staticmethod
    def print_useful_heap(value):
        print("root->", end = '')
        Globals.print_node(value.pointer)
        print("\n", end = '')
    @staticmethod
    def garbage_collector_rf(arr):
        flag = 0
        for i in range(0, 8):
            if arr[i] is not None:
                if arr[i].count == 0:
                    if arr[i].adjacent1 is not None:
                        arr[i].adjacent1.count-=1
                        arr[i].adjacent1 = None
                    if arr[i].adjacent2 is not None:
                        arr[i].adjacent2.count-=1
                        arr[i].adjacent2 = None
                    if arr[i].adjacent3 is not None:
                        arr[i].adjacent3.count-=1
                        arr[i].adjacent3 = None
                    arr[i] = None
                    arr[i] = None
                    flag = 1
        if flag != 0: #rfc is changed so gc again
            Globals.garbage_collector_rf(arr)

A = root_tag()
B = root_tag()
Globals.initialize(A, B)
print(" Simulation of reference counting garbage collector\n", end = '')
print("legend: -> indicates connection and {} indicate all the elements connected to the element\n", end = '')
print("the full heap is: ", end = '')
print("\n", end = '')
Globals.print_heap(Globals.heap)
print("-----------------", end = '')
print("\n", end = '')
print("Heap connected to the roots is: ", end = '')
print("\n", end = '')
Globals.print_useful_heap(A)
Globals.print_useful_heap(B)
print("-----------------", end = '')
print("\n", end = '')
Globals.garbage_collector_rf(Globals.heap)
print("the garbage collector triggered,full heap disaplaying\n", end = '')
Globals.print_heap(Globals.heap)
print("matche heap connected to roots printed below\n", end = '')
Globals.print_useful_heap(A)
Globals.print_useful_heap(B)