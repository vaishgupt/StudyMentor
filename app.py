import streamlit as st

from src.loader import DocumentLoader
from src.splitter import TextSplitter
from src.embeddings import EmbeddingModel
from src.vectorstore import VectorStore

from src.llm import GeminiLLM
from src.rag import RAG

from src.summarizer import Summarizer
from src.mcq_generator import MCQGenerator
from src.flashcards import FlashcardGenerator
from src.study_planner import StudyPlanner

from src.tts import TextToSpeech

from src.cache import Cache


# ----------------------------------
# Page Configuration
# ----------------------------------
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="wide"
)


Cache.initialize()

# ----------------------------------
# Session State
# ----------------------------------

if "vector_db" not in st.session_state:
     st.session_state["vector_db"] = None

if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""

if "generated_docs" not in st.session_state:
    st.session_state.generated_docs = []

if "generated_feature" not in st.session_state:
    st.session_state.generated_feature = ""

# ----------------------------------
# Cache Embedding Model
# ----------------------------------
@st.cache_resource
def load_embedding_model():
    return EmbeddingModel.load_embeddings()

# ----------------------------------
# Text To Speech
# ----------------------------------

def play_audio(key):

    if st.button("🔊 Listen", key=key):

        if st.session_state.generated_text.strip() == "":
            st.warning("Nothing to read.")
            return

        with st.spinner("Generating audio..."):

            audio_path = TextToSpeech.generate_audio(
                st.session_state.generated_text
            )

        with open(audio_path, "rb") as audio_file:
            st.audio(audio_file.read())


# ----------------------------------
# Title
# ----------------------------------
st.title("📚 AI Study Buddy")
st.markdown("### Your Personal AI Study Assistant")


# ----------------------------------
# Sidebar
# ----------------------------------
with st.sidebar:

    st.header("📂 Upload Study Material")

    uploaded_files = st.file_uploader(
        "Upload your notes",
        type=["pdf", "docx", "pptx", "txt"],
        accept_multiple_files=True,
    )

    process = st.button(
        "⚙️ Process Documents",
        use_container_width=True
    )

    st.divider()

    st.header("🎯 Features")

    feature = st.selectbox(
        "Choose Feature",
        [
            "Chat with Notes",
            "Summarize",
            "Explain Topic",
            "Flashcards",
            "MCQs",
            "Short Questions",
            "Long Questions",
            "Revision Mode",
            "Study Planner",
            "Smart Search",
        ],
    )


# ----------------------------------
# Main Workspace
# ----------------------------------
st.subheader("💬 AI Workspace")


if uploaded_files:

    st.success(f"✅ {len(uploaded_files)} file(s) selected.")

    st.write("### Uploaded Files")

    for file in uploaded_files:
        st.write(f"📄 {file.name}")

    if process:

        with st.spinner("📚 Processing documents..."):

            # -------------------------
            # Load Documents
            # -------------------------
            documents = DocumentLoader.load_documents(uploaded_files)

            # -------------------------
            # Split into Chunks
            # -------------------------
            chunks = TextSplitter.split_documents(documents)

            # -------------------------
            # Load Embedding Model
            # -------------------------
            embeddings = load_embedding_model()

            # -------------------------
            # Create FAISS Vector Store
            # -------------------------
            vector_db = VectorStore.create(
                chunks,
                embeddings
            )

            # Save in session
            st.session_state["vector_db"] = vector_db
            st.session_state["embeddings"] = embeddings
            st.session_state["chunks"] = chunks

        st.success("✅ Documents Processed Successfully!")

        # -------------------------
        # Metrics
        # -------------------------
        col1, col2, col3 = st.columns(3)

        col1.metric("Documents", len(documents))
        col2.metric("Chunks", len(chunks))
        col3.metric("Vectors", vector_db.index.ntotal)

        st.divider()

        # -------------------------
        # Chunk Preview
        # -------------------------
        st.subheader("📖 Chunk Preview")

        for i, chunk in enumerate(chunks[:5], start=1):

            with st.expander(f"Chunk {i}"):

                st.write("### Metadata")

                st.json(chunk.metadata)

                st.write("### Content")

                st.write(chunk.page_content)

else:

    st.info("👈 Upload one or more study files from the sidebar.")


st.divider()

