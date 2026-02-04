from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,JSONResponse
import pandas as pd
from app import AI_que ,AI_res

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# @app.get("/", response_class=HTMLResponse)
# def home(request: Request):
#     return templates.TemplateResponse(
#         "index.html",
#         {"request": request}
#     )
@app.get("/question")
def get_que():
    question = AI_que()
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

    ai_result = AI_res(question, answer)

    return {"evaluation": ai_result}


CSV_PATH = "data.csv"
df = pd.read_csv(CSV_PATH , delimiter= ';')
df.columns = df.columns.str.strip()

@app.get("/")
def home(request: Request):
    types = sorted(df["Type"].dropna().unique().tolist())
    return templates.TemplateResponse(
        "appti.html",
        {"request": request, "types": types}
    )

@app.get("/questions/{qtype}")
def get_questions(qtype: str):
    filtered_df = df[df["Type"] == qtype]

    questions = filtered_df.to_dict(orient="records")
    return JSONResponse(questions)

@app.post("/check-answer")
async def check_answer(payload: dict):
    user_ans = payload["user_answer"]
    correct_ans = payload["correct_answer"]
    approach = payload["approach"]

    is_correct = user_ans == correct_ans

    return {
        "correct": is_correct,
        "approach": approach if not is_correct else None
    }
