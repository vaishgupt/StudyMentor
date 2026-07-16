from google.genai import types


class FlashcardGenerator:

    @staticmethod
    def generate(vector_db, client):

        retriever = vector_db.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 8,
                "fetch_k": 30
            }
        )

        docs = retriever.invoke(
            "Generate study flashcards from the uploaded notes."
        )

        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        prompt = f"""
You are an AI Study Assistant.

Use ONLY the provided context.

Generate 10 flashcards.

Rules:
- Each flashcard should contain:
  - Question
  - Answer
- Keep answers concise and suitable for quick revision.
- Cover different concepts from the notes.
- Do not invent information.

Format exactly like this:

## Flashcard 1

Question:
...

Answer:
...

Repeat for all 10 flashcards.

If the context is insufficient, reply:

"I couldn't generate flashcards from the uploaded notes."

Context:
{context}
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.4
            ),
        )

        return response.text