# ----------------------------------
# Chat Section
# ----------------------------------


# ----------------------------------
# AI Workspace
# ----------------------------------

st.subheader(f"🤖 {feature}")

query = ""

if feature == "Chat with Notes":

    query = st.text_area(
        "Ask anything about your uploaded notes",
        placeholder="Example: Explain Neural Networks.",
        height=120,
    )

# ----------------------------------
# Study Planner Inputs
# ----------------------------------

exam_date = None
study_hours = None
difficulty = None

if feature == "Study Planner":

    st.subheader("📅 Study Preferences")

    exam_date = st.date_input(
        "Exam Date"
    )

    study_hours = st.slider(
        "Study Hours Per Day",
        min_value=1,
        max_value=12,
        value=3
    )

    difficulty = st.selectbox(
        "Current Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

button = st.button(
    "🚀 Generate",
    use_container_width=True
)

if button:

    if "vector_db" not in st.session_state:

        st.warning("⚠️ Please upload and process documents first.")

    else:

        llm = GeminiLLM.load()

        with st.spinner("🤖 Working..."):

            # -------------------------
            # Chat
            # -------------------------
            if feature == "Chat with Notes":

                if query.strip() == "":
                    st.warning("⚠️ Enter a question.")

                else:

                    # Check cache first
                    cached_answer = Cache.get(query)

                    if cached_answer:

                        answer = cached_answer
                        docs = []

                        st.success("⚡ Answer loaded from cache.")

                    else:

                        answer, docs = RAG.ask(
                            query,
                            st.session_state["vector_db"],
                            llm
                        )

                        Cache.save(query, answer)

                    st.session_state.generated_text = answer
                    st.session_state.generated_docs = docs
                    st.session_state.generated_feature = "Chat"

                    # st.divider()

                    # st.subheader("📚 Sources")

                    # for doc in docs:

                    #     st.write(
                    #         f"**{doc.metadata['source']}** | Page {doc.metadata['page']}"
                    #     )

            # -------------------------
            # Summarizer
            # -------------------------
            elif feature == "Summarize":

                summary = Summarizer.summarize(
                    st.session_state["vector_db"],
                    llm
                )

                st.session_state.generated_text = summary
                st.session_state.generated_docs = []
                st.session_state.generated_feature = "Summary"

            
            # -------------------------
            # MCQ Generator
            # -------------------------
            elif feature == "MCQs":

                mcqs = MCQGenerator.generate(
                    st.session_state["vector_db"],
                    llm
                )

                st.session_state.generated_text = mcqs
                st.session_state.generated_docs = []
                st.session_state.generated_feature = "MCQs"

                        # -------------------------
            # Flashcards
            # -------------------------
            elif feature == "Flashcards":

                flashcards = FlashcardGenerator.generate(
                    st.session_state["vector_db"],
                    llm
                )

                st.session_state.generated_text = flashcards
                st.session_state.generated_docs = []
                st.session_state.generated_feature = "Flashcards"



                        # -------------------------
            # Study Planner
            # -------------------------
            elif feature == "Study Planner":

                plan = StudyPlanner.generate(
                        st.session_state["vector_db"],
                        llm,
                        exam_date,
                        study_hours,
                        difficulty
                    )

                st.session_state.generated_text = plan
                st.session_state.generated_docs = []
                st.session_state.generated_feature = "Study Planner"

# ----------------------------------
# Display Generated Result
# ----------------------------------

if st.session_state.generated_text:

    st.divider()

    if st.session_state.generated_feature == "Chat":
        st.subheader("📖 Answer")

    elif st.session_state.generated_feature == "Summary":
        st.subheader("📄 Summary")

    elif st.session_state.generated_feature == "MCQs":
        st.subheader("📝 Generated MCQs")

    elif st.session_state.generated_feature == "Flashcards":
        st.subheader("🧠 Flashcards")

    elif st.session_state.generated_feature == "Study Planner":
        st.subheader("📚 Personalized Study Plan")

    st.markdown(st.session_state.generated_text)

    play_audio("listen_audio")

    if st.session_state.generated_docs:

        st.divider()

        st.subheader("📚 Sources")

        for doc in st.session_state.generated_docs:

            st.write(
                f"**{doc.metadata['source']}** | Page {doc.metadata['page']}"
            )