from datetime import datetime
from fastapi import UploadFile
import ast
import io
import os
import pandas as pd

DATA_PATH = os.path.join(os.getcwd(), "data")
RAW_DATA_PATH = os.path.join(DATA_PATH, "raw")
PROCESSED_DATA_PATH = os.path.join(DATA_PATH, "processed")

class MakeDataset:
    
    @staticmethod
    def build(name="RECEIPT_LINES", filepath: str = None):
        source_path = filepath if filepath else os.path.join(RAW_DATA_PATH, 'lines_hier.pkl')
        df = pd.read_pickle(source_path)
        df['DT_T_RECEIPT'] = df['T_RECEIPT'].astype('datetime64[s]')
        df['TS_T_RECEIPT'] = df['DT_T_RECEIPT'].apply(lambda x: x.timestamp())

        inter = df[['K_MEMBER', 'TS_T_RECEIPT', 'LINE_NUM', 'Key_receipt', 'QUANTITY', 'Q_AMOUNT', 'Q_DISCOUNT_AMOUNT', 'Key_product']]
        item = df[['D_PRODUCT', 'K_PRODUCT_TYPE', 'Key_product', 'hierarchy', 'K_DITTA']]

        inter = inter.rename(columns={'K_MEMBER': 'K_MEMBER:token',
                                       'TS_T_RECEIPT': 'TS_T_RECEIPT:float',
                                       'LINE_NUM': 'LINE_NUM:float',
                                       'Key_receipt': 'Key_receipt:token',
                                       'QUANTITY': 'QUANTITY:float',
                                       'Q_AMOUNT': 'Q_AMOUNT:float',
                                       'Q_DISCOUNT_AMOUNT': 'Q_DISCOUNT_AMOUNT:float',
                                       'Key_product': 'Key_product:token'})

        item = item.rename(columns={'D_PRODUCT': 'D_PRODUCT:token_seq',
                                     'K_PRODUCT_TYPE': 'K_PRODUCT_TYPE:token',
                                     'Key_product': 'Key_product:token',
                                     'K_DITTA': 'K_DITTA:token',
                                     'hierarchy': 'hierarchy:token_seq'})
        item = item.drop_duplicates("Key_product:token").reset_index(drop=True)

        out_dir_type_1 = os.path.join(PROCESSED_DATA_PATH, 'type_1', name)
        if not os.path.exists(out_dir_type_1):
            os.makedirs(out_dir_type_1)
        item.to_csv(os.path.join(out_dir_type_1, f'{name}.item'), sep='\t', index=False)
        inter.to_csv(os.path.join(out_dir_type_1, f'{name}.inter'), sep='\t', index=False)
        print(f"Dataset files {name}.item and {name}.inter created at {out_dir_type_1}")

        out_dir_type_2 = os.path.join(PROCESSED_DATA_PATH, 'type_2', name)
        if not os.path.exists(out_dir_type_2):
            os.makedirs(out_dir_type_2)

        dataset_path = os.path.join(out_dir_type_2, f'{name}.inter')
        inter.to_csv(dataset_path, sep='\t', index=False)
        print(f"Dataset file {name}.inter created at {dataset_path}")

    @staticmethod
    async def csv_to_pickle(file: UploadFile) -> str:
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
        
        df['hierarchy'] = df['hierarchy'].apply(lambda x: ast.literal_eval(str(x)))
        now = datetime.now()
        filename = f"lines_hier_test-{now.day}-{now.strftime('%b')}-{now.year}-{now.hour}-{now.minute}-{now.second}.pkl"

        if not os.path.exists(RAW_DATA_PATH):
            os.makedirs(RAW_DATA_PATH)
        raw_dataset_path = os.path.join(RAW_DATA_PATH, filename)

        df.to_pickle(raw_dataset_path)
        
        print(f"Raw data saved at: {raw_dataset_path}")
        return raw_dataset_path
