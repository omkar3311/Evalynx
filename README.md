# Evalynx – AI-Powered Mock Interview Platform

Evalynx is an AI-powered mock interview platform designed to simulate real technical interviews for Machine Learning and Data Science roles.  
It uses **FastAPI**, **Retrieval-Augmented Generation (RAG)**, and **Ollama (Mistral 7B)** to conduct interviews, evaluate answers, and generate structured feedback.

The system dynamically selects questions, retrieves authoritative reference answers, and evaluates candidate responses using a large language model under strict scoring rules.

---

## 🚀 Features

- AI-driven technical interviews
- Dynamic question selection
- Retrieval-Augmented Generation (RAG) for factual grounding
- Strict per-question scoring
- Structured feedback generation
- Timed interview questions
- Voice-based AI interviewer
- Speech-to-text answer input
- Webcam support
- Interview progress tracking
- Automated final evaluation and scoring

---

## 🧩 Build Interviews for Any Domain

Evalynx is **domain-independent**.

You can create interviews for **any field** (Data Science, Backend, DevOps, Cybersecurity, Finance, Medicine, etc.) by simply providing a new knowledge file.

### How It Works
- Create a new text file (e.g., `data.txt`)
- Add question–answer pairs in the format:
Q: <your question>
A: <reference answer>
- Replace the existing data file
- Restart the application

The system automatically:
- Encodes the new data
- Builds vector embeddings
- Selects relevant questions
- Evaluates answers using the same scoring logic

No code changes are required.

---

## 🧠 Tech Stack

### Backend
- **FastAPI**
- **Pydantic**
- **Ollama (Mistral 7B)**
- **ChromaDB**
- **SentenceTransformers**
- **NumPy**
- **Python**

### Frontend
- HTML5
- CSS (custom)
- Vanilla JavaScript
- Web Speech API (Text-to-Speech & Speech Recognition)
- MediaDevices API (Camera)

---


## 📂 Project Structure

.
├── app.py
├── data2.txt
├── main.py
├── README.md
├── requirements.txt
├── static
│   ├── css
│   │   └── style.css
│   ├── images
│   │   └── evalynx.png
│   └── js
│       └── interview.js
└── templates
    ├── home.html
    └── interview.html

## 🎯 Purpose

Evalynx is designed to provide a realistic, AI-driven interview environment that closely mirrors real technical interviews.

The platform helps candidates:
- Practice structured technical explanations
- Improve clarity and depth of answers
- Manage time pressure during interviews
- Receive objective, reference-grounded feedback
- Prepare for interviews across different technical domains

By combining Retrieval-Augmented Generation (RAG) with strict evaluation rules, Evalynx focuses on **correctness, reasoning, and communication**, not memorization.


## 🔄 Interview Workflow

1. User enters their name and starts the interview
2. A new interview session is created
3. Five questions are selected dynamically from the knowledge base
4. For each question:
   - The AI interviewer reads the question aloud
   - A 60-second timer is started
   - The candidate responds via voice or text
   - Answers are recorded and stored
5. Reference answers are retrieved using vector similarity search
6. After the final question:
   - All responses are evaluated by the LLM
   - Each question is scored out of 2
   - A total score out of 10 is computed
   - Detailed per-question feedback is generated
7. Final evaluation is presented to the candidate

---

## 🧪 Evaluation Methodology

- Each question carries exactly **2 marks**
- Total score is calculated out of **10**
- Partial scoring is allowed (0, 1, or 2)
- Evaluation is based strictly on retrieved reference answers
- Unanswered questions automatically receive a score of 0
- Feedback is concise, technical, and interview-oriented

---
