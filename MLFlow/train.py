import mlflow
from model1 import *

mlflow.set_tracking_uri("http://127.0.0.1:5000/")
mlflow.set_experiment("stock_trade")
mlflow.autolog()


def train(ticker, start_date, end_date, download_start, save_path):
    data = process_data(ticker, download_start, end_date, start_date)
    num_episodes = len(data)
    
    env = StockTradingEnv(ticker=ticker, start=download_start, end=end_date, real_start=start_date)
    agent = QLearningAgent(env)
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
        cumulative_return = (final_net_worth - initial_balance) / initial_balance * 100
        print(f"Final Net Worth: {final_net_worth}")
        print(f"Cumulative Return: {cumulative_return:.2f}%")
        
        agent.save_model(save_path)
        
        mlflow.log_metric('final_net_worth', final_net_worth)
        mlflow.log_metric('cumulative_return', cumulative_return)
        
        mlflow.log_artifact(save_path)


# if __name__ == '__main__':
#     train()