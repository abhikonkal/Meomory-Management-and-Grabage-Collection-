class node:
    def __init__(self, num):
        #instance fields found by C++ to Python Converter:
        self.data = 0
        self.mark = False
        self.adjacent1 = None
        self.adjacent2 = None
        self.adjacent3 = None

        self.data = num
        self.adjacent1 = None
        self.adjacent2 = None
        self.adjacent3 = None
        Globals.mark=False #we know at most 3 connections are present
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
        #create connections now
        root1.pointer = Globals.heap[0] #root1->5
        Globals.heap[0].adjacent1 = Globals.heap[1] #5->1
        root2.pointer = Globals.heap[1] #root2->1
        Globals.heap[1].adjacent1 = Globals.heap[2] #1->2
        Globals.heap[1].adjacent2 = Globals.heap[3] #1->9
        Globals.heap[1].adjacent3 = Globals.heap[4] #1->10
        Globals.heap[5].adjacent1 = Globals.heap[1] #7->1
        Globals.heap[5].adjacent2 = Globals.heap[6] #7->8
        Globals.heap[6].adjacent1 = Globals.heap[4] #8->10
        Globals.heap[7].adjacent1 = Globals.heap[6] #3->8
        Globals.heap[7].adjacent2 = Globals.heap[4] #3->10
        #connections done
    @staticmethod
    def mark_node(ptr):
        head = ptr
        tail = None
        middle = None
        flag = 1
        while head is not None:
            if not head.mark: #if node we are on is unmarked, mark it
                head.mark = True
            if head.adjacent1 is not None and not head.adjacent1.mark: #if adjacent node to this is unmarked
                tail = middle
                middle = head
                head = head.adjacent1
            elif head.adjacent2 is not None and not head.adjacent2.mark: 
                tail = middle
                middle = head
                head = head.adjacent2
            elif head.adjacent3 is not None and not head.adjacent3.mark:
                tail = middle
                middle = head
                head = head.adjacent3
            else:
                head = middle
                middle = tail
                tail = None

    @staticmethod
    def marker(value):
        Globals.mark_node(value.pointer)
    @staticmethod
    def sweep(arr):
        for i in range(0, 8):
            if arr[i] is not None:
                if not arr[i].mark:
                    #abandone the node
                    arr[i].adjacent1 = None
                    arr[i].adjacent2 = None
                    arr[i].adjacent3 = None
                    arr[i] = None
                    arr[i] = None
    @staticmethod
    def garbage_collector(r1, r2, hp):
        print("Mark phase started.......", end = '')
        print("\n", end = '')
        Globals.marker(r1)
        Globals.marker(r2)
        print("Marking  phase done", end = '')
        print("\n", end = '')
        print("Sweep phase started.......", end = '')
        print("\n", end = '')
        Globals.sweep(hp)
    @staticmethod
    def print_node(node):
        if node is None:
            return
        print(" ", end = '')
        print(node.data, end = '')
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


A = root_tag()
B = root_tag()
Globals.initialize(A,B)
print("Simulation for mark sweep garbage collector\n", end = '')
print("legend: - indicates connection and {} indicate all the elements connected to the element\n", end = '')
print("Displaying full heap is: ", end = '')
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
Globals.garbage_collector(A, B, Globals.heap)
print("gc triggered displaying heap\n", end = '')
Globals.print_heap(Globals.heap)
print("match heap connected to roots printed below\n", end = '')
Globals.print_useful_heap(A)
Globals.print_useful_heap(B)
print("-----------------", end = '')