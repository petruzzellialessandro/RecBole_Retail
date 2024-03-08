from http import HTTPStatus
from fastapi import HTTPException, Form, File, UploadFile, APIRouter
from schemas import TaskType, StatusResponse, StartTaskResponse, PredictResponse, EvaluateResponse, TrainResponse
import os
from task.tasks import predict_task, evaluate_task, train_task
from celery.result import AsyncResult
from task.worker import app as celery_app
import io
import csv
from typing import Union

TRAIN_USER = os.getenv("TRAIN_USERNAME", "admin")
TRAIN_PASS = os.getenv("TRAIN_PASSWORD", "admin")

main = APIRouter()

async def read_list_from_csv(file: UploadFile) -> list:
    """ Read the file and return the file storage object."""
    try:
        contents = await file.read()
        decoded_contents = io.StringIO(contents.decode('utf-8'))
        csv_reader = csv.DictReader(decoded_contents, delimiter='\t')
        
        return [row[0] for row in csv_reader]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@main.get("/", tags=["General"], status_code=HTTPStatus.OK)
def root():
    """ Root endpoint used only as welcome message."""
    return {"message": "Welcome to RecBole Retail Recommender System! Please, read the `/docs`!"}

@main.post("/predict", tags=["Prediction"], status_code=HTTPStatus.ACCEPTED, response_model=StartTaskResponse)
async def start_predict_task(model: str = Form(...), k: int = Form(10), user_id: str = Form(...), file: UploadFile = File(...)):
    """ Predict model endpoint used to get the recommendations for the user."""	
    shopping_cart_items = await read_list_from_csv(file)
    task = predict_task.delay(model, k, user_id, shopping_cart_items)
    return {"task_id": task.id}

@main.post("/evaluate", tags=["Evaluate"], status_code=HTTPStatus.ACCEPTED, response_model=StartTaskResponse)
async def start_predict_task(model: str = Form(...), file: UploadFile = File(...)):
    """ Test model endpoint used to get the performance metrics and evaluate the model drifting."""	
    test_set = await read_list_from_csv(file)
    task = evaluate_task.delay(model, test_set)
    return {"task_id": task.id}

@main.post("/train", tags=["Training"], status_code=HTTPStatus.ACCEPTED, response_model=StartTaskResponse)
async def start_train_task(model: str = Form(...), username: str = Form(...), password: str = Form(...)):
    """ Train model endpoint used to start the training process for the model."""	
    if username != TRAIN_USER or password != TRAIN_PASS:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    task = train_task.delay(model)
    return {"task_id": task.id}
    
@main.get("/{task_type}/task-status/{task_id}", status_code=HTTPStatus.ACCEPTED, response_model=StatusResponse)
async def check_task_status(task_type: TaskType, task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if not task_result.ready():
        return {"status": "pending", "task_id": task_id}
    elif task_result.successful():
        return {
            "status": "completed",
            "task_id": task_id,
        }
    elif task_result.failed():
        return {"status": "failed", "task_id": task_id}
    else:
        return {"status": "unknown", "task_id": task_id}

@main.get("/{task_type}/task-result/{task_id}",  response_model=Union[PredictResponse, EvaluateResponse, TrainResponse])
async def get_task_result(task_type: TaskType, task_id: str) -> Union[PredictResponse, EvaluateResponse, TrainResponse]:
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.ready():
        result = task_result.get(timeout=1.0)
        match task_type:
            case TaskType.predict:
                return PredictResponse(status="completed", task_id=task_id, result=result)
            case TaskType.evaluate:
                return EvaluateResponse(status="completed", task_id=task_id, result=result)
            case TaskType.train:
                return TrainResponse(status="completed", task_id=task_id, result=result)
            case _:
                raise HTTPException(status_code=400, detail="Invalid task type")
    else:
         return StatusResponse(status="pending", task_id=task_id)