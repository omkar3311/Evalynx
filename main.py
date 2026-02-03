from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

QUESTION = "What is the capital of France?"
CORRECT_ANSWER = "paris"

@app.get("/question")
def get_que():
    return {"question": QUESTION}

@app.post("/evaluate")
async def evaluate_answer(request: Request):
    body = await request.json()
    answer = body.get("answer", "").strip().lower()

    if not answer:
        return {
            "correct": False,
            "score": 0,
            "feedback": "No answer provided"
        }

    if answer == CORRECT_ANSWER:
        return {
            "correct": True,
            "score": 1,
            "feedback": "Correct answer. Well done."
        }

    return {
        "correct": False,
        "score": 0,
        "feedback": "Incorrect. The correct answer is Paris."
    }
