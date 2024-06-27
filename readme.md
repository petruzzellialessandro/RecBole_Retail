# Retail RecBole

## Overview
This project aims to transform the shopping experience in the retail sector through the application of advanced artificial intelligence models.


## Getting Started

- Rename the `sample.env` file into `.env` and fill it with your OpenAI account information. Remember to change the admin credentials to prevent unauthorized access to the training process.
- Install Python from [Python Download Link](https://www.python.org/downloads/).
- Install Docker from [Docker Download Link](https://docs.docker.com/get-docker/).
- Run the `setup_backend_data.py` script placed in the root folder.

    On Windows:
    ```
    python setup_backend_data.py
    ```
    On Unix/Linux/MacOS:
    ```
    python3 setup_backend_data.py
    ```

### Running the Software with Docker (recommended)
To run the software using Docker, follow these steps:

- Start the Docker containers with the command:
    ```
    docker-compose up
    ```

### Running the Software without Docker
If you prefer not to use Docker, you can follow these steps to set up the environment manually:

#### Message Broker Setup
- Install Docker from [Docker Download Link](https://docs.docker.com/get-docker/).
- Download the `Redis` container:
    ```
    docker pull redis
    ```
- Run the container:
    ```
    docker run --name redis -p 6379:6379 -d redis
    ```

#### Backend Setup
- Create a Python virtual environment inside the "src/app/backend" folder:
    ```
    python -m venv venv
    ```
- Activate the virtual environment:
    On Windows:
    ```
    .\venv\Scripts\activate
    ```
    On Unix or MacOS:
    ```
    source venv/bin/activate
    ```
- Install the requirements specified in the "backend" folder:
    ```
    pip install -r backend/requirements.txt -r backend/requirements_torch.txt
    ```
- Depending on your system, run the `run.sh` script for Unix/Linux or the `run.bat` script for Windows to start the backend server.

#### Frontend Setup
- Install NodeJS version 18.17.1 from [NodeJS Download Link](https://nodejs.org/en/download/)
- Inside the "src/app/frontend" folder, install the project dependencies:
    ```
    npm i
    ```
- Start the frontend application:
    ```
    npm start
    ```

## Usage
Visit the page at http://127.0.0.1:3000/ to access the frontend application.
- Start the train process for a model the first time you run the Software and wait for its completion.
- Store the task id to check the status and results later, because it will take a while.
- For testing purposes, you can use the `test_prediction_data.csv` to ask for some user predictions, given a user token, or start an evaluation of the model using the and the `test_evaluation_data.csv` file. Both files are placed in the frontend folder.

## API Documentation

For the API documentation, please visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## CHANGELOG

Details about the previous notebook based implementation can be found [here](README_OLD.md).
Config and data files are placed in their respective root folders.
