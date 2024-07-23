import numpy as np
import pandas as pd
import pickle
import gym
from gym import spaces
from model_element.preprocess import *
import math

parameters = ['Close', 'macd', 'macd_diff', 'macd_signal', 'obv']

class StockTradingEnv(gym.Env):
    def __init__(self, ticker, start, end):
        self.data = process_data(ticker, start, end)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(5,))
        self.action_space = spaces.Discrete(3)
        self.max_steps = len(self.data) - 1
        self.reset()

    def reset(self):
        self.current_step = 0
        self.balance = 10000
        self.shares_owned = 0
        self.net_worth = self.balance
        self.max_net_worth = self.balance
        return self._next_observation()

    def _next_observation(self):
        obs = np.array([
            self.data['Close'][self.current_step],
            # self.data['Volume'][self.current_step],
            self.data['macd'][self.current_step],
            self.data['macd_diff'][self.current_step],
            self.data['macd_signal'][self.current_step],
            self.data['obv'][self.current_step]
        ])
        return obs

    def step(self, action):
        assert self.action_space.contains(action)
        
        prev_net_worth = self.net_worth
        # print(f"Date: {self.data['Date'][self.current_step]}")
        if action == 0:  # Sell
            if self.shares_owned > 0:
                self.balance += self.data['price_next_day'][self.current_step] * self.shares_owned
                self.shares_owned = 0
                # print(f"Sell at {self.data['price_next_day'][self.current_step]}")
        
        elif action == 2:  # Buy
            if self.balance >= self.data['price_next_day'][self.current_step]:
                share_buy = math.floor(self.balance / self.data['price_next_day'][self.current_step])
                self.shares_owned += share_buy
                self.balance -= self.data['price_next_day'][self.current_step] * share_buy
        #         print(f"Buy at {self.data['price_next_day'][self.current_step]} * {share_buy}")
                
        # print(f"Balance {self.balance}")
        # print(f"Share owend {self.shares_owned}")
        
        self.net_worth = self.balance + (self.shares_owned * self.data['Close'][self.current_step])
        self.max_net_worth = max(self.max_net_worth, self.net_worth)
        
        self.current_step += 1
        
        done = self.current_step > self.max_steps
        
        if not done:
            obs = self._next_observation()
        else:
            obs = np.zeros_like(self.observation_space.low)
        
        reward = self.net_worth - prev_net_worth
        return obs, reward, done, {}
    
class QLearningAgent:
    def __init__(self, env, learning_rate=0.1, discount_factor=0.99, exploration_rate=1.0, exploration_decay_rate=0.995):
        self.env = env
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay_rate = exploration_decay_rate
        self.q_table = np.zeros((10, 10, 10, 10, 10, env.action_space.n))

    def _discretize_state(self, state):
        state_bounds = [
            (self.env.data['Close'].min(), self.env.data['Close'].max()),
            # (self.env.data['Volume'].min(), self.env.data['Volume'].max()),
            (self.env.data['macd'].min(), self.env.data['macd'].max()),
            (self.env.data['macd_diff'].min(), self.env.data['macd'].max()),
            (self.env.data['macd_signal'].min(), self.env.data['macd'].max()),
            (self.env.data['obv'].min(), self.env.data['obv'].max())
        ]
        discrete_state = []
        state = np.nan_to_num(state)  # Replace NaNs with 0
        for i in range(len(state)):
            if state_bounds[i][0] == state_bounds[i][1]:
                discrete_state.append(0)
            else:
                scaled_value = (state[i] - state_bounds[i][0]) / (state_bounds[i][1] - state_bounds[i][0])
                discrete_value = int(np.clip(scaled_value * (self.q_table.shape[i] - 1), 0, self.q_table.shape[i] - 1))
                discrete_state.append(discrete_value)
        return tuple(discrete_state)

    def choose_action(self, state):
        discrete_state = self._discretize_state(state)
        if np.random.rand() < self.exploration_rate:
            return self.env.action_space.sample()
        else:
            return np.argmax(self.q_table[discrete_state])

    def update_q_table(self, state, action, reward, next_state):
        state_index = self._discretize_state(state)
        next_state_index = self._discretize_state(next_state)
        q_value = self.q_table[state_index][action]
        max_next_q_value = np.max(self.q_table[next_state_index])
        
        new_q_value = (1 - self.learning_rate) * q_value + self.learning_rate * (reward + self.discount_factor * max_next_q_value)
        self.q_table[state_index][action] = new_q_value

    def decay_exploration_rate(self):
        if self.exploration_rate > 0.01:
            self.exploration_rate *= self.exploration_decay_rate