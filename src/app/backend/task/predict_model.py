from recbole.quick_start import load_data_and_model
from task.utils import make_interaction_df, get_products_from_tokens
import os
import torch

config_path = os.path.join(os.getcwd(), "config", "model_type_2_predict_config.yaml")

def get_past_interacted_items_tokens(dataset, user_token: str) -> list[str]:
    user_id = dataset.token2id(field="K_MEMBER", tokens=user_token)
    hist, _, _ = dataset.history_item_matrix()
    interacted_item_ids_tensor = hist[user_id].tolist()
    interacted_item_ids = [item_id for _, item_id in enumerate(interacted_item_ids_tensor) if item_id != 0]
    items_tokens = dataset.id2token(field="Key_product", ids=interacted_item_ids)

    return items_tokens


def get_top_k_recommendations_explained(model_path: str, k: int, user_token: str, current_item_tokens: list[str]) -> list[tuple]:
    config, model, dataset, _, _, _ = load_data_and_model(model_file=model_path)
    print(f"dataset: {dataset}")

    interactions = make_interaction_df(config, dataset, user_token, current_item_tokens)

    model.eval()
    with torch.no_grad():
        scores = model.full_sort_predict(interactions).to(config['device'])
        
    topk_scores, topk_indices = torch.topk(scores, k)
    topk_item_ids = topk_indices.cpu().numpy().tolist()[0]
    topk_scores_list = topk_scores.cpu().numpy().tolist()[0]

    topk_tokens = [dataset.id2token("Key_product", id_) for id_ in topk_item_ids]
    recommended_items_descriptions = get_products_from_tokens(topk_tokens)

    recommendations = [{
        "token": item['token'],
        "description": item['description'],
        "score": score
    } for item, score in zip(recommended_items_descriptions, topk_scores_list)]

    past_tokens = get_past_interacted_items_tokens(dataset, user_token)
    past_items = get_products_from_tokens(past_tokens)

    response = {
        "user_token": user_token,
        "recommendations": recommendations,
        "past_interactions": past_items
    }

    return response