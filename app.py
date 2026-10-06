import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

from retrieve import retrieve_knowledge
from generator import generate_answer


st.set_page_config(
    page_title="OKF Knowledge Assistant",
    page_icon="📚",
    layout="centered"
)


def load_gemini_client():

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            raise ValueError("GEMINI_API_KEY not found.")
        raise ValueError("GEMINI_API_KEY not found.")

    client = genai.Client(
        api_key=api_key
    )

    return client


client = load_gemini_client()


# Store conversation
if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📚 OKF Knowledge Assistant")

st.write(
    "Ask questions about the structured company knowledge base."
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("Knowledge Base")

    st.write("5 active concepts")
    st.write("• HR Policies")
    st.write("• Finance Policies")
    st.write("• Learning & Development")

    st.divider()

    st.write("This assistant uses structured OKF knowledge.")
    st.write("PDFs are converted into Markdown knowledge files.")


# --------------------------------------------------
# Example questions
# --------------------------------------------------

st.subheader("Try an example")

col1, col2 = st.columns(2)

with col1:

    if st.button("Annual leave"):

        st.session_state.example_question = (
            "How many annual leave days are available?"
        )


with col2:

    if st.button("Work from home"):

        st.session_state.example_question = (
            "How many days can I work from home?"
        )


col3, col4 = st.columns(2)

with col3:

    if st.button("Travel reimbursement"):

        st.session_state.example_question = (
            "What is the hotel reimbursement limit?"
        )


with col4:

    if st.button("Attendance"):

        st.session_state.example_question = (
            "What should an employee do if they cannot attend work?"
        )


# Get example question if a button was clicked
example_question = st.session_state.get(
    "example_question",
    ""
)


# --------------------------------------------------
# Display previous messages
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# --------------------------------------------------
# User input
# --------------------------------------------------

question = st.chat_input(
    "Ask a question..."
)


if not question and example_question:

    question = example_question

    st.session_state.example_question = ""


# --------------------------------------------------
# Process question
# --------------------------------------------------

if question:

    with st.chat_message("user"):
        st.write(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # Find relevant OKF knowledge
    result = retrieve_knowledge(question)


    if result is None:

        answer = (
            "I couldn't find relevant knowledge "
            "in the knowledge base."
        )

        concept = None

    else:

        concept = result["concept"]
        knowledge = result["knowledge"]


        # Build conversation history
        chat_history = ""

        for message in st.session_state.messages[:-1]:

            chat_history += (
                message["role"]
                + ": "
                + message["content"]
                + "\n"
            )


        # Generate answer
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
                "but the AI service is temporarily unavailable. "
                "Please try again."
            )


    # --------------------------------------------------
    # Display answer
    # --------------------------------------------------

    with st.chat_message("assistant"):

        st.write(answer)


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    # --------------------------------------------------
    # Show selected knowledge
    # --------------------------------------------------

    if concept is not None:

        with st.expander("Knowledge used"):

            st.write(
                "**Title:** "
                + concept["title"]
            )

            st.write(
                "**Type:** "
                + concept["type"]
            )

            st.write(
                "**Status:** "
                + concept["status"]
            )

            st.write(
                "**Tags:** "
                + ", ".join(concept["tags"])
            )

            st.write(
                "**Source:** "
                + os.path.basename(
                    concept["resource"]
                )
            )