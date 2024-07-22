# Download artifacts from registered model
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri("sqlite:///mlflow.db")
client = MlflowClient()

prd_model_run_id = client.get_model_version_by_alias("stock-trade-action-best-model", "prd").run_id

mlflow.artifacts.download_artifacts(run_id= prd_model_run_id, dst_path = "./web_service/")