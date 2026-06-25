# rl-fundamentals-to-rlhf

RL progression from classical search and planning through deep RL
to RLHF fine-tuning of GPT-2 on Databricks Dolly-15k.

## Contents

### Eight Puzzle - Search Algorithms
Implemented BFS, DFS, UCS, Best-First Search, and two A* variants from scratch
to solve the Eight Puzzle. Compared uninformed strategies against heuristic approaches
using misplaced tile count and Manhattan distance heuristics. Tracked depth, path cost,
and max frontier size across all algorithms.

Files: eight_puzzle_search.ipynb, node.py, utils.py

### Frozen Lake - Dynamic Programming
Implemented value iteration and policy iteration on the 8x8 stochastic Frozen Lake
environment. Compared five random policies against the optimal policy derived through
value iteration, with histograms showing goal-reach rates across 100 runs of 10,000
episodes each.

Files: frozen_lake_value_iteration.ipynb

### Snake Game - Q-Learning
Implemented an epsilon-greedy Q-learning agent on a custom Snake environment with a
12-feature binary state space. Trained with epsilon decay and saved the best Q-table.
Ran experiments across five epsilon values (0.1 to 0.9) and plotted returns, apples
eaten, stops, and unique states visited.

Files: Agent.py, QLearning.py, SnakeEnv.py, qtable_2025_9.csv

### Atari Pong - DQN
Implemented Deep Q-Network with experience replay and a separate target network to
stabilize training on Atari Pong. Built the convolutional network architecture and
replay buffer from scratch, then evaluated the trained policy with episode rendering.

Files: Pong_train.ipynb, Pong_eval.ipynb, dqn_core.py

### RLHF with GPT-2
Implemented the full three-step RLHF pipeline on GPT-2 using Databricks Dolly-15k:
Supervised Fine-Tuning, Reward Model Training, and PPO-based policy optimization.
Ran follow-up experiments on generation parameters, prompt engineering strategies,
and training duration to improve output quality.

Files: rlhf_gpt2_pipeline.ipynb, rlhf_gpt2_experiments.ipynb

## Libraries

Python, PyTorch, HuggingFace Transformers, Stable-Baselines3, trl,
gymnasium, numpy, matplotlib

## Goal

To build intuition for RL from the ground up - from hand-coded search and
tabular Q-learning to neural policies and human preference alignment.
