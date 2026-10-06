from config import GEMINI_MODEL


def generate_answer(client, question, knowledge, chat_history):

    prompt = f"""
You are a helpful knowledge assistant.

Answer the user's question using the provided OKF knowledge.

Rules:
1. Use the provided knowledge as the main source.
2. Do not make up information that is not present in the knowledge.
3. If the answer is not present, say:
   "I couldn't find the answer in the provided knowledge."
4. Keep the answer clear and direct.
5. Use previous conversation only when the user asks a follow-up question.

Previous Conversation:
{chat_history}

OKF Knowledge:
{knowledge}

User Question:
{question}
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text