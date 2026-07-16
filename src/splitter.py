from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextSplitter:

    @staticmethod
    def split_documents(documents):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=200,
            separators=[
                "\n\n",
                "\n",
                ". ",
                "? ",
                "! ",
                " ",
                ""
            ]
        )

        return splitter.split_documents(documents)