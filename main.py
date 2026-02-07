from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import pandas as pd
from app import AI_que ,AI_res
from questions import que
import random
import time
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class user(BaseModel):
    name : str 
    profession : str 

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "intro.html",
        {"request": request}
    )
@app.get("/question")
def get_que():
    question = random.choice(list(que.keys()))
    return {"question": question}

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
    
current_user = {}
@app.post("/user_data")
def user_data(request : user):
    current_user["name"] = request.name
    current_user["profession"] = request.profession
    return{
        "status" : "ok" ,
        "name"  : request.name ,
        "profession" : request.profession
    }
    
@app.get("/interview")
def interview(request: Request):
    return templates.TemplateResponse(
        "interview.html",
        {
            "request": request,
            "name": current_user["name"],
            "profession": current_user["profession"]
        }
    )

# CSV_PATH = "data.csv"
# df = pd.read_csv(CSV_PATH , delimiter= ';')
# df.columns = df.columns.str.strip()

# @app.get("/")
# def home(request: Request):
#     types = sorted(df["Type"].dropna().unique().tolist())
#     return templates.TemplateResponse(
#         "appti.html",
#         {"request": request, "types": types}
#     )

# @app.get("/questions/{qtype}")
# def get_questions(qtype: str):
#     filtered_df = df[df["Type"] == qtype]

#     questions = filtered_df.to_dict(orient="records")
#     return JSONResponse(questions)

# @app.post("/check-answer")
# async def check_answer(payload: dict):
#     user_ans = payload["user_answer"]
#     correct_ans = payload["correct_answer"]
#     approach = payload["approach"]

#     is_correct = user_ans == correct_ans

#     return {
#         "correct": is_correct,
#         "approach": approach if not is_correct else None
#     }
