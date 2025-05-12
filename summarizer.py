from transformers import pipeline

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
chatbot_pipeline = pipeline("text-generation", model="microsoft/DialoGPT-small", max_length=100)

def summarize_text(text):
    summary = summarizer(text, max_length=100, min_length=25, do_sample=False)
    return summary[0]['summary_text']

def answer_question(context, question):
    # Try QA pipeline first
    result = qa_pipeline(question=question, context=context)
    answer = result.get('answer', '').strip()
    score = result.get('score', 0)
    print(f"DEBUG: QA pipeline score: {score}, answer: {answer}")
    if answer and score > 0.4:
        return answer
    else:
        # Improved fallback to chatbot pipeline with more context and instructions
        prompt = (
            f"Context: {context}\n"
            f"Question: {question}\n"
            "Answer the question based on the context above. If the answer is not contained in the context, say 'I don't know.'"
        )
        responses = chatbot_pipeline(prompt, max_length=150, num_return_sequences=1)
        generated_text = responses[0]['generated_text']
        answer = generated_text.replace(prompt, "").strip()
        if not answer or answer.lower() in ["i don't know.", "i do not know.", "unknown"]:
            return "Sorry, I could not generate an answer."
        return answer
