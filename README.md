# rl-fundamentals-to-rlhf

RL progression from classical search and planning through deep RL
to RLHF fine-tuning of GPT-2 on Databricks Dolly-15k.

## Contents

### 1 - Eight Puzzle (Search Algorithms)
Implemented A*, BFS, DFS, UCS, and Best-First Search on the Eight Puzzle.
Files: search.ipynb, node.py, utils.py

### 2 - Frozen Lake (Dynamic Programming)
Implemented value iteration and policy iteration on the Frozen Lake environment.
Files: SreejaReddyYeluru.ipynb

### 3 - Snake Game (Q-Learning)
Implemented a Q-learning agent that learns to play Snake from scratch.
Q-table saved after training.
Files: Agent.py, QLearning.py, SnakeEnv.py, qtable_2025_9.csv

### 4 - Atari Pong (DQN)
Implemented Deep Q-Network to play Atari Pong using experience replay
and a target network.
Files: Pong_train.ipynb, Pong_eval.ipynb, dqn_core.py

### 5 - RLHF with GPT-2
Implemented the three-step RLHF pipeline on GPT-2 using Databricks Dolly-15k:
Supervised Fine-Tuning, Reward Model Training, and PPO-based policy optimization.
Part 2 includes improvement experiments on generation parameters, prompt engineering,
and training duration.
Files: Simple_RLHF.ipynb (Part 1), Modifications_Copy of Simple_RLHF.ipynb (Part 2),
HW5Report.pdf

## Libraries

Python, PyTorch, HuggingFace Transformers, Stable-Baselines3, gymnasium,
trl, numpy, matplotlib

## Goal

To build intuition for RL from the ground up from hand-coded search and
tabular Q-learning to neural policies and human preference alignment.
