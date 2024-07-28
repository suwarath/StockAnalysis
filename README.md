# Stock Analysis

## Objective
The objective of this model is to develop a reinforcement learning (RL) system for making stock trading decisions (buy, sell, hold) based on historical and current stock data.

1. **Environment:**
   A custom gym environment that simulates stock trading by providing observations such as stock prices, volume, MACD (Moving Average Convergence Divergence) indicators, and OBV (On-Balance Volume).
2. **Agent:**
   Utilizes Q-learning to learn optimal trading actions by updating its Q-table based on the rewards received from actions taken in the environment.
3. **Model Training:**
   Train the model using historical stock data, running multiple episodes to refine the agent's policy.
4. **Evaluation:**
   Assess the model's performance through cumulative returns and rewards.
5. **Key Components:**
   * **State Representation:** Includes stock prices, trading volume, MACD indicators, and OBV.
   * **Action Space:** Discrete actions representing selling, holding, or buying the stock
   * **Reward Function:** Based on changes in net worth from the trading actions.

This model aims to make informed, data-driven trading decisions using technical indicators and reinforcement learning strategies.

## Tech Stack
This project was developed locally and used the following tech stack for development
* Python 3.11
* Qlearning (gym)
* Prefect
* MLFlow
* Evidently
* Docker
* Makefile

## Prerequisites
Ensure you have the following installed before running the project:
## Prerequisites
Ensure you have the following installed before running the project:

1. **Python 3.11**  
   [Download and install Python 3.11](https://www.python.org/downloads/release/python-3110/)

2. **pipenv**  
   Install pipenv using pip:
   ```sh
   pip install pipenv
   ```
   [pipenv documentation](https://pipenv.pypa.io/en/latest/)

3. **make**
   * **Windows**: Install make using [Chocolatey](https://community.chocolatey.org/packages/make)
   * **macOS**: Make is already installed as a default. However, you might need to download XCode from Appstore if the error about xcode.
   * **Linux**: Install make using your pakage manager  
   ```sh
   sudo apt-get install make
   ```
4. **docker**   
   [Download and install Docker](https://docs.docker.com/get-docker/)

## How to run the project
1. **Clone the stock analysis repository locally:**  
   ```sh
   git clone https://github.com/suwarath/StockAnalysis
   ```

2. **Setup the environment:**   
   Change directory to where you save the repo and run following command to set up the virtual environment and installs the necessary dependencies.
   ```sh
   make setup
   ```

3. **Start ML flow:**
   ```sh
   make mlflow
   ```
   MLflow will be started, and you can access it at http://localhost:8080

4. **Start Prefect:**
   ```sh
   make prefect
   ```
   Prefect will be started, and you can access it at http://localhost:4200

5. **Start Evidently Dashboard**
   ```sh
   make evidently
   ```
   The Evidently dashboardwill be started, and you can access it at http://localhost:8000

6. **Train, log, register the best model in MLflow, and deploy to Prefect:**
   ```sh
   make deploy
   ```
   This command will train the model, log the results, register the best model in MLflow, and deploy the pipeline to Prefect.

   After deploying, you can access the pipeline via http://localhost:4200 and run the deployed flow using the Prefect UI.

7. **Start the service:**
   ```sh
   make service
   ```
   This command will containerize the web service and run the docker service.
   
8. **Run unit tests:**
   ```sh
   make unit-test
   ```
   This command will run the unit tests to ensure the functionality of individual components.
9. **Run integration tests:**
    ```sh
    make integration-test
    ```
    This command will run the integration tests to ensure the Docker service and Evidently work together as expected.
    
    After running, the Evidently dashboard will be updated, and the service will be logged.

10. **Run dummy monitoring (Optional):**
    ```sh
    make dummy-monitoring
    ```
    This command will simulate monitoring for the model during January 2024.
11. **Format the code using black, isort, and pylint**
    ```sh
    make format
    ```
    This command will format the code using black, isort, and pylint.
12. **Clean the environment:**
    ```sh
    make clean
    ```
    This command will clean up the environment, stoping docker service and removing .venv, mlflow.db, mlruns, and evidently workspace.