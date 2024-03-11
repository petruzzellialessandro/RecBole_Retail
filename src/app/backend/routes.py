from http import HTTPStatus
from fastapi import HTTPException, Form, File, UploadFile, APIRouter, Response
from schemas import TaskStatus, TaskStatusResponse, TaskType, PredictResponse, EvaluateResponse, TrainResponse
import os
from task.tasks import predict_task, evaluate_task, train_task
from celery.result import AsyncResult
from task.worker import app as celery_app
from task.utils import read_list_from_csv
from fastapi.responses import JSONResponse

from typing import Union

TRAIN_USER = os.getenv("TRAIN_USERNAME", "admin")
TRAIN_PASS = os.getenv("TRAIN_PASSWORD", "admin")

main = APIRouter()

@main.get("/", tags=["General"], status_code=HTTPStatus.OK)
def root():
    """ Root endpoint used only as welcome message."""
    return {"message": "Welcome to RecBole Retail Recommender System! Please, read the `/docs`!"}

@main.post("/predict", tags=["Prediction"], status_code=HTTPStatus.ACCEPTED, response_model=TaskStatusResponse)
async def start_predict_task(user_id: str = Form(...), k: int = Form(10), file: UploadFile = File(...), model: str = Form(...)):
    """ Predict model endpoint used to get the recommendations for the user."""	
    shopping_cart_items = await read_list_from_csv(file)
    task = predict_task.delay(model, k, user_id, shopping_cart_items)
    return {
        "status": TaskStatus.STARTED,
        "task_id": task.id
    }

@main.post("/evaluate", tags=["Evaluate"], status_code=HTTPStatus.ACCEPTED, response_model=TaskStatusResponse)
async def start_predict_task(model: str = Form(...), file: UploadFile = File(...)):
    """ Test model endpoint used to get the performance metrics and evaluate the model drifting."""	
    test_set = await read_list_from_csv(file)
    task = evaluate_task.delay(model, test_set)
    return {
        "status": TaskStatus.STARTED,
        "task_id": task.id
    }

@main.post("/train", tags=["Training"], status_code=HTTPStatus.ACCEPTED, response_model=TaskStatusResponse)
async def start_train_task(model: str = Form(...), username: str = Form(...), password: str = Form(...)):
    """ Train model endpoint used to start the training process for the model."""	
    if username != TRAIN_USER or password != TRAIN_PASS:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    task = train_task.delay(model)
    return {
        "status": TaskStatus.STARTED,
        "task_id": task.id
    }
    
@main.get("/{task_type}/task-status/{task_id}", status_code=HTTPStatus.ACCEPTED, response_model=TaskStatusResponse)
async def check_task_status(task_type: TaskType, task_id: str):
    task = AsyncResult(task_id, app=celery_app)
    return {
        "status": task.status,
        "task_id": task_id
    }
    
@main.get("/{task_type}/task-result/{task_id}", tags=["Results"], status_code=HTTPStatus.OK, response_model=Union[PredictResponse, EvaluateResponse, TrainResponse], response_class=JSONResponse)
async def get_task_result(task_type: TaskType, task_id: str):
    task = AsyncResult(task_id, app=celery_app)
    if task.status == "SUCCESS":
        result = {
            "status": TaskStatus.SUCCESS,
            "task_id": task_id,
            "result": task.result
        }
        
        match task_type:
            case TaskType.PREDICT:
                return PredictResponse(**result)
            case TaskType.EVALUATE:
                return EvaluateResponse(**result)
            case TaskType.TRAIN:
                return TrainResponse(**result)
            case _:
                raise HTTPException(status_code=400, detail="Invalid task type")
    else:
         return TaskStatusResponse(status=TaskStatus.PENDING, task_id=task_id)