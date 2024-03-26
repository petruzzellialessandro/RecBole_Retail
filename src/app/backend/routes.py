from celery.result import AsyncResult
from fastapi import HTTPException, Form, File, UploadFile, APIRouter
from fastapi.responses import JSONResponse
from http import HTTPStatus
from schemas import TaskNotFoundResponse, TaskStatus, TaskStatusResponse, TaskResponse
from task.make_dataset import MakeDataset
from task.tasks import predict_task, evaluate_task, train_task
from task.utils import read_list_from_csv
from task.worker import app as celery_app
from typing import Union
import os

TRAIN_USER = os.getenv("TRAIN_USERNAME", "admin")
TRAIN_PASS = os.getenv("TRAIN_PASSWORD", "admin")
docs_url = "http://localhost:8000/docs"

main = APIRouter()

@main.get("/", tags=["General"], status_code=HTTPStatus.OK)
def root():
    """ Root endpoint used only as welcome message."""
    return {
        "message": "Welcome to RecBole Retail Recommender System! Please, read the docs!",
        "docs_url": docs_url
    }

@main.post("/predict", tags=["Prediction"], status_code=HTTPStatus.ACCEPTED, response_model=TaskStatusResponse)
async def start_predict_task(user_token: str = Form(...), k: int = Form(10), file: UploadFile = File(...), model: str = Form(...)):
    """ Predict model endpoint used to get the recommendations for the user."""	
    item_tokens = await read_list_from_csv(file)
    task = predict_task.delay(model, k, user_token, item_tokens)
    return {
        "status": task.status,
        "task_id": task.id
    }

@main.post("/evaluate", tags=["Evaluate"], status_code=HTTPStatus.ACCEPTED, response_model=TaskStatusResponse)
async def start_evaluate_task(file: UploadFile = File(...), model: str = Form(...)):
    """ Test model endpoint used to get the performance metrics and evaluate the model drifting."""	
    dataset_path = await MakeDataset.csv_to_pickle(file)
    MakeDataset.build(name='RECEIPT_LINES_TEST', filepath=dataset_path)
    task = evaluate_task.delay(model)
    return {
        "status": task.status,
        "task_id": task.id
    }

@main.post("/train", tags=["Training"], status_code=HTTPStatus.ACCEPTED, response_model=TaskStatusResponse)
async def start_train_task(model: str = Form(...), username: str = Form(...), password: str = Form(...)):
    """ Train model endpoint used to start the training process for the model."""	
    if username != TRAIN_USER or password != TRAIN_PASS:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    task = train_task.delay(model)
    return {
        "status": task.status,
        "task_id": task.id
    }
    
@main.get("/task-status/{task_id}", tags=["Status"], status_code=HTTPStatus.ACCEPTED, response_model=TaskStatusResponse)
async def check_task_status(task_id: str):
    task = AsyncResult(task_id, app=celery_app)
    return {
        "status": task.status,
        "task_id": task_id
    }
    
@main.get("/task-result/{task_id}", tags=["Results"], status_code=HTTPStatus.OK, response_model=Union[TaskNotFoundResponse, TaskResponse], response_class=JSONResponse)
async def get_task_result(task_id: str):
    task = AsyncResult(task_id, app=celery_app)
    try:
        if task.state == "PENDING":
            return TaskNotFoundResponse(status=TaskStatus.UNKNOWN, task_id=task_id, result='Task not started or not existing')    
        else:
            response = {
                "status": task.state,
                "task_id": task_id,
                "result": task.result
            }
    except Exception as e:
        response = {
            "status": TaskStatus.FAILURE,
            "task_id": task_id,
            "result": str(e.error)
        }
    return response