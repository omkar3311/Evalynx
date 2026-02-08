from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import pandas as pd
from app import AI_res , questions
from questions import que
import random
import time
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class user(BaseModel):
    name : str 

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "intro.html",
        {"request": request}
    )
@app.get("/question")
def get_que():
    question = questions()
    return {"question": question[0]}

@app.post("/evaluate")
async def evaluate_answer(request: Request):
    body = await request.json()

    question = body.get("question", "")
    answer = body.get("answer", "").strip().lower()

    if not question or not answer:
        return {
            "correct": False,
            "score": 0,
            "feedback": "Missing question or answer"
        }
    start_time = time.perf_counter()
    ai_result = AI_res(question, answer)
    end_time = time.perf_counter()

    total_time = round(end_time - start_time, 2)

    return {
        "evaluation": ai_result,
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

