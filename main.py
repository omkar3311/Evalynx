from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import pandas as pd
from app import AI_res , questions ,encode_data ,retrieve
import random
import time
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
encode_data()

class user(BaseModel):
    name : str 

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {"request": request}
    )
    
interview_sessions = {}

@app.get("/question")
def get_que():
    # q_list = ["What is Machine Learning?" , "What are the main types of Machine Learning?" , 
    #           "What is the difference between classification and regression?", "What is overfitting in Machine Learning?",
    #           "What is underfitting? "]
    q_list = questions() 
    session_id = str(time.time())

    interview_sessions[session_id] = {
        "questions": q_list,
        "answers": [],
        "index": 0
    }

    return {
        "session_id": session_id,
        "question": q_list[0]
    }

class AnswerPayload(BaseModel):
    session_id: str
    answer: str

ai_data = {}
@app.post("/next-question")
def next_question(payload: AnswerPayload):
    session = interview_sessions.get(payload.session_id)

    if not session:
        return {"error": "Invalid session"}

    idx = session["index"]
    question = session["questions"][idx]

    session["answers"].append({
        "question": question,
        "answer": payload.answer
    })
    retrieved_ans = retrieve(question)
    ai_data[question] = {
        "reference_answer": retrieved_ans,
        "user_answer": payload.answer
    }
    session["index"] += 1
    
    if session["index"] < len(session["questions"]):
        return {
            "question": session["questions"][session["index"]],
            "done": False
        }

    start_time = time.perf_counter()
    ai_result = AI_res(ai_data)
    end_time = time.perf_counter()

    total_time = round(end_time - start_time, 2)
    return {
        "done": True,
        "evaluation":ai_result,
#         "evaluation": """
#         Total Score: 9

# Per Question Evaluation:
# 1. Score: 2 | Feedback: Correct, but more specific information about machine learning would have been beneficial.
# 2. Score: 2 | Feedback: Correct, but providing examples for each type of machine learning could have improved the answer.
# 3. Score: 2 | Feedback: Correct, but a clearer distinction between the two would have made the answer more informative.
# 4. Score: 2 | Feedback: Correct, but specifying overfitting as learning irrelevant patterns and suggesting ways to address it would have been useful.
# 5. Score: 2 | Feedback: Correct, but mentioning underfitting as a model being too simple and providing suggestions for improvement would have been beneficial.

# Overall Feedback:
# The candidate demonstrated a good understanding of the basics of machine learning, including its definition, types, and common issues like overfitting and underfitting. However, the answers could have been more detailed and informative to show a stronger grasp of these concepts. The candidate may benefit from focusing on providing more specific and well-structured responses during technical interviews.""",
        "time_taken": total_time
    }
    
current_user = None
@app.post("/user_data")
def user_data(request : user):
    global current_user
    current_user = request.name
    return{
        "status" : "ok" ,
        "name"  : request.name 
    }
    
@app.get("/interview")
def interview(request: Request):
    return templates.TemplateResponse(
        "interview.html",
        {
            "request": request,
            "name": current_user
        }
    )

