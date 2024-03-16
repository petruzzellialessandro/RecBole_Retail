from logging import getLogger
from recbole.config import Config
from recbole.data import create_dataset
from recbole.data.utils import create_samplers, get_dataloader
from recbole.quick_start import load_data_and_model
from recbole.trainer import Trainer
from recbole.utils import init_seed, init_logger, get_trainer
import os

config_path = os.path.join(os.getcwd(), "config", "model_type_2_test_config.yaml")

def get_performance_evaluation(model_name: str, model_path: str) -> list[str]:

    dataset_name = "RECEIPT_LINES_TEST"
    print(f"Model name: {model_name}\nModel path: {model_path}\nConfig path: {config_path}")
    config = Config(model=model_name, dataset=dataset_name, config_file_list=[config_path])
    logger = getLogger()
    init_logger(config)
    logger.info(config)
    print(f"Config: {config}")

    init_seed(config["seed"], config["reproducibility"])

    dataset = create_dataset(config)
    built_dataset = dataset.build()

    _, _, test_sampler = create_samplers(
        config,
        dataset,
        built_dataset
    )
    print(f"Test sampler: {test_sampler}")

    test_data = get_dataloader(config, "test")(
        config, dataset, test_sampler, shuffle=False
    )
    logger.info(f"Test sampler: {test_data}")
    print(f"Test data: {test_data._dataset}")
    
    _, model, _, _, _, _ = load_data_and_model(model_path)
    
    trainer = get_trainer(config["MODEL_TYPE"], model_name)(config, model)
    print(f"Model path: {model_path}")
    # trainer.resume_checkpoint(model_path)

    test_result = trainer.evaluate(test_data, model_file=model_path, show_progress=True, load_best_model=True)
    logger.info(test_result)

    print(f"Evaluation completed:\n{test_result}")
    return test_result
