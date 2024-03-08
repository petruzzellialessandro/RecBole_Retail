import os
from .utils import find_latest_model
from .predict_model import get_top_k_recommendations
from .test_model import get_performance_evaluation
from .train_model import start_training
from .make_embedding import MakeEmbedding
from .make_description_embedding import MakeDescriptionEmbedding

from .worker import app

current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
models_path = os.path.join(parent_dir, "models", "type_2")

@app.task(bind=True, name="predict_task", track_started=True)
def predict_task(self, model_name: str, k: int, user_token: str, shopping_cart_tokens: list[str]) -> dict[str, str]:
    latest_model_path = find_latest_model(models_path, model_name)
    predictions = get_top_k_recommendations(latest_model_path, k, user_token, shopping_cart_tokens)
    response = {
        'task_id': predictions.id,
        'status': 'completed',
        'result': predictions
    }
    return response

@app.task(bind=True, name="evaluate_task", track_started=True)
def evaluate_task(self, model_name: str, test_set: list[str]) -> dict[str, str]:
    latest_model_path = find_latest_model(models_path, model_name)
    evaluation = get_performance_evaluation(latest_model_path, test_set)
    response = {
        'task_id': evaluation.id,
        'status': 'completed',
        'result': evaluation
    }
    return response

@app.task(bind=True, name="train_task", track_started=True)
def train_task(self, model_name: str) -> dict[str, str]:
    # MakeEmbedding.create_embedding()
    # MakeDescriptionEmbedding.create_description_embedding()
    start_training(model_name)
    response = {
        'task_id': model_name,
        'status': 'completed'
    }
    return response
