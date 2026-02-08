import ollama
import re
import chromadb
from chromadb.config import Settings

# def AI_que():
#     print("AI_que called")
#     response = ollama.chat(
#         model="mistral:7b",
#         messages=[
#             {
#                 "role": "system",
#                 "content": (
#                     "You are an aptitude question generator.\n\n"
#                     "Your task is to output EXACTLY ONE aptitude question.\n\n"
#                     "ABSOLUTE RULES (must not be violated):\n"
#                     "- Output ONLY the question text\n"
#                     "- Do NOT include the answer\n"
#                     "- Do NOT include explanations, solutions, or reasoning\n"
#                     "- Do NOT include the words \"answer\", \"solution\", or \"explanation\"\n"
#                     "- Do NOT include prefixes like \"Question:\"\n"
#                     "- ONE sentence only\n"
#                     "- End with a question mark (?)\n\n"
#                     "CONTENT RULES:\n"
#                     "- The question must be an aptitude-style problem\n"
#                     "- It may involve basic algebra, arithmetic, logic, or functions\n"
#                     "- The question must be solvable but NOT trivial\n\n"
#                     "If any rule is violated, the output is invalid."
#                 )
#             }
#         ]
#     )
#     print("AI_que recieved")
#     return response["message"]["content"].strip()

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
    
def clean_text(text):
    pattern = r"Q:(.*?)A:(.*?)--"
    data = re.sub(r"\n" , "" , text)
    data = re.findall(pattern,data,re.S)
    return data

def client_storage():
    client = chromadb.Client(Settings(persist_directory = "chroma_db"))
    storage = client.get_or_create_collection(name = "rag_storage")
    return client , storage