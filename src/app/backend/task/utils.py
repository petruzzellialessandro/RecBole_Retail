from datetime import datetime
from fastapi import HTTPException, UploadFile
import csv
import io
import os
import pandas as pd
import re
import torch
import pickle

# def get_filename_without_extension(path) -> str:
#     basename = os.path.basename(path)
#     filename_without_extension = os.path.splitext(basename)[0]
#     return filename_without_extension

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
    
async def save_raw_data(file: UploadFile) -> str:
    """ Save the raw interactions file."""

    contents = await file.read()
    decoded_contents = io.StringIO(contents.decode('utf-8'))
    df = pd.read_csv(decoded_contents, sep=',')
        
    expected_columns = [
        "Key_product", "Key_receipt", "LINE_NUM", "K_PRODUCT_TYPE",
        "D_PRODUCT", "K_MEMBER", "QUANTITY", "Q_AMOUNT", "Q_DISCOUNT_AMOUNT",
        "T_RECEIPT", "K_DITTA", "hierarchy"
    ]
        
    if not all(column in df.columns for column in expected_columns):
        raise ValueError("File attributes do not match the required ones.")
    
    now = datetime.now()
    filename = f"lines_hier_test-{now.day}-{now.strftime('%b')}-{now.year}-{now.hour}-{now.minute}-{now.second}.pkl"
    save_path = os.path.join(os.getcwd(), "data", "raw")

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    filepath = os.path.join(save_path, filename)

    df.to_pickle(filepath)
    
    print(f"Raw data saved at: {filepath}")
    return filepath

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

def get_products_from_tokens(tokens: list[str]) -> list[str]:
    print(f"Tokens: {tokens}")
    """ Get the descriptions from the tokens."""
    pickle_file_path = os.path.join(os.getcwd(), "data", "raw", "products.pkl")
    df = pd.read_pickle(pickle_file_path)

    tokens_int = [int(token) for token in tokens if token.isdigit()]
    filtered_df = df[df['K_PRODUCT'].isin(tokens_int)][['K_PRODUCT', 'D_PRODUCT']]
    print(f"Filtered df: {filtered_df}")
    descriptions = [f"{row['K_PRODUCT']}: {row['D_PRODUCT']}" for _, row in filtered_df.iterrows()]

    print(f"Descriptions: {descriptions}")
    return descriptions

if __name__ == "__main__":
    current_dir = os.getcwd()
    models_path = os.path.join(current_dir, "models", "type_2")
    latest_model_path = find_latest_model(models_path, "GRU4Rec")
    print(f"Latest model path: {latest_model_path}")