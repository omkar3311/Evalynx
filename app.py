import ollama
import re
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np

def AI_res(ai_data: dict):
    print("AI_res called")
    SYSTEM_PROMPT = (
        "You are a senior Machine Learning Engineer conducting a technical interview.\n"
        "You will be given exactly 5 questions.\n"
        "Each question has:\n"
        "- a reference answer (correct answer)\n"
        "- a user answer\n\n"
        "Rules:\n"
        "- Each question is worth exactly 2 marks\n"
        "- Total score is out of 10\n"
        "- Give partial marks (0, 1, or 2) per question\n"
        "- Judge correctness based ONLY on the reference answer\n"
        "- Be strict but fair\n"
        "- If the User Answer is an empty string (\"\"), it means the user did not answer the question;\n"
        "  in that case, give a score of 0 and provide a one-line feedback briefly explaining the expected concept\n"
        "- No extra explanations\n\n"
        "- No extra explanations\n\n"
        "Return output in EXACTLY this format:\n\n"
        "Total Score: <number out of 10>\n\n"
        "Per Question Evaluation:\n"
        "1. Score: <0-2> | Feedback: <one short sentence>\n"
        "2. Score: <0-2> | Feedback: <one short sentence>\n"
        "3. Score: <0-2> | Feedback: <one short sentence>\n"
        "4. Score: <0-2> | Feedback: <one short sentence>\n"
        "5. Score: <0-2> | Feedback: <one short sentence>\n\n"
        "Overall Feedback:\n"
        "<2–3 sentences summarizing ML strengths and weaknesses>\n"
        "Do NOT add anything else."
    )

    user_prompt = "Evaluate the following answers:\n\n"

    for idx, (question, data) in enumerate(ai_data.items(), start=1):
        user_prompt += (
            f"Question {idx}: {question}\n"
            f"Reference Answer: {data['reference_answer']}\n"
            f"User Answer: {data['user_answer']}\n\n"
        )

    response = ollama.chat(
        model="mistral:7b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )
    print(response["message"]["content"].strip())
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


client = chromadb.Client(Settings(persist_directory = "chroma_db"))
storage = client.get_or_create_collection(name = "rag_storage")
model = SentenceTransformer("all-MiniLM-L6-v2")

def encode_data():
    data = clean_text()
    for i ,(q,a) in enumerate(data):
        emd = model.encode(q).tolist()
        storage.add(
            ids = [f"q{i}"],
            documents = [q],
            embeddings = [emd],
            metadatas=[{"answer": a}]
        )

def retrieve(user_que , k =3):
    que = model.encode(user_que).tolist()
    results = storage.query(
        query_embeddings = [que],
        n_results = k
        )
    return results["metadatas"][0][0]["answer"]

def questions():
    data = clean_text()
    que = []
    for i ,(q ,a) in enumerate(data):
        que.append(q)
    ques = np.random.choice(que , size = 5 , replace =False)
    return ques