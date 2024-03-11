from typing import List, Optional
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
    UNKNOWN = 'UNKNOWN'

class TaskStatusResponse(BaseModel):
    status: TaskStatus
    task_id: str

class PredictResponse(TaskStatusResponse):
    result: Optional[List[str]] = None

class EvaluateResponse(TaskStatusResponse):
    result: Optional[dict] = None

class TrainResponse(TaskStatusResponse):
    result: Optional[bool] = None

class TaskNotFoundResponse(TaskStatusResponse):
    result: str