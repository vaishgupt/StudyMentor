from google.genai import types


class Summarizer:

    @staticmethod
    def summarize(vector_db, client):

        # Retrieve representative chunks from the vector database
        retriever = vector_db.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 8,
                "fetch_k": 30
            }
        )

        docs = retriever.invoke("Summarize the uploaded notes.")

        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        prompt = f"""
You are an AI Study Assistant.

Using ONLY the provided context, generate a well-structured summary.

Format your response exactly like this:

# 📄 Summary

## Overview
A short paragraph describing the notes.

## Key Concepts
- Point 1
- Point 2
- Point 3

## Important Points
- Point 1
- Point 2
- Point 3

## Quick Revision
Write 4–6 concise revision bullets.

If the context is insufficient, say:
"I couldn't generate a summary from the uploaded notes."

Context:
{context}
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3
            ),
        )

        return response.text