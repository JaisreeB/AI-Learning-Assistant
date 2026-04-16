from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routes import auth, progress

import requests
import os
import json
from dotenv import load_dotenv

# ---------------- ENV ---------------- #

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# ---------------- APP ---------------- #

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- DB INIT ---------------- #

Base.metadata.create_all(bind=engine)

# ---------------- ROUTES ---------------- #

app.include_router(auth.router)
app.include_router(progress.router)

# ---------------- AI QUERY ---------------- #

def query(payload):
    try:
        payload["parameters"] = {
            "temperature": 0.3,
            "max_new_tokens": 500
        }

        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=10
        )

        return response.json()

    except Exception as e:
        print("HF Error:", e)
        return None


# ---------------- FALLBACK QUIZ (ALWAYS 5) ---------------- #

def fallback_quiz(topic):
    return [
        {
            "question": f"What is {topic}?",
            "options": ["Basic concept", "Hardware", "Software", "None"],
            "answer": "Basic concept",
            "level": "beginner",
            "explanation": f"{topic} is a fundamental concept."
        },
        {
            "question": f"Where is {topic} used?",
            "options": ["Real systems", "Art only", "Music", "Sports"],
            "answer": "Real systems",
            "level": "beginner",
            "explanation": f"{topic} is used in real-world applications."
        },
        {
            "question": f"Why is {topic} important?",
            "options": ["Efficiency", "Decoration", "Gaming", "None"],
            "answer": "Efficiency",
            "level": "beginner",
            "explanation": f"{topic} improves efficiency."
        },
        {
            "question": f"What improves {topic} performance?",
            "options": ["Optimization", "Ignoring", "Random", "None"],
            "answer": "Optimization",
            "level": "intermediate",
            "explanation": "Optimization improves performance."
        },
        {
            "question": f"Advanced use of {topic}?",
            "options": ["System design", "Basic usage", "Simple idea", "None"],
            "answer": "System design",
            "level": "advanced",
            "explanation": f"{topic} is used in system design."
        }
    ]


# ---------------- QUIZ (FIXED - ALWAYS 5) ---------------- #

@app.get("/get_quiz")
def get_quiz(topic: str, sector: str):

    prompt = f"""
You are a strict JSON generator.

TOPIC: {topic}
DOMAIN: {sector}

Return ONLY a JSON array of 5 MCQs.

Each item:
{{
  "question": "...",
  "options": ["A","B","C","D"],
  "answer": "A",
  "level": "beginner|intermediate|advanced",
  "explanation": "1-2 lines"
}}

NO TEXT. ONLY JSON.
"""

    try:
        response = query({"inputs": prompt})

        print("HF RAW RESPONSE:", response)  # 🔥 DEBUG

        if not response:
            return fallback_quiz(topic)

        # -----------------------------
        # 🔥 FIX: handle all response types
        # -----------------------------

        if isinstance(response, dict):
            text = response.get("generated_text", "")
        elif isinstance(response, list):
            text = response[0].get("generated_text", "")
        else:
            return fallback_quiz(topic)

        if not text:
            return fallback_quiz(topic)

        print("AI TEXT:", text)

        start = text.find("[")
        end = text.rfind("]")

        if start == -1 or end == -1:
            return fallback_quiz(topic)

        json_str = text[start:end+1]

        quiz = json.loads(json_str)

        if not isinstance(quiz, list):
            return fallback_quiz(topic)

        return quiz[:5]

    except Exception as e:
        print("QUIZ ERROR:", e)
        return fallback_quiz(topic)

# ---------------- EXPLANATION ---------------- #

@app.get("/get_explanation")
def get_explanation(topic: str, level: str):

    prompt = f"""
You are an expert tutor.

Explain the topic: {topic}

Student level: {level}

Rules:
- Write a SINGLE well-structured paragraph
- Must be easy for {level} learner
- Include real-world examples
- Must feel like a human teacher explanation
- No bullet points
"""

    result = query({"inputs": prompt})

    try:
        text = result[0]["generated_text"]
        return {"explanation": text}
    except:
        return {
            "explanation": f"{topic} is an important concept used in real-world applications and becomes more powerful when understood deeply at the {level} level."
        }


# ---------------- VIDEOS ---------------- #

@app.get("/get_videos")
def get_videos(topic: str, level: str):

    if not YOUTUBE_API_KEY:
        return {"videos": [{"title": "No API key", "url": "#"}]}

    try:
        from googleapiclient.discovery import build

        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

        request = youtube.search().list(
            part="snippet",
            q=f"{topic} {level} tutorial",
            maxResults=5,
            type="video"
        )

        response = request.execute()

        videos = []

        for item in response.get("items", []):
            videos.append({
                "title": item["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            })

        return {"videos": videos}

    except Exception as e:
        print("YouTube error:", e)
        return {"videos": [{"title": "Error loading videos", "url": "#"}]}