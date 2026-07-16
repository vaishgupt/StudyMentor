from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingModel:

    @staticmethod
    def load_embeddings():

        embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={
                "device": "cpu"
            },
            encode_kwargs={
                "normalize_embeddings": True
            }
        )

        return embeddings