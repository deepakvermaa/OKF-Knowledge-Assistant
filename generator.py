from config import GEMINI_MODEL


def generate_answer(client, question, knowledge, chat_history):
    prompt = f"""
You are a helpful knowledge assistant.

Answer the user's question using the provided OKF knowledge.

Rules:
1. Use the provided knowledge as the main source.
2. Do not invent facts.
3. You can calculate or derive an answer from the provided facts.
4. When the user asks for monthly working hours and the knowledge gives weekly working hours,
   calculate the average monthly hours using:
   weekly hours × 52 ÷ 12.
5. Clearly say when a value is an average or derived value.
6. If the answer cannot be found or derived from the provided knowledge, say:
   "I couldn't find the answer in the provided knowledge."
7. Keep the answer clear and direct.

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