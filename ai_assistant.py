import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_openai(question, context=None):
    prompt = question
    if context:
        prompt = f"Context: {context}\\nQuestion: {question}"

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
            n=1,
            stop=None,
        )
        answer = response.choices[0].text.strip()
        return answer
    except Exception as e:
        return f"Error communicating with AI assistant: {str(e)}"
