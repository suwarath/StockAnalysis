import sys
import pickle
import pandas as pd
import os
import configparser
from prefect import task, flow, get_run_logger
from prefect.context import get_run_context
from prefect.deployments import Deployment
import mlflow

from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient

from train import *

EXPERIMENT_NAME = "stock_trade_action"
REGISTER_MODEL_NAME = "stock-trade-action-best-model"

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment(EXPERIMENT_NAME)
mlflow.autolog()


@task(name = "train_and_register_best_model")
def train_and_register_model(ticker, start_date, end_date, models, EXPERIMENT_NAME=EXPERIMENT_NAME, REGISTER_MODEL_NAME=REGISTER_MODEL_NAME):
    logger = get_run_logger()
    
    client = MlflowClient()

    
    logger.info(f'training data and register model for {ticker} from {start_date} to {end_date}')
    for model in models:
        train_and_log_model(ticker, start_date, end_date, model, save_path = f"./models/{model}.bin")
        
    logger.info(f'selecting the best model')
    experiment = client.get_experiment_by_name(EXPERIMENT_NAME)
    best_run = client.search_runs(experiment_ids=experiment.experiment_id,
                                  run_view_type=ViewType.ACTIVE_ONLY,
                                  max_results=1,
                                  order_by=["metrics.cumulative_return DESC"])[0]

    logger.info(f'selecting the best model')
    best_run_id = best_run.info.run_id
    best_model_uri = f"runs:/{best_run_id}/model"
    mlflow.register_model(model_uri=best_model_uri, name= REGISTER_MODEL_NAME)
  
@task(name = "transition_model_to_production")
def transition_model_stage():
    logger = get_run_logger()
    
    client = MlflowClient()
    lastest_mv = client.get_registered_model(name=REGISTER_MODEL_NAME)
    version = lastest_mv.latest_versions[0].version
  
    logger.info(f'transition model {REGISTER_MODEL_NAME} version {version} to production')
    
    client.set_registered_model_alias(
            name=REGISTER_MODEL_NAME,
            alias="prd",
            version= version
        )

@flow
def run():
    ticker = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    models = sys.argv[4].split(',')
    train_and_register_model(ticker, start_date, end_date, models)
    transition_model_stage()

if __name__ == '__main__':
    run()
    
    # Deploy Prefect Flow
    deployment = Deployment.build_from_flow(
        flow = run,
        name= "stock_action_training_flow",
        version=1,
    )
    deployment.apply()