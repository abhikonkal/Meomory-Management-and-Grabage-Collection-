from tkinter import *
#globals
memory_size = 64
g_size=0

#Linked list utilities
class free_node:
    def __init__(self,index,size):
        self.index = index
        self.size = size
        self.next = None
        self.mark = 0
        self.prev = None

#initially whole memory is free
free_head = free_node(0,memory_size)

def delete_node(itr):
    global free_head
    prev_node = itr.prev
    next_node = itr.next
    if prev_node == None:
        free_head = next_node
        if free_head != None:
            free_head.prev = None
        del itr
    else:
        prev_node.next = next_node
        if next_node != None:
            next_node.prev = prev_node
        del itr

def add_to_free(index,size):
    global free_head
    node = free_node(index,size)
    if free_head == None:
        free_head = node
    else:
        cur = free_head
        prev = None
        while(cur != None and cur.index<index):
            prev = cur
            cur = cur.next
        if prev == None:
            if free_head.index == node.index + node.size:
                free_head.index = node.index
                free_head.size = free_head.size + node.size
            else:
                node.next = free_head
                free_head.prev = node
                node.prev = None
                free_head = node
        elif cur == None:
            if node.index == prev.index+prev.size:
                prev.size = prev.size+node.size
            else:
                prev.next = node
                node.prev = prev
                node.next = None
        else:
            if prev.index+prev.size == node.index and node.index + node.size == cur.index:
                prev.size = prev.size + node.size+cur.size
                prev.next = cur.next
                del cur
                if cur.next != None:
                    cur.next.prev = prev
            elif prev.index+prev.size == node.index:
                prev.size = prev.size+node.size
            elif node.index + node.size == cur.index:
                cur.index = node.index
                cur.size = cur.size+node.size
            else:
                prev.next = node
                node.prev = prev
                node.next = cur
                cur.prev = node

#Simulating alloc and dealloc
def allocate_sim(memory,index,size,ptr_name):
    for i in range(index,index+size):
        memory[i].config(bg = 'black')
    memory[index]['text'] = ptr_name
def deallocate_sim(memory,index,size):
    memory[index]['text'] = ''
    for i in range(index,index+size):
        memory[i].config(bg = 'white')

def declare_garbage(memory,ptr_name,manager):
    for i in range(manager[ptr_name][0],manager[ptr_name][0]+manager[ptr_name][1]):
        memory[i].config(bg = 'red')
    memory[manager[ptr_name][0]]['text'] = 'GBG'

##ALLOCATING MEMORY USING FIRST FIT STRATEGY

def memory_alloc(memory,ptr_to_alloc,size,manager,status_label):
    global free_head
    ptr_name = ptr_to_alloc.get()
    size_to_alloc = size.get()
    #flagging errors if they are present
    try:
        ptr_name = str(ptr_name)
        size_to_alloc = int(size_to_alloc)
    except:
        pass
    else:
        if(size == 0):
            status_label['text'] = "0 sized memory\ncan not be\nallocated."
        elif(len(ptr_name) == 0):
            status_label['text'] = "Variable name\ncan\'t be a\nempty string."
        elif(len(ptr_name)<=50):
            itr = free_head
            found = False
            while itr != None and (not found):
                if itr.size >= size_to_alloc:
                    found = True
                else:
                    itr = itr.next
            if found:
                if ptr_name in manager:
                    declare_garbage(memory,ptr_name,manager) ##if ptr_name is reassigned without freeing the
                    #memory it was already assigned with,it becomes garbage
                    del manager[ptr_name]
                if itr.size == size_to_alloc:
                    itr.mark=1
                    allocate_sim(memory, itr.index, size_to_alloc,ptr_name)
                    manager[ptr_name] = [itr.index,size_to_alloc]
                    delete_node(itr)
                else:
                    itr.mark=1
                    allocate_sim(memory,itr.index,size_to_alloc,ptr_name)
                    manager[ptr_name] = [itr.index,size_to_alloc]
                    itr.size = itr.size-size_to_alloc
                    itr.index = itr.index + size_to_alloc
                status_label['text'] = "Status:\nMemory allocation\nsuccessful.."
            if not found:
                if ptr_name in manager:
                    declare_garbage(memory,ptr_name,manager) ##if ptr_name is reassigned without freeing the
                    #memory it was already assigned with,it becomes garbage
                    global g_size
                    g_size=g_size+manager[ptr_name][1]
                status_label['text'] = "Status:\nMemory allocation\nunsuccessful.."
       

def remove_red_blocks(memory,manager):
    for i in range(0,memory_size):
        if memory[i]['bg'] == 'red':
            memory[i]['text'] = ''
            memory[i].config(bg = 'white') 


def garbage_collector_ms(memory,manager):
    #free all the 0 marked nodes
    itr = free_head
    while itr != None:
        if itr.mark == 0:
            delete_node(itr)
        itr = itr.next
    add_to_free(0,g_size)
    #free all the garbage blocks
    for i in manager:
        if manager[i][0] == 'GBG':
            declare_garbage(memory,i,manager)
            del manager[i]
    remove_red_blocks(memory,manager)
    

def memory_dealloc(memory,manager,ptr_to_free,status_label):
    ptr=ptr_to_free
    if(type(ptr)==str):
        if ptr=="GBG":
            garbage_collector_ms(memory,manager)
            status_label['text'] = "Status:\nGarbage collection\nsuccessful.."
    else:
        ptr = ptr_to_free.get()
        if ptr not in manager:
            status_label['text'] = "Entered pointer\ndoes not\nexist.."
        else:
            deallocate_sim(memory,manager[ptr][0],manager[ptr][1])
            add_to_free(manager[ptr][0],manager[ptr][1])
            del manager[ptr]
            status_label['text'] = "Status:\nMemory Deallocated\nSuccessfully.."
        

