import os
import pandas as pd

class MakeDataset:
    def __init__(self, data=None):
        self.raw_data_path = os.path.join(os.getcwd(), "data", "raw")
        self.processed_data_path = os.path.join(os.getcwd(), "data", "processed")
        self.data = data
        self.name = "RECEIPT_LINES_TEST" if self.data else "RECEIPT_LINES"
        self.dataset_path = None

    def create_dataset_file(self):
        source_path = self.data if self.data else os.path.join(self.raw_data_path, 'lines_hier.pkl')
        data = pd.read_pickle(source_path)
        data['DT_T_RECEIPT'] = data['T_RECEIPT'].astype('datetime64[s]')
        data['TS_T_RECEIPT'] = data['DT_T_RECEIPT'].apply(lambda x: x.timestamp())

        inter = data[['K_MEMBER', 'TS_T_RECEIPT', 'LINE_NUM', 'Key_receipt', 'QUANTITY', 'Q_AMOUNT', 'Q_DISCOUNT_AMOUNT', 'Key_product']]
        item = data[['D_PRODUCT', 'K_PRODUCT_TYPE', 'Key_product', 'hierarchy', 'K_DITTA']]

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

        out_dir_type_1 = os.path.join(self.processed_data_path, 'type_1', self.name)
        if not os.path.exists(out_dir_type_1):
            os.makedirs(out_dir_type_1)
        item.to_csv(os.path.join(out_dir_type_1, f'{self.name}.item'), sep='\t', index=False)
        inter.to_csv(os.path.join(out_dir_type_1, f'{self.name}.inter'), sep='\t', index=False)

        out_dir_type_2 = os.path.join(self.processed_data_path, 'type_2', self.name)
        if not os.path.exists(out_dir_type_2):
            os.makedirs(out_dir_type_2)

        self.dataset_path = os.path.join(out_dir_type_2, f'{self.name}.inter')
        inter.to_csv(self.dataset_path, sep='\t', index=False)
        print(f"Dataset file created at {self.dataset_path}")

# if __name__ == '__main__':
#     dataset_creator = MakeDataset()
#     dataset_creator.create_dataset_file()
