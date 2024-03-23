from recbole.config import Config
from recbole.data import create_dataset, data_preparation
from recbole.data.utils import create_samplers, get_dataloader
from recbole.utils import init_seed, get_model
import os
import torch
from task.metrics import RecRetailMetrics

CONFIG_TEST_PATH = os.path.join(os.getcwd(), "config", "model_type_2_test_config.yaml")

def get_performance_evaluation(model_name: str, model_path: str):
    checkpoint = torch.load(model_path)

    config_base = checkpoint["config"]
    dataset = create_dataset(config_base)
    base_train_dataset, _, _ = data_preparation(config_base, dataset)

    init_seed(config_base["seed"], config_base["reproducibility"])
    
    config_test = Config(model=model_name, config_file_list=[CONFIG_TEST_PATH])

    test_dataset = create_dataset(config_test)

    test_dataset.field2id_token = dataset.field2token_id
    built_datasets = test_dataset.build()
    
    train_sampler, _, test_sampler = create_samplers(
        config_test,
        test_dataset,
        built_datasets
    )

    train_dataloader = get_dataloader(config_test, "test")(
        config_test, test_dataset, train_sampler, shuffle=False
    )
    test_dataloader = get_dataloader(config_test, "test")(
        config_test, test_dataset, test_sampler, shuffle=False
    )
        
    model = get_model(config_base["model"])(config_base, base_train_dataset.dataset).to(config_base["device"])
    model.load_state_dict(state_dict=checkpoint["state_dict"])
    
    model.eval()
    results_pred = model.full_sort_predict(train_dataloader.dataset[:])

    _, predicted_items_ids = torch.sort(results_pred, descending=True)
    ground_truth = test_dataloader.dataset[:]['Key_product']
    predicted_items = predicted_items_ids
    users = train_dataloader.dataset[:]['K_MEMBER']

    item_popularity = dataset.counter('Key_product')

    recMetrics = RecRetailMetrics(
        predicted_items=predicted_items,
        ground_truth=ground_truth,
        config=config_test,
        users=users,
        total_items=dataset.item_num,
        item_popularity=item_popularity,
    )
    return recMetrics.compute_all_metrics()