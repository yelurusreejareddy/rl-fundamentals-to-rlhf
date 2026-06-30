"""
node.py
=======
This file contains definitions of critical container data structures used in  
the algorithms -- Stack, Queue, PriorityQueue and PriorityQueueWithFunction.

"""
import copy
import utils

class State:
    """ 
    A class that represents a board for the 8 Puzzle problem.
    A 3x3 board of tiles is represented by a 1x9 flat list of nine numbers, 
    0-9 (both inclusive), where 0 represents the empty cell.  For example,
    
      1 3 4  
      8 6 2  is represented by [1,3,4,8,6,2,7,0,5]
      7 0 5
    """
    # class/static variables
    num_rows, num_cols = 3, 3  # 3x3 grid
    directions = ['up', 'down', 'left', 'right']  # possible directions in a grid from any tile
    direction_offsets = {'up': -3, 'down': 3, 'left': -1, 'right': 1} # offsets in 1D list for each dir
    empty_val = 0  # value that indicates empty cell
    
    # instance methods
    def __init__(self, st = [0,0,0,0,0,0,0,0,0]):
        """ initializes the 1D list representing a 2D (num_rows x num_cols) grid """
        self.st_list = st  # 'st' is a flat/1D list

    def empty_index(self):
        """ returns the 0-based index for the empty cell """
        ##
        ## Write your code
        for index in range(0,len(self.st_list)):
            if self.st_list[index]==0:
                self.empty_val=index
        ##
   

    def find_next_states(self):
        """
        Returns a list of legal states from the current state, considering all directions.
        A legal state should be in the form (direction, next_state), for example ('down', next State object), 
        where 'down' is the direction (to which the empty tile was moved) and 'next State object'  
        is a _NEW_ State object which represenets the empty tile is moved to the direction.
        The function checks all directions and return ONLY the legal new states.
        """
        ##
        ## Write your code
        next_state=[]       
        self.empty_index()
        if self.empty_val >2:
             tile_index=self.st_list[:]
             tile_index[self.empty_val],tile_index[self.empty_val-3] = tile_index[self.empty_val-3],tile_index[self.empty_val]
             next_state.append(tile_index)
        if self.empty_val < 6 :
            tile_index=self.st_list[:]
            tile_index[self.empty_val], tile_index[self.empty_val+3] = tile_index[self.empty_val+3], tile_index[self.empty_val]
            next_state.append(tile_index)
        if self.empty_val%3 != 0:
            tile_index=self.st_list[:]
            tile_index[self.empty_val], tile_index[self.empty_val-1] = tile_index[self.empty_val-1], tile_index[self.empty_val]
            next_state.append(tile_index)
        if self.empty_val%3 != 2 :
            tile_index=self.st_list[:]
            tile_index[self.empty_val], tile_index[self.empty_val+1] = tile_index[self.empty_val+1], tile_index[self.empty_val]
            next_state.append(tile_index)
        return next_state
        ##
   
    
    def __eq__(self, other):
        """ return True if two State's are equal -->
            self.st_list and other are the same list """
        ##
        ## Write your code
        if self.st_list == other.st_list:
           return True
        return False
        ##
     
        
    def __repr__(self):
        """ 
        Returns a string where the 1D list is formatted as a 2D grid, e.g.
          1 3 4  
          8 6 2
          7 0 5
        """
        ##
        ## Write your code
        grid = ""
        for i in range(0, len(self.st_list), self.num_cols):
            row = self.st_list[i:i + self.num_cols]
            rstring = " ".join(str(n) for n in row)
            grid += rstring + "\n"
        return grid.strip()
        ##
        ##additional code
    def misplaced_count(self,item):
        c=0
        g=[1,2,3,8,0,4,7,6,5]
        for i in range(0,len(item)):
            if g[i]!=item[i] and item[i]!=0:
               c=c+1
        return c
        ##
        

class Node:
    """ 
    A class that represents a node in a search tree.  Instance members are straight-forward.
    The self.status is a dictionary containing the values for 'action' (consistent with
    directions in State, 'up', 'down', 'left' or 'right'), 'depth' (counted from 0 at the root),
    'p_cost' (length or cost for the path for this node from the root), and 'ex' (whether
    or not this node has been expanded).
    """
    def __init__(self, state, parent = None, act = None, dep = -1, p_cost = -1, ex = False):
        """ initializes the instance variables """
        self.state = state         # a 'State' object
        self.parent_node = parent  # a parent 'Node'
        self.children = []         # list of child/successor 'Nodes'
        self.status = {'action': act, 'depth': dep, 'path_cost': p_cost, 'expanded': ex}
        
    def print_state(self): 
        """ prints just the state, directly to the terminal """
        print (self.state)

    def find_successors(self):
        """
        Returns the successor nodes in a list.
        """
        ##
        ## Write your code
        if self.status["action"]=="greedy":
            childstages=[]
            childstages=self.state.find_next_states()
            for child_sequence in childstages:
                cnode=Node(State(child_sequence),act="greedy",
                               dep=self.status["depth"]+1,
                               p_cost= self.status["path_cost"]+1
                            )
                self.children.append(cnode)
             
        elif self.status["action"]=="ucs":
            childstages=[]
            childstages=self.state.find_next_states()
            for child_sequence in childstages:               
                cnode=Node(State(child_sequence),act="ucs",
                               dep=self.status["depth"]+1,
                               p_cost= self.status["path_cost"]+child_sequence[self.state.empty_val]
                            )
                self.children.append(cnode)
           
        else:
           childstages=[]
           childstages=self.state.find_next_states()
           for child_sequence in childstages:
               cnode=Node(State(child_sequence),
                               dep=self.status["depth"]+1,
                               p_cost= self.status["path_cost"]+1
                            )
               self.children.append(cnode)

        
        return self.children     

        ##
        


##====================================================
## Additional code, just in case you want to use them.
## It is not required; only for your reference/convenience.
##====================================================
class Problem:
    """ 
    A class that defines various parameters and functions for 8-Puzzle Problem.
    It defines (and creates) the start and goal states (given a 1D list).
    It also defines the cost function -- a cost of each _STEP_ (e.g. always 1 
    or the value of the tile moved).
    """
    def __init__(self, start = None, goal = None, cost_fn = None):
        self.initial = State(start)  # a State object
        self.goal = State(goal)      # ditto
        self.cost_fn = cost_fn
        
    def is_goal(self, other_state):
        return self.goal == other_state


class SearchStrategy:
    """
    A class that defines various parameters/options for search algorithms.
    It defines the container class (to store nodes) to implement frontier 
    (e.g. Stack, Queue, PriorityQueue).  It also defines the heuristic
    function, which estimates the distance to the goal from the current
    state/node.
    """
    def __init__(self, datastr = utils.Queue, heur_fn = None):
        self.ds = datastr         # a container 
        self.heuristic = heur_fn
        
