from google.genai import types


class RAG:

    @staticmethod
    def ask(question, vector_db, client):

        # Create retriever with MMR for better semantic search
        retriever = vector_db.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 5,
                "fetch_k": 20
            }
        )

        # Retrieve relevant chunks
        docs = retriever.invoke(question)

        # Combine retrieved chunks into context
        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        # Debug: Print retrieved chunks
        print("=" * 80)
        print(f"QUESTION: {question}")

        for i, doc in enumerate(docs):
            print(f"\n----- Chunk {i+1} -----")
            print(doc.page_content)

        print("=" * 80)

        # Prompt
        prompt = f"""
You are an AI Study Assistant.

Answer ONLY using the provided context.

Instructions:
- Use only the information from the context.
- If the answer is partially available, provide the available information.
- Do not make up or assume facts.
- If the context contains no relevant information, reply exactly:
"I couldn't find this information in the uploaded notes."

Context:
{context}

Question:
{question}
"""

        # Generate response
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3
            ),
        )

        return response.text, docs