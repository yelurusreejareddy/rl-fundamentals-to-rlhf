"""
utils.py
========
This file contains definitions of critical container data structures used in  
the algorithms -- Stack, Queue, PriorityQueue and PriorityQueueWithFunction.

The code here are written using only basic Python.  No specialty
libraries such as Numpy and Pandas are allowed.

The only exception is Python 'heapq' (https://docs.python.org/3/library/heapq.html)
which is used as the storage for PriorityQueue. You may utilize some functions 
defined in the heapq class to complete the class.
"""

from collections import deque
import heapq

class Stack:
    """A container with a last-in-first-out (LIFO) queuing policy."""
    def __init__(self):
        self.stack = deque()  # from Python collections

    def push(self,item):
        "Push 'item' onto the stack"
        ##
        ## Write your code
        self.stack.append(item)
        ##
       

    def pop(self):
        """Pop the most recently pushed item from the stack"""
        ##
        ## Write your code
        if self.isEmpty():
            print("error: stack is empty")
            return None
        return self.stack.pop()
        ##
        

    def isEmpty(self):
        """Returns true if the stack is empty"""
        ##
        ## Write your code
        if len(self.stack) == 0:
            return True
        return False
        ##
        ## additional code
    def space(self):
        return len(self.stack)      
        #

class Queue:
    """A container with a first-in-first-out (FIFO) queuing policy."""
    def __init__(self):
        self.queue = deque()  # from Python collections

    def push(self,item):
        """Enqueue the 'item' into the queue"""
        ##
        ## Write your code
        self.queue.append(item) 
        ##
        

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        ##
        ## Write your code
        if self.isEmpty():
            return None

        return self.queue.popleft()
        ##

    def isEmpty(self):
        """Returns true if the queue is empty"""
        ##
        ## Write your code
        if len(self.queue) == 0:
            return True
        return False
        ##
        ## additional code
    def space(self):
        return len(self.queue)      
        #


class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []  # a Python list
        self.count = 0

    def push(self, item, priority):
        """
        Insert a tuple (priority, self.count, item) in the correct
        position in the priority queue (including reorganizing the queue)
        """
        entry = (priority, self.count, item) # a tuple
        heapq.heappush(self.heap, entry)     # heappush() does all necessary operations
        self.count += 1

    def pop(self):
        """
        Pop a tuple (priority, count, item) from the priority queue (including 
        reorganizing the queue), and returns the item
        """
        ##
        ## Write your code
        if self.isEmpty():
            return None
        priority, count, item = heapq.heappop(self.heap)
        return item 
        ##
 

    def isEmpty(self):
        """Returns true if the priority queue is empty"""
        ##
        ## Write your code
        if len(self.heap)== 0:
            return True
        return False
        ##
   

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

    def space(self):
        return len(self.heap)
    

## This class is derived from PriorityQueue.  The code is complete.
class PriorityQueueWithFunction(PriorityQueue):
    """
    Implements a priority queue with the same push/pop signature of the
    Queue and the Stack classes. This is designed for drop-in replacement for
    those two classes. The caller has to provide a priority function, which
    extracts each item's priority.
    """
    def  __init__(self, priorityFunction):
        """ Note: priorityFunction (item) -> priority"""
        self.priorityFunction = priorityFunction  # store the priority function
        PriorityQueue.__init__(self)              # super-class initializer

    def push(self, item):
        """Adds an item to the queue with priority from the priority function"""
        PriorityQueue.push(self, item, self.priorityFunction(item))
        ## additional code
    def get_priority(self, node):
        return node.status["path_cost"]
        #

###-------------------
## A helper function for your convenience (if you like to use it)
###-------------------
def manhattanDistance( xy1, xy2 ):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )
