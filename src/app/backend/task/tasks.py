from task.make_embedding import MakeEmbedding
from task.predict_model import get_top_k_recommendations
from task.test_model import get_performance_evaluation
from task.train_model import start_training
from task.utils import find_latest_model
from task.worker import app
import os

current_dir = os.getcwd()
models_path = os.path.join(current_dir, "models", "type_2")

@app.task(bind=True, name="predict_task", track_started=True)
def predict_task(self, model_name: str, k: int, user_token: str, item_tokens: list[str]) -> dict[str, str]:
    latest_model_path = find_latest_model(models_path, model_name)
    top_k = get_top_k_recommendations(latest_model_path, k, user_token, item_tokens)
    return top_k

@app.task(bind=True, name="evaluate_task", track_started=True)
def evaluate_task(self, model_name: str, test_set: list[str]) -> dict[str, str]:
    latest_model_path = find_latest_model(models_path, model_name)
    evaluation = get_performance_evaluation(latest_model_path, test_set)
    response = {
        'status': 'completed',
        'result': evaluation
    }
    return response

@app.task(bind=True, name="train_task", track_started=True)
def train_task(self, model_name: str) -> dict[str, str]:
    MakeEmbedding.create_embedding()
    # MakeDescriptionEmbedding.create_description_embedding()
    start_training(model_name)
    response = {
        'status': 'completed'
    }
    return response
