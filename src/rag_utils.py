import os
from dotenv import load_dotenv
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import tiktoken

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
tokenizer = tiktoken.encoding_for_model("gpt-4")

def chunk_text(text, max_tokens=200):
    words = text.split()
    chunks = []
    current_chunk = []
    tokens = 0
    for word in words:
        word_tokens = len(tokenizer.encode(word))
        if tokens + word_tokens > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            tokens = word_tokens
        else:
            current_chunk.append(word)
            tokens += word_tokens
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def get_embeddings(texts):
    return [client.embeddings.create(model="text-embedding-3-small", input=txt).data[0].embedding for txt in texts]

def retrieve_top_chunks(query, chunks, embeddings, top_k=3):
    query_embedding = get_embeddings([query])[0]
    scores = cosine_similarity([query_embedding], embeddings)[0]
    ranked = sorted(zip(scores, chunks), key=lambda x: x[0], reverse=True)
    return [chunk for _, chunk in ranked[:top_k]]

def get_context(question, key_elements, rubric):
    base_text = f"Question: {question}\nKey Elements: {key_elements}\nRubric: {rubric}"
    chunks = chunk_text(base_text)
    embeddings = get_embeddings(chunks)
    top_chunks = retrieve_top_chunks(question, chunks, embeddings)
    return top_chunks