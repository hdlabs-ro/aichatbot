import pandas as pd
import faiss

class Retrieval:
    def __init__(self, df_filepath, fields_to_index, embeddings_model):
        self.df = self._read_df(df_filepath)
        self.fields_to_index = fields_to_index
        self.embeddings_model = embeddings_model
        self.index, self.texts = self._setup_index()


    def _read_df(self, df_filepath):
        if df_filepath.endswith('.csv'):
            return pd.read_csv(df_filepath)
        elif df_filepath.endswith('.json'):
            return pd.read_json(df_filepath)

        raise ValueError("Unsupported file format. Use .csv or .json")

    def _setup_index(self):
        texts = self.df.apply(lambda x: Retrieval.row_to_text(x, self.fields_to_index), axis=1).tolist()
        embeddings = self.embeddings_model.encode(texts, convert_to_numpy=True)
        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(embeddings)
        return index, texts

    def search(self, query, threshold=0.4):
        query_emb = self.embeddings_model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(query_emb, k=100)

        results = []
        for score, idx in zip(D[0], I[0]):
            if score >= threshold:
                results.append(self.texts[idx])
        return results

    @staticmethod
    def row_to_text(row, fields_to_index):
        text = ""
        for field in fields_to_index:
            text += f"{field['name']}: {row[field['value']]} "
        return text



