# Recbole Retail App

## Preliminaries
This app provides a Python backend server that exposes a REST API for interacting with the model. To test the functionalities, you can use the accompanying Frontend app.
REST API URL: http://127.0.0.1:8000/docs

## Backend
To set up the backend, follow these steps:
- Create a Python virtual environment.
    ```
    python -m venv venv
    ```
- Activate the virtual environment.
    On Unix or MacOS, run:
    ```
    source venv/bin/activate
    ```
    On Windows, run:
    ```
    .\venv\Scripts\activate
    ```
- Install the requirements specified in both the "models" and "backend" folders with "pip install -r requirements.txt".
    ```
    pip install -r models/requirements.txt
    ```
    For the "backend" folder, run:
    ```
    pip install -r backend/requirements.txt
    ```
- Run the `run.sh` script for Unix/Linux or the `run.bat` script for Windows, depending on your system configuration.

## Frontend
To set up the frontend, follow these steps:
- Install NodeJS version 18.17.1.
- Run `npm install` within the "frontend" folder.
- Run `npm start` to launch the frontend application.