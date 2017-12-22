import math

class min_priority_queue():
    '''this class implements a min priority queue using a min heap'''
    #init function expects a list of 2 tuples (key, value) pairs as input
    #key is used to move elements arund in the priority queue and value is the satellite data
    def __init__(self, in_lst):
        self.lst = in_lst
        #length of input list
        self.lst_len = len(self.lst)
        self.build_min_heap()

    def is_empty(self):
        if (self.lst_len > 0):
            return False
        else:
            return True

    def min_heapify(self, index=0):
        #look at the current node as if it is the root and those below
        #operate on it to satisfy the min heap property
        if (index == None):
            return
        root = index
        left_child = index*2 + 1
        right_child = index*2 + 2
        tmp_lst = [math.inf, math.inf, math.inf]
        if (root < self.lst_len):
            tmp_lst[0] = self.lst[root][0]
        if (left_child < self.lst_len):
            tmp_lst[1] = self.lst[left_child][0]
        if (right_child < self.lst_len):
            tmp_lst[2] = self.lst[right_child][0]
        min_ind = tmp_lst.index(min(tmp_lst))
        if (min_ind == 1):
            self.swap(left_child, root)
            self.min_heapify(left_child)
        elif (min_ind == 2):
            self.swap(right_child, root)
            self.min_heapify(right_child)

    def build_min_heap(self):
        for i in range(int(math.floor(len(self.lst)/2))-1, -1, -1):
            self.min_heapify(i)

    def remove_min(self):
        #check if there are any elements in lst
        if (self.lst_len<1):
            return None
        #swap the first and last elements
        self.swap(0, self.lst_len-1)
        ret_val = self.lst.pop()
        self.lst_len -= 1
        if (self.lst_len != 0):
            self.min_heapify(0)
        return (ret_val[1])

    def decrease_key(self, original_tuple, new_key):
        #assume the node we are searching for to be at child_index
        #any updates to the binary tree will propagate upwards
        child_index = self.lst.index(original_tuple)
        #check if the key actually decresed
        if (self.lst[child_index][0] > new_key):
            #update the key
            self.lst[child_index] = (new_key,self.lst[child_index][1])
        else:
            return
        if (child_index % 2 == 1):
            parent_index = int((child_index-1)/2)
        else:
            parent_index = int((child_index-2)/2)

        while (parent_index > -1):
            if (self.lst[child_index][0] < self.lst[parent_index][0]):
                self.swap(child_index, parent_index)
                child_index = parent_index
            else:
                return
            if (child_index % 2 == 1):
                parent_index = int((child_index-1)/2)
            else:
                parent_index = int((child_index-2)/2)

    def swap(self, ind1, ind2):
        temp = self.lst[ind1]
        self.lst[ind1] = self.lst[ind2]
        self.lst[ind2] = temp
