import os
import torch.nn as nn
import torch
import itertools
import pandas as pd
import os
import numpy as np

class MakeEmbedding:
    def __init__(self, raw_data_path=None, processed_data_path=None):
        self.raw_data_path = raw_data_path or os.path.join(os.getcwd(), "data", "raw")
        self.processed_data_path = processed_data_path or os.path.join(os.getcwd(), "data", "processed")

    def create_embedding(self, file_name="RECEIPT_LINES"):
        HIERARCHY_MAX_LEN = 4
        EMBEDDING_SIZE = 64
        MERGE_METHOD = "sum"

        df = pd.read_pickle(os.path.join(self.raw_data_path, "lines_hier.pkl"))
        df.drop_duplicates(subset=['Key_product'], inplace=True)
        df['hierarchy'] = df['hierarchy'].apply(lambda x: ([0]*HIERARCHY_MAX_LEN + x)[-HIERARCHY_MAX_LEN:])
        df = df.loc[:, ['Key_product', 'D_PRODUCT', 'Q_AMOUNT', 'K_DITTA', 'hierarchy']]
        df.reset_index(drop=True, inplace=True)
        
        has_description = None
        # Merge with description
        try:
            df_description = pd.read_pickle(os.path.join(self.processed_data_path, "df_products_descriptions.pkl"))
            df = pd.merge(df, df_description, left_on='D_PRODUCT', right_on='name', how='left')
            df = df[['Key_product', 'D_PRODUCT', 'description_word2vec', 'Q_AMOUNT', 'K_DITTA', 'hierarchy']]
            has_description = True
        except:
            has_description = False

        # Create the embedding

        mapping_items = {v: i for i, v in enumerate(set(itertools.chain(*df['hierarchy'].tolist())))}
        num_items = len(mapping_items)
        df['mapped_hier'] =  df['hierarchy'].apply(lambda x: torch.IntTensor([mapping_items[y] for y in x]))
        embedding_ = nn.Embedding(num_items, EMBEDDING_SIZE, padding_idx=mapping_items[0])

        # Compute the embedding for each product and merge them

        if MERGE_METHOD == 'sum':
            df['hier_embed'] = df['mapped_hier'].apply(lambda x: embedding_(x).sum(dim=0).detach().numpy().tolist())
        else:
            df['hier_embed'] = df['mapped_hier'].apply(lambda x: embedding_(x).mean(dim=0).detach().numpy().tolist())

        if has_description:
            df = df.loc[:, ['Key_product', 'hier_embed', 'description_word2vec']]
            if MERGE_METHOD == 'sum':
                df['tensor_embed'] = df.apply(lambda x: list(np.array(x['hier_embed']) + np.array(x['description_word2vec'])), axis=1)
            else:
                df['tensor_embed'] = df.apply(lambda x: list(np.mean(np.stack((x['hier_embed'], x['description_word2vec'])), axis=0)), axis=1)
        else:
            df = df.loc[:, ['Key_product', 'hier_embed']]
            df['tensor_embed'] = df['hier_embed']

        # Add the extra embedding for [MASK] and [PAD]

        embedding_extra = nn.Embedding(num_items, EMBEDDING_SIZE)
        extra_embed = pd.DataFrame([{
            'Key_product': '[MASK]',
            'tensor_embed': embedding_extra(torch.IntTensor([0])).detach().numpy().tolist()[0]
        },
        {
            'Key_product': '[PAD]',
            'tensor_embed': embedding_extra(torch.IntTensor([1])).detach().numpy().tolist()[0]
        }])
        df = pd.concat([df, extra_embed]).reset_index(drop=True)

        # Dataframe preparation

        df['tensor_string'] = df['tensor_embed'].astype(str).apply(lambda x: x.replace("[", "").replace("]", "").replace(",", ""))
        df['Key_product'] = df['Key_product'].astype(str)
        df = df.loc[:, ['Key_product', 'tensor_string']].rename(columns={
            'Key_product':'Key_product:token',
            'tensor_string': 'item_emb:float_seq'
        })
        target_dir = os.path.join(self.processed_data_path, "type_2", file_name)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        df.to_csv(os.path.join(target_dir, f"{file_name}.item"), sep="\t", index=False)
        print(f"Embedding created and saved at: {os.path.join(target_dir, f'{file_name}.item')}")
        return df

if __name__ == '__main__':
    embedding_creator = MakeEmbedding()
    embedding_creator.create_embedding()

