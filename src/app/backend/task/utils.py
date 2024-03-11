from datetime import datetime
from fastapi import HTTPException, UploadFile
import csv
import io
import os
import pandas as pd
import re
import torch

def make_interaction_df(config, dataset, user_token: str, item_tokens: list[str]) -> pd.DataFrame:
    """ Create the interaction dataframe."""

    user_id = dataset.token2id(field="K_MEMBER", tokens=user_token)
    item_ids = [dataset.token2id(field="Key_product", tokens=token) for token in item_tokens]

    max_length = config['MAX_ITEM_LIST_LENGTH']
    padded_item_ids = item_ids + [0] * (max_length - len(item_ids))
    input_inter = {
        'user_id': torch.tensor([user_id]),
        'Key_product_list': torch.tensor([padded_item_ids]),
        'item_length': torch.tensor([len(item_ids)]),
    }
    return input_inter

async def read_list_from_csv(file: UploadFile) -> list:
    """ Read the file and return the list of values."""
    try:
        contents = await file.read()
        decoded_contents = io.StringIO(contents.decode('utf-8'))
        csv_reader = csv.reader(decoded_contents, delimiter='\t')
        
        return [row[0] for row in csv_reader]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

def find_latest_model(directory: str, prefix: str) -> str:
    regex_pattern = rf"{prefix}-([A-Za-z]+)-(\d+)-(\d+)_(\d+)-(\d+)-(\d+)\.pth"
    latest_file = None
    latest_time = None

    for file in os.listdir(directory):
        match = re.match(regex_pattern, file, re.IGNORECASE)
        if match:
            month_str, day, year, hour, minute, second = match.groups()
            datetime_str = f"{day} {month_str} {year} {hour}:{minute}:{second}"
            try:
                file_time = datetime.strptime(datetime_str, '%d %b %Y %H:%M:%S')
            except ValueError as e:
                print(f"Something went wrong during model file name conversion {file}: {e}")
                continue

            if latest_time is None or file_time > latest_time:
                latest_file = file
                latest_time = file_time

    return os.path.join(directory, latest_file)