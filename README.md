# 📚 AI Study Buddy

An intelligent, recruiter-friendly AI study assistant that transforms uploaded educational materials into a personalized learning experience.

Built with Python, Streamlit, LangChain, Google Gemini, FAISS, and sentence-transformers, this project showcases end-to-end AI application development — from document ingestion and embeddings to retrieval-augmented generation (RAG) and interactive study support.

---

## 🚀 Why This Project Stands Out

It is a complete AI-powered learning platform that helps students:

- Ask questions directly from their own notes
- Generate concise summaries
- Create flashcards for revision
- Produce MCQs for self-testing
- Build a personalized study plan based on exam deadlines and available time
- Listen to generated content via text-to-speech


---

## ✨ Key Features

- 📄 Upload study materials in PDF, DOCX, PPTX, and TXT formats
- 🧠 Semantic search over uploaded documents using embeddings + vector search
- 🤖 AI-powered chat with notes using Retrieval-Augmented Generation (RAG)
- 📝 Automatic summarization of long content
- 🧠 Flashcard generation for quick revision
- ✅ MCQ generation for self-assessment
- 📅 Personalized study planner based on exam date, study hours, and skill level
- 🔊 Text-to-speech support for audio-based revision
- ⚡ Cached responses for faster repeated queries

---

## 🛠️ Tech Stack

- Python
- Streamlit for the web UI
- LangChain and LangChain Community
- Google Gemini for LLM generation
- Hugging Face embeddings
- FAISS for vector similarity search
- gTTS for text-to-speech
- Python-dotenv for environment management

---

## 🧩 How It Works

1. Upload notes and study materials
2. Extract and split the content into meaningful chunks
3. Generate embeddings and store them in a FAISS vector database
4. Retrieve the most relevant context using semantic search
5. Use Gemini to generate summaries, explanations, flashcards, MCQs, and study plans

---

## ▶️ Getting Started

### 1. Clone the repository


### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file and add your Google API key:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### 4. Run the app

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```text
AI_Study_Planner/
├── app.py
├── requirements.txt
├── src/
│   ├── cache.py
│   ├── embeddings.py
│   ├── flashcards.py
│   ├── llm.py
│   ├── loader.py
│   ├── mcq_generator.py
│   ├── rag.py
│   ├── splitter.py
│   ├── study_planner.py
│   ├── summarizer.py
│   ├── tts.py
│   └── vectorstore.py
└── vector_store/
```

---
