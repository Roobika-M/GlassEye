from transformers import pipeline

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
qa_pipeline = pipeline("question-answering")

def summarize_text(text):
    summary = summarizer(text, max_length=100, min_length=25, do_sample=False)
    return summary[0]['summary_text']

def answer_question(context, question):
    result = qa_pipeline(question=question, context=context)
    return result['answer']
