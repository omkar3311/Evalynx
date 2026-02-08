import ollama
import re
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

def AI_res(question, user_answer):
    print("AI_res called")
    response = ollama.chat(
        model="mistral:7b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict computer science evaluator.\n"
                    "Evaluate the user's answer to the given question.\n"
                    "Return output in EXACTLY this format:\n\n"
                    "Correct: yes or no\n"
                    "Score: <number from 0 to 10>\n"
                    "Feedback: <one or two sentences on how to improve>\n\n"
                    "Do not add anything else."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Question: {question}\n"
                    f"User Answer: {user_answer}"
                )
            }
        ]
    )
    print("AI_res recieved")

    return response["message"]["content"].strip()

def import_data():
    text = ""
    with open("data2.txt" , "r") as f:
        text += f.read()
    return text
    
def clean_text():
    text = import_data()
    pattern = r"Q:(.*?)A:(.*?)--"
    data = re.sub(r"\n" , "" , text)
    data = re.findall(pattern,data,re.S)
    return data

def client_storage_model():
    client = chromadb.Client(Settings(persist_directory = "chroma_db"))
    storage = client.get_or_create_collection(name = "rag_storage")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return client , storage , model

def encode_data(data , model ,storage):
    for i ,(q,a) in enumerate(data):
        emd = model.encode(q).tolist()
        storage.add(
            ids = f"q{i}",
            documents = [q],
            embeddings = [emd],
            metadatas=[{"answer": a}]
        )
        
def retrive(model,user_que ,storage , k =3):
    que = model.encode(user_que).tolist()
    results = storage.query(
        query_embeddings = [que],
        n_results = k
        )
    if not results["distances"][0]:
        return "No answer found."
    return results

def questions():
    data = clean_text()
    que = []
    for q ,a in enumerate(data):
        que.append(q)