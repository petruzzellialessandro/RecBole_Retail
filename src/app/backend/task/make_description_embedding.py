import os
import pandas as pd
import numpy as np
import re
import uuid
import yaml
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from numpy.linalg import norm
from openai import OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
from IPython.display import clear_output
import string
import time

class MakeDescriptionEmbedding:
    """
    A class to manage the processing, fetching, and updating of product descriptions
    using Word2Vec and TF-IDF models. It encapsulates functionalities for
    loading products, fetching descriptions from a language model, preprocessing text,
    and recommending products based on their descriptions.

    Attributes:
    config (dict): Configuration settings loaded from a YAML file.
    client (OpenAI): OpenAI client for interacting with the language model.
    model_w2v (Word2Vec): Word2Vec model for generating word embeddings.
    tfidf_vectorizer (TfidfVectorizer): TF-IDF vectorizer for text data.
    products (pd.DataFrame): DataFrame containing product information.
    """
    def __init__(self, config_path: str):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        self.products_file = self.config['products_file']
        self.data_file = self.config['data_file']
        self.product_description_field = self.config['product_description_field']
        self.openai_model = self.config['openai_model']
        self.word2vec_model_path = self.config['word2vec_model_path']
        self.embedding_size = self.config['embedding_size']

        self.client = OpenAI(api_key=os.environ.get('openai_api_key'))
        self.model_w2v = None
        self.tfidf_vectorizer = None
        self.products = self.load_products(self.products_file)

    def load_products(self, products_file: str) -> pd.DataFrame:
        """
        Loads products from a file or creates a DataFrame from a source file.

        Parameters:
        products_file (str): Path to the products file.

        Returns:
        pd.DataFrame: DataFrame containing products.
        """
        if os.path.isfile(products_file):
            return pd.read_pickle(products_file)
        else:
            return self.make_df(self.data_file, 
                                products_file, 
                                self.product_description_field)
    
    def create_description_embedding(self):
        self.batch_fetch(self.products)
        self.products['processed_description'] = self.products['description'].apply(self.preprocess_text)
        corpus_w2v = self.products['processed_description'].tolist()

        model_w2v = Word2Vec(sentences=corpus_w2v, vector_size=self.embedding_size, window=5, min_count=2, workers=4)
        model_w2v.save(self.word2vec_model_path)

        corpus_tfidf = [" ".join(doc) for doc in corpus_w2v]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus_tfidf)
        feature_names = vectorizer.get_feature_names_out()
        self.products['tokens'] = corpus_tfidf

        word_tfidf_dict = {}
        for word in feature_names:
            word_index = vectorizer.vocabulary_[word]
            word_tfidf = tfidf_matrix[:, word_index].toarray()
            word_tfidf_dict[word] = np.mean(word_tfidf)

        # Compute the weighted document vectors
        self.products['description_word2vec'] = self.products['processed_description'].apply(lambda doc: self.weighted_document_vector(doc, model_w2v, word_tfidf_dict))
        pd.to_pickle(self.products, self.products_file)
        return self.products

    def make_df(self, source_file: str, target_file: str, attribute: str) -> pd.DataFrame:
        """
        Creates a DataFrame from a source file, processes it to remove unidentified items, 
        and saves the resulting DataFrame to a target file. Each item in the DataFrame 
        is assigned a unique ID.

        Parameters:
        source_file (str): Path to the source file containing the data.
        target_file (str): Path where the processed DataFrame should be saved.
        attribute (str): Attribute name in the source DataFrame to be processed.

        Returns:
        DataFrame: A DataFrame with unique IDs, names of the items, 
                and placeholders for descriptions and tokens.

        Throws:
        FileNotFoundError: If the source_file does not exist.
        """
        df = pd.read_pickle(source_file)
        all_items = df[attribute].drop_duplicates()
        pattern = re.compile(r'^[^a-zA-Z]*$')
        identified_items = [item for item in all_items if not pattern.match(item)]
        data = [{'id': uuid.uuid4().hex, 'name': item, 'description': '', 'tokens': ''} for item in identified_items]
        items_df = pd.DataFrame(data)
        pd.to_pickle(items_df, target_file)
        return items_df

    def answer_to_dict(self, answers: str) -> dict:
        """
        Converts a text string containing item descriptions in a specific format into a dictionary.
        The format is expected to be '<id>:<description>'.

        Parameters:
        text (str): String containing item descriptions.

        Returns:
        dict: A dictionary where each key is an item ID and each value is the corresponding description.
        """
        pattern = re.compile(r'([a-f0-9]+):(.*?)(?=\n|$)')
        matches = pattern.findall(answers)
        return {id.strip(): description.strip() for id, description in matches}

    def update_products_with_descriptions(self, updates_dict: dict) -> None:
        """
        Updates a DataFrame of products with descriptions provided in a dictionary format.

        Parameters:
        products (DataFrame): The DataFrame of products to be updated.
        dict (dict): Dictionary containing item IDs as keys and descriptions as values.

        Returns:
        DataFrame: Updated DataFrame with descriptions added to the corresponding products.
        """
        for key, value in updates_dict.items():
            self.products.loc[self.products['id'] == key, 'description'] = value

    def fetch_descriptions(self, items: pd.DataFrame, max_words=15, temperature=0.2) -> str:
        """
        Fetches descriptions for a list of products using a language model. Generates prompts 
        for each product and retrieves responses from the model.

        Parameters:
        items (DataFrame): DataFrame containing product IDs and names.
        max_words (int, optional): Maximum number of words for each description.
        temperature (float, optional): Controls the randomness of the model's responses.

        Returns:
        list: A list containing the model's responses in the specified format.

        Throws:
        Exception: If there is an error in making the API request.
        """
        context_message = {
            "role": "system",
            "content": f"Given a list products with format of 'id: name', for each id write a description in english language of {max_words} words length. Focus of its specific benefits and unique features. Reply when you have all answers. Format your response as list of 'id: description'."
        }
        prompts = [{"role": "user", "content": f"{row['id']}: {row['name']}"} for index, row in items.iterrows()]
        prompts.insert(0, context_message)
        response = self.client.chat.completions.create(
            model=self.openai_model,
            messages=prompts,
            temperature=temperature,
        )
        if response and hasattr(response, 'choices'):
            return response.choices[0].message.content.strip()
        else:
            raise Exception("Invalid API response")

    def batch_fetch(self, df: pd.DataFrame, batch_size=10, max_response_words=15, max_retries=3, retry_delay=5) -> pd.DataFrame:
        """
        Processes items in batches to fetch descriptions. Handles retries and updates the items 
        with the fetched descriptions.

        Parameters:
        df (DataFrame): Dataframe containing product details including 'id' and 'name'.
        batch_size (int, optional): Number of items to process in each batch.
        max_response_words (int, optional): Maximum number of words for each response.
        max_retries (int, optional): Maximum number of retry attempts for fetching descriptions.
        retry_delay (int, optional): Delay between retries in seconds.

        Throws:
        Exception: If there is an error in batch processing or fetching descriptions.
        """
        items = df.copy()
        descriptionless_items = items[(items.str.len() < 80)]
        attempts = 0
        while len(descriptionless_items) > 0 and attempts <= max_retries:
            try:
                batch = descriptionless_items.sample(min(len(descriptionless_items), batch_size))
                answers = self.fetch_descriptions(batch, max_response_words)
                description_dict = self.answer_to_dict(answers)
                self.update_products_with_descriptions(description_dict)

                clear_output(wait=True)
                time.sleep(retry_delay)
                descriptionless_items = items[(items.str.len() < 80)]

            except Exception as e:
                print(f"Get batch descriptions exception:\n{e}")
                attempts += 1
                time.sleep(retry_delay)
            if attempts > max_retries:
                print("Max attempts reached. Aborting.")
                break
        return items

    def preprocess_text(self, text: str) -> list:
        """
        Processes a given text by converting it to lowercase, removing punctuation,
        and filtering out stopwords.

        Parameters:
        text (str): The text string to be preprocessed.

        Returns:
        list: A list of words (tokens) after preprocessing the text.
        """

        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        words = word_tokenize(text)
        return [word for word in words if word not in stopwords.words('english')]

    def train_word2vec(self, processed_texts: list):
        """
        Trains the Word2Vec model on the provided processed text data.

        Parameters:
        processed_texts (list): A list of processed texts, where each text is a list of words.

        Description:
        This function initializes and trains a Word2Vec model using the provided processed
        texts. The trained model is stored in the `model_w2v` attribute of the class.
        """
        self.model_w2v = Word2Vec(sentences=processed_texts, vector_size=100, window=5, min_count=2, workers=4)
        self.model_w2v.save(self.word2vec_model_path)

    def train_tfidf(self, processed_texts: list):
        """
        Trains the TF-IDF vectorizer on the provided processed text data and returns the TF-IDF matrix.

        Parameters:
        processed_texts (list): A list of processed texts, where each text is a list of words.

        Returns:
        scipy.sparse.csr.csr_matrix: The TF-IDF matrix obtained from the processed texts.

        Description:
        This function constructs a corpus from the processed texts and then initializes
        and trains a TfidfVectorizer. The TF-IDF matrix generated from the vectorizer
        is returned. The trained vectorizer is stored in the `tfidf_vectorizer` attribute
        of the class.
        """
        corpus_tfidf = [" ".join(doc) for doc in processed_texts]
        self.tfidf_vectorizer = TfidfVectorizer()
        return self.tfidf_vectorizer.fit_transform(corpus_tfidf)

    def weighted_word_vector(self, word: str) -> np.ndarray:
        """
        Computes the weighted vector for a given word using Word2Vec and TF-IDF weights.

        Parameters:
        word (str): The word for which the vector is to be computed.
        model_w2v (Word2Vec model): Pre-trained Word2Vec model.
        word_tfidf (dict): Dictionary of TF-IDF weights with words as keys.

        Returns:
        numpy.ndarray: The weighted vector for the given word. Returns a zero vector 
                    if the word is not in the Word2Vec model or the TF-IDF dictionary.
        """
        if word in self.model_w2v.wv and word in self.tfidf_vectorizer.vocabulary_:
            word_index = self.tfidf_vectorizer.vocabulary_[word]
            word_tfidf = self.tfidf_vectorizer.idf_[word_index]
            return self.model_w2v.wv[word] * word_tfidf
        else:
            return np.zeros(self.model_w2v.vector_size)

    def weighted_document_vector(self, doc: list) -> np.ndarray:
        """
        Computes the weighted document vector by aggregating the weighted word vectors
        of all the words in the document.

        Parameters:
        doc (list): List of words in the document.
        model_w2v (Word2Vec model): Pre-trained Word2Vec model.
        tfidf_vector (dict): Dictionary of TF-IDF weights with words as keys.

        Returns:
        numpy.ndarray: Aggregated weighted vector representing the document.
        """
        doc_vector = np.zeros(self.model_w2v.vector_size)
        for word in doc:
            word_vector = self.weighted_word_vector(word)
            doc_vector += word_vector
        return doc_vector / len(doc) if doc else doc_vector

    def cosine_similarity(self, vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        """
        Compute the cosine similarity between two vectors.

        Parameters:
        vec_a (numpy.ndarray): The first vector.
        vec_b (numpy.ndarray): The second vector.

        Returns:
        float: Cosine similarity between vec_a and vec_b. Returns 0 if either vector has zero length.
        """
        if norm(vec_a) == 0 or norm(vec_b) == 0:
            return 0
        return np.dot(vec_a, vec_b) / (norm(vec_a) * norm(vec_b))
    
if __name__ == '__main__':
    root_dir = os.path.dirname(os.getcwd())
    config_path = os.path.join(root_dir, "config", "description_embedding_config.yaml")
    embedding_creator = MakeDescriptionEmbedding(config_path)
    embedding_creator.create_description_embedding()