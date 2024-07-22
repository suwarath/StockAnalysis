import os
import pickle
import click
import mlflow
import sys

from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient

from train import *

EXPERIMENT_NAME = "stock_trade_action"

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment(EXPERIMENT_NAME)
mlflow.autolog()

def run_register_model(ticker, start_date, end_date, models):

    client = MlflowClient()

    # Train and Log the Model
    for model in models:
        train_and_log_model(ticker, start_date, end_date, model, save_path = f"./q_learning_model/{model}.pkl")

    # Select the model with the lowest test RMSE
    experiment = client.get_experiment_by_name(EXPERIMENT_NAME)
    best_run = client.search_runs(experiment_ids=experiment.experiment_id,
                                  run_view_type=ViewType.ACTIVE_ONLY,
                                  max_results=1,
                                  order_by=["metrics.cumulative_return DESC"])[0]

    # Register the best model
    best_run_id = best_run.info.run_id
    best_model_uri = f"runs:/{best_run_id}/model"
    mlflow.register_model(model_uri=best_model_uri, name="stock-trade-action-best-model")

def run():
    ticker = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    models = sys.argv[4].split(',')
    run_register_model(ticker, start_date, end_date, models)

if __name__ == '__main__':
    run()
