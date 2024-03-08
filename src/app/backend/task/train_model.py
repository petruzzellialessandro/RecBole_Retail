from recbole.quick_start import run_recbole
import pandas as pd
import os

current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
config_path = os.path.join(parent_dir, "config", "model_type_2_config.yaml")
report_path = os.path.join(parent_dir, "reports" ,"type_2")

def start_training(model: str) -> None:
    dict_results = run_recbole(model=model, config_file_list=[config_path], dataset='RECEIPT_LINES')
    if not os.path.exists(report_path):
        os.mkdir(report_path)
    pd.Series(dict(dict_results['test_result'])).to_json(os.path.join(report_path, "{model}_test.json"), indent=2)
