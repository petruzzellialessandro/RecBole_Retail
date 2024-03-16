from recbole.quick_start import load_data_and_model
from task.utils import find_latest_model, make_interaction_df
import os
import torch

def get_top_k_recommendations(model_path: str, k: int, user_token: str, item_tokens: list[str]) -> list[int]:
    config, model, dataset, _, _, _ = load_data_and_model(model_file=model_path)

    print(f"\nUser token: {user_token}\nItem tokens: {item_tokens}\nK: {k}\n")

    config['load_col']['inter'] = dict()
    config['load_col']['inter'] = ['K_MEMBER', 'Key_product']
    config['train_neg_sample_args'] = dict()
    config['train_neg_sample_args']['uniform'] = 1 
    config['device'] = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    interactions = make_interaction_df(config, dataset, user_token, item_tokens)
    print(interactions)

    model.eval()
    with torch.no_grad():
        scores = model.full_sort_predict(interactions).to(config['device'])
    
    topk_scores, topk_indices = torch.topk(scores, k)
    topk_item_ids = topk_indices.cpu().numpy().tolist()
    topk_item_tokens = [dataset.id2token("Key_product", id_) for id_ in topk_item_ids]

    print(f"Top k scores: {topk_scores}\nTop k item ids: {topk_item_ids}\nTop k item tokens: {topk_item_tokens}")
    topk_item_tokens_list = topk_item_tokens[0].tolist()
    
    return topk_item_tokens_list

if __name__ == "__main__":
    current_dir = os.getcwd()
    models_path = os.path.join(current_dir, "models", "type_2")
    latest_model_path = find_latest_model(models_path, 'GRU4Rec')
    print(f"\nLatest model path: {latest_model_path}\n")
    k = 3
    user_token = "34779518"
    item_tokens = ["6482150","6482152","6482153","6482154"]
    results = get_top_k_recommendations(latest_model_path, k, user_token, item_tokens)
    print(results)