export PIPENV_VENV_IN_PROJECT := 1
export PIPENV_VERBOSITY := -1

prerequisites:
	@echo "Building Python environment and unzipping dataset"
	pip install --upgrade pipenv
	pipenv install --python 3.11

mlflow:
	@echo "Running mlflow ui"
	pipenv run mlflow ui --backend-store-uri sqlite:///mlflow.db

prefect:
	@echo "Starting Prefect server"
	pipenv run prefect server start

deploy: 
	@echo "Running train and deploy"
	pipenv run ./workflow/train_and_deploy.py

monitoring:
	@echo "Starting evidently dashboard"
	pipenv run docker-compose -f ./monitoring/docker-compose.yaml up --build

web-service:
	@echo "Creating docker container for model deployment (as web service)"
	pipenv run docker build -f ./web-service/Dockerfile -t housing-price-prediction-service:v1

test:

clean:
	@echo "Cleaning"
	rm -rf __pycache__
	rm -rf evidently
	rm -rf mlruns
	rm -rf mlflow.db
	pipenv --rm

code:
	@echo "Code formatting with black, isort, and pylint"
	black .
	isort .
	pylint --recursive=y .