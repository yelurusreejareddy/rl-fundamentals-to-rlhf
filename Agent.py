"""
Agent.py -- Class Agent, which performs Temporal Difference (TD) Q-Learning for the Snake game.
"""
import random
import numpy as np

class Agent:
    """ 
    An AI agent which controls the snake's movements.
    """
    def __init__(self, env, params):
        self.env = env
        self.action_space = env.action_space  # 4 actions for SnakeGame
        self.state_space = env.state_space    # 12 features for SnakeGame
        self.gamma = params['gamma']
        self.alpha = params['alpha']
        self.epsilon = params['epsilon'] 
        self.epsilon_min = params['epsilon_min'] 
        self.epsilon_decay = params['epsilon_decay']
        ## TO-DO: Choose your data structure to hold the Q table and initialize it
        self.Q = {} # creating Q table as a dictionary
        

    @staticmethod
    def state_to_int(state_list):
        """ Map state as a list of binary digits, e.g. [0,1,0,0,1,1,1] to an integer."""
        return int("".join(str(x) for x in state_list), 2)
    
    @staticmethod
    def state_to_str(state_list):
        """ Map state as a list of binary digits, e.g. [0,1,0,0,1,1,1], to a string e.g. '0100111'. """
        return "".join(str(x) for x in state_list)

    @staticmethod
    def binstr_to_int(state_str):
        """ Map a state binary string, e.g. '0100111', to an integer."""
        return int(state_str, 2)

    # (A) 
    def init_state(self, state):
        """ Initialize the state's entry in state_table and Q, if anything needed at all."""
        # converting binary list state to integer key
        state_id = Agent.state_to_int(state)
        if state_id not in self.Q:# checking if state is not already present in Q table
            self.Q[state_id] = [0.0] * self.action_space # initializing Q values for all actions for this new state
        # pass # for now
        
    # (A)
    def select_action(self, state):
        """
        Do the epsilon-greedy action selection. Note: 'state' is an original list of binary digits.
        It should call the function select_greedy() for the greedy case.
        """
        # initializing state in Q table
        self.init_state(state)
        # generating random number to decide between exploration and exploitation
        if random.random() < self.epsilon:
            return np.random.choice(self.action_space) # choosing random action to explore
        else: # choosing best action using greedy method
            return self.select_greedy(state)
        #return np.random.choice(self.action_space) # for now

    # (A)
    def select_greedy(self, state):
        """ 
        Greedy choice of action based on the Q-table. 
        """
        state_id = Agent.state_to_int(state) # converting state to an integer key
        if state_id not in self.Q: # if state not in Q table then random action
            return np.random.choice(self.action_space)
        q_values = self.Q[state_id] # retrieving list of Q values for this state
        max_q = max(q_values)  # finding highest Q value
        # collecting all actions that have highest Q-value
        best_actions = [i for i, q in enumerate(q_values) if q == max_q]
        return random.choice(best_actions)
        # return np.random.choice(self.action_space) # for now
    
    # (A)
    def update_Qtable(self, state, action, reward, next_state):
        """
        Update the Q-table (and anything else necessary) after an action is taken.
        Note that both 'state' and 'next_state' are an original list of binary digits.
        """
        current_state = Agent.state_to_int(state)
        future_state = Agent.state_to_int(next_state)
        self.init_state(state) # initializing both states
        self.init_state(next_state)
        max_q_next = max(self.Q[future_state]) # finding maximum Q value for next state
        current_q = self.Q[current_state][action] # fetching current Q value
        # applying the Q-learning update rule
        self.Q[current_state][action] = current_q + self.alpha * (reward + self.gamma * max_q_next - current_q)
        # update the epsilon at the end
        self.adjust_epsilon()

    # (A)
    def num_states_visited(self):
        """ Returns the number of unique states visited. Obtain from the Q table."""
        return len(self.Q)
        # return 0 # for now
    
    # (A)
    def write_qtable(self, filepath):
        """ Write the content of the Q-table to an output file. """
        with open(filepath, 'w', newline='') as file: # opening file in write mode
            for state_id in sorted(self.Q.keys()): # looping through states in sorted order
                for action_id, q_val in enumerate(self.Q[state_id]):# looping through actions
                    file.write(f"{state_id}, {action_id}, {q_val}\n")
        #pass # for now

    # (A)
    def read_qtable(self, filepath):
        """ Read in the Q table saved in a csv file. """
        try:
            with open(filepath, 'r') as file: # opening file in read mode
                for line in file: # reading each line and parsing state, action, q value
                     state_id_str, action_id_str, q_val_str = line.strip().split(',')
                     state_id = int(state_id_str) # converting to appropriate types
                     action_id = int(action_id_str)
                     q_val = float(q_val_str)
                     if state_id not in self.Q: # initializing state if not in Q table
                         self.Q[state_id] = [0.0] * self.action_space
                     self.Q[state_id][action_id] = q_val # assigning Q value to correct action
        except FileNotFoundError:
            print(f"Error: file {filepath} not found.")
        except ValueError as e:
            print(f"Error: {e}")
        # pass # for now


    def adjust_epsilon(self):
        """ Implements the epsilon decay. """
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