if __name__ == "__main__":
    
    
    root = Tk()
    root.title('Heap management')
    root.configure(background = 'orange')
    root.geometry('900x900')
    manager = dict()
    #for memory simulation
    memory = []
    for i in range(100):
        memory.append(Button(root,text = "",state = DISABLED,bg = 'white'))
        
    x_off = 0.20
    y_off = 0.30

    for i in range(10):
        for j in range(10):
            memory[i*8+j].place(relx = x_off+(1/8)*j*0.60,rely = y_off+(1/8)*i*0.60,relheight = 1/8*0.60,relwidth = 1/8*0.60)

    #for messages
    message = "\n**U can ENTER GBG in ptr to free or\n press garbage colllector button to trigger garbage collector"
             
    message_label = Label(root,text = message,font = "Helvetica 8",bg = "orange")
    message_label.place(relx = 0,rely = 0.9,relheight = 0.1,relwidth = 1)
    status_label = Label(root,text = "",font = "Helvetica 10",bg = "orange")
    status_label.place(relx = 0.80,rely = 0.30,relwidth = 0.20,relheight = 0.60)

    #user helper grids
    back_gr = Label(root,text = '',bg = 'blue')
    back_gr.place(relx = 0,rely = 0.375,relwidth = 0.18,relheight = 0.525)
    mean = Label(root,text = "Legend",font = "italic",bg = 'blue')
    mean.place(relx = 0,rely = 0.375,relheight = 0.075,relwidth = 0.18)
    white_button = Button(root,text ='',state = DISABLED)
    white_button.place(relx = 0.05,rely = 0.45,relwidth = 0.075,relheight = 0.075)
    white_means = Label(root,text = "Free Cell",font = "Helvetica 10 bold",bg = 'blue')
    white_means.place(relx = 0,rely = 0.525,relwidth = 0.18,relheight = 0.075)
    black_button = Button(root, text='', state=DISABLED,bg = "black")
    black_button.place(relx=0.05, rely=0.60, relwidth=0.075, relheight=0.075)
    black_means = Label(root, text="Allocated Cell", font="Helvetica 10 bold",bg = 'blue')
    black_means.place(relx=0, rely=0.675, relwidth=0.18, relheight=0.075)
    red_button = Button(root,text = '',bg = 'red',state = DISABLED)
    red_button.place(relx = 0.05,rely = 0.75,relwidth=0.075, relheight=0.075)
    red_label = Label(root,text = "GBG:\nGarbage cell",font = "Helvetica 10 bold",bg = "blue")
    red_label.place(relx = 0,rely = 0.825,relwidth = 0.18,relheight = 0.075)


    #for allocation simulation
    l_alloc = Label(root,text = "Allocate a memory",font = "Times 20 italic bold",bg ="orange")
    l_alloc.place(relx = 0,rely = 0,relheight = 0.075,relwidth = 0.40)
    ptr_ask_alloc = Label(root, text="ptr name :", font="Times 20 italic bold", bg="orange")
    ptr_ask_alloc.place(relx=0, rely=0.075, relheight=0.075, relwidth=0.20)
    ptr_to_alloc = Entry(root,font = "Times 20 italic bold",justify = CENTER)
    ptr_to_alloc.place(relx = 0.20,rely = 0.075,relheight = 0.075,relwidth = 0.20)
    size_ask = Label(root, text="Size to allocate :", font="Times 20 italic bold", bg="orange")
    size_ask.place(relx=0, rely=0.15,relheight=0.075, relwidth=0.20)
    size = Entry(root, font="Times 20 italic bold", justify=CENTER)
    size.place(relx=0.20, rely=0.15, relheight=0.075, relwidth=0.20)

    #imp button
    submit_alloc = Button(root,text = "Submit",font = "Times 20 italic bold",command = lambda : memory_alloc(memory,ptr_to_alloc,size,manager,status_label))


    submit_alloc.place(relx = 0.20,rely = 0.225+0.0112,relheight = 0.05,relwidth = 0.20)

    #for deallocation(freeing memory) simulation
    l_free = Label(root,text = "Free the memory",font = "Times 20 italic bold",bg = 'orange')
    l_free.place(relx = 0.60,rely = 0,relheight = 0.075,relwidth = 0.40)
    ptr_ask_free = Label(root,text = "ptr name :",font = "Times 20 italic bold",bg = 'orange')
    ptr_ask_free.place(relx=0.60, rely=0.075, relheight=0.075, relwidth=0.20)
    ptr_to_free = Entry(root,font = "Times 20 italic bold",justify = CENTER)
    ptr_to_free.place(relx = 0.80,rely = 0.075, relheight = 0.075,relwidth = 0.20)

    #imp button
    submit_free = Button(text = "Submit",font = "Times 20 italic bold",command = lambda:memory_dealloc(memory,manager,ptr_to_free,status_label))
    submit_free.place(relx = 0.80,rely = 0.15+0.0125,relheight = 0.05,relwidth = 0.20)


    #for garbage collection simulation
    l_gc= Label(root,text = "Garbage collection :",font = "Times 20 italic bold",bg = 'orange')
    l_gc.place(relx = 0.70,rely = 0.225,relheight = 0.05,relwidth = 0.40)
    gc_button = Button(root,text = "Submit",font = "Times 20 italic bold",command = lambda : memory_dealloc(memory,manager,"GBG",status_label))
    gc_button.place(relx = 0.80,rely = 0.225+0.0500,relheight = 0.05,relwidth = 0.20)
    
    root.mainloop()
