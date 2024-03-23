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
    
def find_latest_model(prefix: str, path=None) -> str:
    models_path = path if path else os.path.join(os.getcwd(), "models", "type_2")
    
    regex_pattern = rf"{prefix}-([A-Za-z]+)-(\d+)-(\d+)_(\d+)-(\d+)-(\d+)\.pth"
    latest_file = None
    latest_time = None
    for file in os.listdir(models_path):
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

    if latest_file is not None:
        return os.path.join(models_path, latest_file)
    else:
        return None
    
def get_products_from_tokens(tokens: list[str]) -> list[{str, str}]:
    print(f"Products from item tokens: {tokens}")
    """ Get the descriptions from the tokens."""
    pickle_file_path = os.path.join(os.getcwd(), "data", "raw", "products.pkl")
    df = pd.read_pickle(pickle_file_path)

    tokens_int = [int(token) for token in tokens]
    filtered_df = df[df['K_PRODUCT'].isin(tokens_int)][['K_PRODUCT', 'D_PRODUCT']]
    items = [{'token': str(row['K_PRODUCT']), 'description': row['D_PRODUCT']} for _, row in filtered_df.iterrows()]
    print(f"Products items: {items}")
    return items

def get_ground_truth_from_interactions(dataset) -> list:
    """ Get the ground truth from the interactions."""
    inter = dataset.inter_matrix(form='csr')
    user_item_pairs = []

    for user_id in range(inter.shape[0]):
        start_idx = inter.indptr[user_id]
        end_idx = inter.indptr[user_id + 1]
        item_indices = inter.indices[start_idx:end_idx]
        
        user_item_pairs.extend([(user_id, item_id) for item_id in item_indices])
    return user_item_pairs

if __name__ == "__main__":
    latest_model_path = find_latest_model("GRU4Rec")
    print(f"Latest model path: {latest_model_path}")