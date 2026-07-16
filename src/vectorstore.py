from langchain_community.vectorstores import FAISS


class VectorStore:

    @staticmethod
    def create(chunks, embeddings):

        vector_db = FAISS.from_documents(
            documents=chunks,
            embedding=embeddings
        )

        return vector_db