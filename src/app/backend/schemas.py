from pydantic import BaseModel
from enum import Enum

class Interaction(BaseModel):
    Key_product: str

class StartTaskResponse(BaseModel):
    task_id: str

class TaskType(str, Enum):
    predict = "predict"
    train = "train"
    evaluate = "evaluate"

class StatusResponse(BaseModel):
    status: str
    task_id: str

class PredictResponse(StatusResponse):
    result: list = []

class EvaluateResponse(StatusResponse):
    result: list = []

class TrainResponse(StatusResponse):
    result: bool