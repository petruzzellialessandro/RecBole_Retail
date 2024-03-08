import os
import pandas as pd

class MakeDataset:
    def __init__(self, raw_data_path=None, processed_data_path=None):
        self.raw_data_path = raw_data_path or os.path.join(os.path.dirname(os.getcwd()), "data", "raw")
        self.processed_data_path = processed_data_path or os.path.join(os.path.dirname(os.getcwd()), "data", "processed")

    def create_atomic_file(self):
        data = pd.read_pickle(os.path.join(self.raw_data_path, 'lines_hier.pkl'))
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

        out_dir_type_1 = os.path.join(self.processed_data_path, 'type_1', 'RECEIPT_LINES')
        if not os.path.exists(out_dir_type_1):
            os.makedirs(out_dir_type_1)
        item.to_csv(os.path.join(out_dir_type_1, 'RECEIPT_LINES.item'), sep='\t', index=False)
        inter.to_csv(os.path.join(out_dir_type_1, 'RECEIPT_LINES.inter'), sep='\t', index=False)

        out_dir_type_2 = os.path.join(self.processed_data_path, 'type_2', 'RECEIPT_LINES')
        if not os.path.exists(out_dir_type_2):
            os.makedirs(out_dir_type_2)
        inter.to_csv(os.path.join(out_dir_type_2, 'RECEIPT_LINES.inter'), sep='\t', index=False)

if __name__ == '__main__':
    dataset_creator = MakeDataset()
    dataset_creator.create_atomic_file()
