import os
from recbole.quick_start import load_data_and_model
from recbole.trainer import Trainer

def get_performance_evaluation(model_path: str, test_set: list[str]) -> list[str]:
    # TODO: verify which config to load
    _, model, dataset, _, _, _ = load_data_and_model(model_path)
    parent_dir = os.path.dirname(os.getcwd())
    config_path = os.path.join(parent_dir, "config", "model_type_2_config.yaml")
    items_id = [dataset.token2id(field="Key_product", tokens=item).to(model.device) for item in test_set]
    try:
        trainer = Trainer(config_path, model)
        scores = trainer.evaluate(items_id)
        # scores = full_sort_topk([user_id], model, products_id, k, device=torch.cuda.device(0) if torch.cuda.is_available() else 'cpu')	
        print(f"Prediction completed:\n{scores}")
        return scores.tolist()
    except Exception as e:
        print(f"Prediction error:\n{e}")
        return []
