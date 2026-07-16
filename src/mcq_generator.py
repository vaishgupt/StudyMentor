from google.genai import types


class MCQGenerator:

    @staticmethod
    def generate(vector_db, client):

        retriever = vector_db.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 8,
                "fetch_k": 30
            }
        )

        docs = retriever.invoke("Generate multiple choice questions from the uploaded notes.")

        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        prompt = f"""
You are an AI Study Assistant.

Use ONLY the provided context.

Generate 10 multiple-choice questions.

Rules:
- Each question should have exactly 4 options (A, B, C, D).
- Clearly indicate the correct answer after each question.
- Questions should cover different topics from the notes.
- Do not invent information outside the context.

Format exactly like this:

## Question 1

Question text

A.
B.
C.
D.

✅ Correct Answer: B

Repeat for all 10 questions.

If the context is insufficient, reply:

"I couldn't generate MCQs from the uploaded notes."

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