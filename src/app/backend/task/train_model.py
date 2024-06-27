from recbole.quick_start import run_recbole
import pandas as pd
import os

current_dir = os.getcwd()
config_path = os.path.join(current_dir, "config", "model_type_2_config.yaml")
report_path = os.path.join(current_dir, "reports" ,"type_2")

def start_training(model: str) -> None:
    dict_results = run_recbole(model=model, config_file_list=[config_path], dataset='RECEIPT_LINES')
    if not os.path.exists(report_path):
        os.mkdir(report_path)
    pd.Series(dict(dict_results['test_result'])).to_json(os.path.join(report_path, f"{model}_train_evaluation.json"), indent=2)
    return dict_results['test_result']
