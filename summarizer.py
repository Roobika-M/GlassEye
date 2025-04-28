from transformers import pipeline

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
chatbot_pipeline = pipeline("text-generation", model="microsoft/DialoGPT-small", max_length=100)

def summarize_text(text):
    summary = summarizer(text, max_length=100, min_length=25, do_sample=False)
    return summary[0]['summary_text']

def is_general_question(question):
    general_keywords = ["how to", "why", "what is", "error", "fix", "help", "close", "open", "install", "run"]
    question_lower = question.lower()
    return any(keyword in question_lower for keyword in general_keywords)

def answer_question(context, question):
    if is_general_question(question):
        prompt = f"Q: {question}\nA:"
        responses = chatbot_pipeline(prompt, max_length=100, num_return_sequences=1)
        generated_text = responses[0]['generated_text']
        # Remove the question part from the generated text if repeated
        answer = generated_text.replace(prompt, "").strip()
        return answer if answer else "Sorry, I could not generate an answer."
    else:
        result = qa_pipeline(question=question, context=context)
        return result['answer']
