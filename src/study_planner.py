from google.genai import types


class StudyPlanner:

    @staticmethod
    def generate(
        vector_db,
        client,
        exam_date,
        study_hours,
        difficulty
    ):

        # Create retriever
        retriever = vector_db.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 8,
                "fetch_k": 30
            }
        )

        # Retrieve relevant chunks
        docs = retriever.invoke(
            "Generate a study plan from the uploaded notes."
        )

        # Combine retrieved context
        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        # Prompt
        prompt = f"""
You are an expert AI Study Planner.

Use ONLY the provided context.

The student has provided the following details:

Exam Date:
{exam_date}

Available Study Hours Per Day:
{study_hours}

Current Skill Level:
{difficulty}

Create a personalized study plan.

Your response should include:

# 📚 Personalized Study Plan

## Overview
Briefly explain what the uploaded notes cover.

## Recommended Learning Order
List the topics in the best sequence.

## Day-wise Study Plan
Distribute the workload according to the available study hours.

## Revision Strategy
Suggest how and when to revise.

## Final Revision
Explain what to do before the exam.

Important Rules:
- Use ONLY the uploaded notes.
- Do not invent topics.
- Make the schedule realistic.
- Adjust the workload based on the available study hours.
- Assume the student is preparing specifically for the uploaded material.

If the context is insufficient, reply:

"I couldn't generate a study plan from the uploaded notes."

Context:
{context}
"""

        # Generate response
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.4
            ),
        )

        return response.text