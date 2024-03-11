from typing import List
from pydantic import BaseModel
from enum import Enum

class TaskType(str, Enum):
    PREDICT = "predict"
    TRAIN = "train"
    EVALUATE = "evaluate"

class TaskStatus(Enum):
    PENDING = 'PENDING'
    STARTED = 'STARTED'
    RETRY = 'RETRY'
    FAILURE = 'FAILURE'
    SUCCESS = 'SUCCESS'

class TaskStatusResponse(BaseModel):
    status: str
    task_id: str

class PredictResponse(BaseModel):
    status: str
    task_id: str
    result: List[str] = []

class EvaluateResponse(BaseModel):
    status: str
    result: dict = {}

class TrainResponse(BaseModel):
    status: str
    result: bool