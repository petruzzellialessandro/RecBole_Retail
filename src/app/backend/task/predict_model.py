import os
from recbole.quick_start import load_data_and_model
from recbole.utils.case_study import full_sort_topk
import torch

current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
models_path = os.path.join(parent_dir, "models", "type_2")

def get_top_k_recommendations(model_path: str, k: int, user_token: str, shopping_cart_tokens: list[str]) -> list[str]:
    _, model, dataset, _, _, _ = load_data_and_model(model_path)
    print((f"Model {model} {model_path} {dataset}"))
    if(not model or not dataset):
        print(f"Model {model} {model_path} {dataset} not found")
        raise Exception(f"Model {model} {model_path} {dataset} not found")
    # print(dataset)
    user_id = dataset.token2id(field="K_MEMBER", tokens=user_token).to(model.device)
    items_id = [dataset.token2id(field="Key_product", tokens=item).to(model.device) for item in shopping_cart_tokens]
    # user_tensor = torch.LongTensor([user_id])
    # item_tensor = torch.LongTensor(items_id)
    try:
        # scores = model.forward(user_tensor, item_tensor)
        # top_k_indices = scores.topk(k).indices.tolist()
        scores = full_sort_topk([user_id], model, items_id, k, device=torch.cuda.device(0) if torch.cuda.is_available() else 'cpu')	
        print(f"Prediction completed:\n{scores}")
        return scores.tolist()
    except Exception as e:
        print(f"Prediction error:\n{e}")
        return []
