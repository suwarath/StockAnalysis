# Download artifacts from registered model
import datetime as dt

import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri("sqlite:///mlflow.db")
client = MlflowClient()

prd_model = client.get_model_version_by_alias(
    "stock-trade-action-best-model", "prd"
)
prd_version = prd_model.version
prd_run_id = prd_model.run_id
run = client.get_run(prd_run_id)
prd_model_metrics = run.data.metrics
prd_model_end_time = dt.datetime.fromtimestamp(
    run.info.end_time / 1000
).strftime("%Y-%m-%d %H:%M:%S.%f")

mlflow.artifacts.download_artifacts(
    run_id=prd_run_id, dst_path="./web_service/"
)

print(
    f"Download model version ({prd_version}) from run id: {prd_run_id} metrics: {prd_model_metrics} trained at: {prd_model_end_time} GMT+7:00"
)
