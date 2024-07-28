import pickle
import shutil
import importlib

import mlflow

shutil.copy(
    "./workflow/preprocess.py", "./workflow/model_element/preprocess.py"
)

from model_element.preprocess import *


def save_model(self, file_path):
    with open(file_path, "wb") as file:
        pickle.dump(self.q_table, file)


def train_and_log_model(ticker, start_date, end_date, model):
    data = process_data(ticker, start_date, end_date)
    num_episodes = len(data)

    m = importlib.import_module(model)

    env = m.StockTradingEnv(ticker=ticker, start=start_date, end=end_date)
    agent = m.QLearningAgent(env)
    episode_rewards = []
    for episode in range(num_episodes):
        state = env.reset()
        episode_reward = 0
        while True:
            action = agent.choose_action(state)
            next_state, reward, done, _ = env.step(action)
            agent.update_q_table(state, action, reward, next_state)
            state = next_state
            episode_reward += reward
            if done:
                break

        agent.decay_exploration_rate()
        episode_rewards.append(episode_reward)
        print(f"Episode {episode + 1}/{num_episodes}, Reward: {episode_reward}")

    with mlflow.start_run():
        final_net_worth = agent.env.net_worth
        initial_balance = 10000
        cumulative_return = (
            (final_net_worth - initial_balance) / initial_balance * 100
        )
        print(f"Final Net Worth: {final_net_worth}")
        print(f"Cumulative Return: {cumulative_return:.2f}%")

        with open("./workflow/model_element/qtable.bin", "wb") as file:
            pickle.dump(agent.q_table, file)
        shutil.copy(
            f"./workflow/{model}.py", "./workflow/model_element/model.py"
        )

        mlflow.log_param("parameters", m.parameters)
        mlflow.log_metric("final_net_worth", final_net_worth)
        mlflow.log_metric("cumulative_return", cumulative_return)

        mlflow.log_artifact("./workflow/model_element/")
