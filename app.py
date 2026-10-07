import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

from embedder import load_model
from retrieve import retrieve_knowledge
from generator import generate_answer


st.set_page_config(
    page_title="OKF Knowledge Assistant",
    page_icon="📚"
)


def load_gemini_client():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            raise ValueError("GEMINI_API_KEY not found.")

    return genai.Client(api_key=api_key)


client = load_gemini_client()

if "embedding_model" not in st.session_state:
    st.session_state.embedding_model = load_model()

embedding_model = st.session_state.embedding_model


if "messages" not in st.session_state:
    st.session_state.messages = []


st.title("📚 OKF Knowledge Assistant")

st.write(
    "Ask questions about the company policies in the knowledge base."
)


with st.sidebar:
    st.header("Knowledge Base")

    st.write("12 policy documents")
    st.write("Embeddings: Sentence Transformers")
    st.write("Search: FAISS")
    st.write("Answer generation: Gemini")

    st.subheader("Example questions")

    st.write("• How many days of annual leave do employees get?")
    st.write("• Can I work from home?")
    st.write("• Can I claim hotel expenses?")
    st.write("• What are the normal working hours?")
    st.write("• How do I claim a certification expense?")


for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


question = st.chat_input("Ask a question about the policies...")


if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.write(question)

    result = retrieve_knowledge(
        question,
        embedding_model
    )

    if result is None:

        answer = "I couldn't find relevant knowledge for this question."

    else:

        knowledge = result["knowledge"]

        chat_history = ""

        for message in st.session_state.messages:
            chat_history += (
                message["role"]
                + ": "
                + message["content"]
                + "\n"
            )

        try:
            answer = generate_answer(
                client,
                question,
                knowledge,
                chat_history
            )

        except Exception:
            answer = (
                "I found the relevant knowledge, "
                "but the AI service is temporarily unavailable."
            )

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    if result is not None:

        with st.expander("Knowledge used"):

            concept = result["concept"]

            st.write("Title:", concept["title"])
            st.write("Department:", concept["department"])
            st.write("Version:", concept["version"])
            st.write("Status:", concept["status"])
            st.write("Tags:", ", ".join(concept["tags"]))
            st.write("Source:", concept["source"])