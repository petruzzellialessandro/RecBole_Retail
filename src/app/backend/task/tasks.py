from task.make_embedding import MakeEmbedding
from task.predict_model import get_top_k_recommendations_explained
from task.test_model import get_performance_evaluation
from task.train_model import start_training
from task.utils import find_latest_model
from task.worker import app

@app.task(bind=True, name="predict_task", track_started=True)
def predict_task(self, model_name: str, k: int, user_token: str, current_item_tokens: list[str]) -> dict[str, str]:
    try:
        latest_model_path = find_latest_model(model_name)
        predict_response = get_top_k_recommendations_explained(latest_model_path, k, user_token, current_item_tokens)
    except Exception as e:
        predict_response = {
            "error": str(e)
        }
    print(f"Predict response: {predict_response}")
    return predict_response

@app.task(bind=True, name="evaluate_task", track_started=True)
def evaluate_task(self, model_name: str) -> dict[str, str]:
    try:
        makeEmbedding = MakeEmbedding()
        makeEmbedding.create_embedding("RECEIPT_LINES_TEST")
        latest_model_path = find_latest_model(model_name)
        evaluate_results = get_performance_evaluation(model_name, latest_model_path)
    except Exception as e:
        evaluate_results = {
            "error": str(e.msg)
        }
    print(f"Evaluate results: {evaluate_results}")
    return evaluate_results

@app.task(bind=True, name="train_task", track_started=True)
def train_task(self, model_name: str) -> bool:
    try:
        # embedding_creator = MakeEmbedding()
        # embedding_creator.create_embedding()
        # MakeDescriptionEmbedding.create_description_embedding()
        train_results = start_training(model_name)
    except Exception as e:
        train_results = {
            "error": str(e)
        }
    print(f"Train results: {train_results}")
    return train_results

if __name__ == "__main__":
    latest_model_path = find_latest_model("GRU4Rec")
    get_performance_evaluation(latest_model_path)
    