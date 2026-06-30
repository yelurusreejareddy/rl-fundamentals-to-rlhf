"""
QLearning.py -- Q-learning training loop for the Snake game.
"""
import matplotlib
import SnakeEnv as snake_env
import Agent as agent_class

import numpy as np
import matplotlib.pyplot as plt
import random
import copy

def q_learning(agent, env, max_steps, train=True, use_epsilon=False):
    """
    This function simulates a RL game, where the agent learns the (hopefully) optimal policy
    by Q-learning.  The parameters 'agent' and 'env' are created in the calling function and
    passed in, while 'max_step' specifies the maximum timesteps to play (Note: continuous 
    after failing) and 'train' indicates the run is a training or otherwise (i.e., evaluation).
    Most lines are basic and general, calling functions in the environment or the agent.  
    Details depend on the implementations of those components (and their functions).
    """
    # First reset the environment
    state = env.reset()
    agent.init_state(state) #(A)
    
    # Initialize some housekeeping variables
    total_return, n_apples, n_stops, n_goodsteps = 0.0, 0, 0, 0
    done = False
   
    # Play continuously until max_steps.
    for i in range(max_steps):
        
        # Select the action to take at this state. 
        if train or use_epsilon: # this supports epsilon selection during eval
            action = agent.select_action(state)  #(A) epsilon greedy selection
        else:
            action = agent.select_greedy(state)  #(A) greedy selection
        
        # Environment executes the selected action.
        next_state, reward, done, _ = env.step(action) 
        
        # Q-learning if training -- update the Q-table
        if train:
            agent.update_Qtable(state, action, reward, next_state)  #(A) 
            
        # Update to prepare for the next iteration
        state = next_state
        
        # Accumulate the total return and other counts from this step
        total_return += pow(agent.gamma, i) * reward

        if reward == 10:
            n_apples += 1
        elif reward == 1:
            n_goodsteps += 1
        # The play is continuous, so this condition doesn't make the play terminate,
        # but an episode stops when a snake curls itself or hits a wall.
        elif reward == -100:  # i.e., done
            n_stops += 1
        #
    return total_return, n_apples, n_stops, n_goodsteps, agent.num_states_visited() #(A)
    
    
# Do q_learning for 'num_runs' times.  For each run, 'num_steps' steps is done.
def run_ql(max_runs, max_steps, in_params, qtable_file, display = False, train = False, use_epsilon=False):
    """
 use_epsilon: uses epsilon-greedy selection even during evaluation if true.
    """
    num_runs = max_runs
    num_steps = max_steps
    results_list = []
    best_return = float('-inf')
    best_qtable = None

    for run in range(num_runs):
        # reset params
        params = copy.deepcopy(in_params)  # reset the parameters

        # Create an environment and an agent
        env = snake_env.SnakeEnv()
        agent = agent_class.Agent(env, params)

        env.display = display  ## <== display True/False (on/off)

        # If evaluation, read in the given q-table (otherwise q_learning() initializes to small random numbers)
        if not train and qtable_file is not None:
            agent.read_qtable(qtable_file)

        ret = q_learning(agent, env, num_steps, train=train, use_epsilon=use_epsilon) # training=False for evaluation
        results_list.append(ret)

        env.close() # for each run
        print ("* Run {}: Return={:>8.3f}, #Apples={}, #Stops={}, #GoodSteps={}, #UniqueStatesVisited={}"
               .format(run, ret[0], ret[1], ret[2], ret[3], ret[4]))

        if train:
            if ret[0] > best_return:
                best_return = ret[0]
                best_qtable = agent.Q

    if train:
        agent.Q = best_qtable  # overwrite the agent's last Q table
        agent.write_qtable(qtable_file) # so that this function can be used

    return results_list

##===================================================
## Call run_ql() for either/both training and evaluation
#num_runs = 1      #10
#num_steps = 1000 #300   #1000

#params = dict()
#params['gamma'] = 0.95
#params['alpha'] = 0.7
#params['epsilon'] = 0.9  # exploration probability at start
#params['epsilon_min'] = .01  # minimum epsilon
#params['epsilon_decay'] = .995  # exponential decay rate for epsilon

#qtable_file = "qtable_2025_9.csv" #"qtable_true.csv" #None

## Call run_ql() for either training or evaluation
#results_list = run_ql(num_runs, num_steps, params, qtable_file, display = True, train = False) # evaluation
##results_list = run_ql(num_runs, num_steps, params, qtable_file, display = False, train = True) # training

#results = np.array(results_list)
#cmean = np.mean(results, axis=0)
#print ("\n** Mean: Return={:>8.3f}, #Apples={}, #Stops={}, #GoodSteps={}, #UniqueStatesVisited={}"
#           .format(cmean[0], cmean[1], cmean[2], cmean[3], cmean[4]))

# ---------------------------------------------------------
# Part 2: Experimenting with given Epsilons
# ---------------------------------------------------------
qtable_file = "qtable_2025_9.csv" # using best Q table from Part 1
epsilon_values = [0.1, 0.3, 0.5, 0.7, 0.9] # Epsilon values that are given
# collecting results for plotting
returns = []
apples = []
stops = []
good_steps = []
unique_states = []
# parameters
num_runs = 10
num_steps = 1000

for eps in epsilon_values:
    print("\n## Evaluating with epsilon =", eps)
    params = dict()
    params['gamma'] = 0.95
    params['alpha'] = 0.7
    params['epsilon'] = eps
    params['epsilon_min'] = .01  # minimum epsilon
    params['epsilon_decay'] = .995  # exponential decay rate for epsilon
    # evaluating using learned Q table
    # display is false and use_epsilon = True for action selection
    results_list = run_ql(num_runs, num_steps, params, qtable_file, display=False, train=False, use_epsilon=True)
    results = np.array(results_list)
    cmean = np.mean(results, axis=0)
    print("** Mean: Return={:>8.3f}, #Apples={:.1f}, #Stops={:.1f}, #GoodSteps={:.1f}, #UniqueStatesVisited={:.1f}"
          .format(cmean[0], cmean[1], cmean[2], cmean[3], cmean[4]))

    # storing mean values for plotting
    returns.append(cmean[0])
    apples.append(cmean[1])
    stops.append(cmean[2])
    good_steps.append(cmean[3])
    unique_states.append(cmean[4])
# ---------------------------------------------------------
#  plotting
# ---------------------------------------------------------
# creating figure with 5 subplots
fig, axes = plt.subplots(3, 2, figsize=(12, 10))
axes_flat = axes.flatten() # easier indexing
axes_flat[0].plot(epsilon_values, returns, 'g-o', linewidth=2, markersize=8)# Mean Returns
axes_flat[0].set_title('Mean Returns', fontsize=12)
axes_flat[1].plot(epsilon_values, apples, 'r-o', linewidth=2, markersize=8)# Mean of Apples
axes_flat[1].set_title('Mean # of Apples', fontsize=12)
axes_flat[2].plot(epsilon_values, stops, 'b-o', linewidth=2, markersize=8)# Mean of Stops
axes_flat[2].set_title('Mean # of Stops', fontsize=12)
axes_flat[3].plot(epsilon_values, good_steps, 'b-o', linewidth=2, markersize=8)#good steps
axes_flat[3].set_title('Mean # of Good Steps', fontsize=12)
axes_flat[4].plot(epsilon_values, unique_states, 'm-o', linewidth=2, markersize=8)
axes_flat[4].set_title('Mean # of States Visited', fontsize=12) # states visited
axes_flat[5].axis('off') # hiding since no plot
plt.tight_layout()
plt.show()