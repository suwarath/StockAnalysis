export PIPENV_VENV_IN_PROJECT := 1
export PIPENV_VERBOSITY := -1

setup:
	@echo "Building Python environment and unzipping dataset"
	pip3 install --upgrade pipenv
	pipenv install --python 3.11

mlflow:
	@echo "Running mlflow ui. ctrl+c to exit"
	pipenv run mlflow ui --backend-store-uri sqlite:///mlflow.db --port 8080

prefect:
	@echo "Starting Prefect server. ctrl+c to exit"
	pipenv run prefect server start

evidently:
	@echo "Starting evidently dashboard. ctrl+c to exit"
	pipenv run python3 ./monitoring/init_evidently_dashboard.py
	pipenv run evidently ui --workspace ./monitoring/workspace --port 8000

deploy: 
	@echo "Training model and deploying to prefect"
	pipenv run python3 ./workflow/train_and_deploy.py AAPL 2023-01-01 2024-01-01 model1,model2

service:
	@echo "Creating docker container for a web service"
	pipenv run docker build -t get-trade-action-service:v1 .
	pipenv run docker run -it --rm -p 9696:9696 --add-host=host.docker.internal:host-gateway get-trade-action-service:v1

unittest:
	@echo "Running unit test"
	pipenv run pytest ./unit_test/unit_test.py

integrationtest:
	@echo "Runnign unit test"
	pipenv run pytest ./integration_test/test_docker.py

dummymonitoring:
	@echo "Running dummy data for evidently dashboard"
	pipenv run python3 ./monitoring/dummy_monitoring.py  

format:
	@echo "Code formatting with black, isort, and pylint"
	pipenv run black .
	pipenv run isort .
	pipenv run pylint --recursive=y .

clean:
	@echo "Stoping all running docker"
	rm -rf __pycache__
	docker stop $(docker ps -q)
	@echo "Cleaning mlflow"
	rm -rf mlflow.db
	rm -rf mlruns
	@echo "Cleaning evidently"
	rm -rf ./monitoring/workspace/
	@echo "Removing environment"
	pipenv --rm