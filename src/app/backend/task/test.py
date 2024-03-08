import os
from recbole.quick_start import load_data_and_model
from recbole.utils.case_study import full_sort_topk
import torch
from utils import find_latest_model
from recbole.data import (create_dataset,)

current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
models_path = os.path.join(parent_dir, "models", "type_2")
config_path = os.path.join(parent_dir, "config", "model_type_2_config.yaml")

def get_top_k_recommendations(model_name: str, k: int, user_token: str, shopping_cart_tokens):
    latest_model_path = find_latest_model(models_path, model_name)
    print(f"Model file: {latest_model_path}")
    print(models_path,'GRU4Rec-Mar-07-2024_22-55-35.pth')

    # checkpoint = torch.load(latest_model_path)
    # config = checkpoint["config"]
    dataset = create_dataset(config_path)
    
    # _, model, dataset, _, _, _ = load_data_and_model(latest_model_path)
    # config_path = os.path.join(parent_dir, "config", "model_type_2_config.yaml")
    _, model, _, _, _, _ = load_data_and_model(model_file=latest_model_path)

    user_id = dataset.token2id(field="K_MEMBER", tokens=user_token).to(model.device)
    items_id = [dataset.token2id(field="Key_product", tokens=item).to(model.device) for item in shopping_cart_tokens]

    try:
        # scores = model.forward(user_tensor, item_tensor)
        # top_k_indices = scores.topk(k).indices.tolist()
        scores = full_sort_topk([user_id], model, items_id, k, device=torch.cuda.device(0) if torch.cuda.is_available() else 'cpu')	
        print(f"Prediction completed:\n{scores}")
        return scores.tolist()
    except Exception as e:
        print(f"Prediction error:\n{e}")
        return []

if __name__ == "__main__":
    get_top_k_recommendations("GRU4Rec", 10, 34698943, [6482150, 6482152])