# AI-Learning-Assistant
AI Learning Assistant is a full-stack web app that provides personalized, topic-based quizzes with real-time evaluation and AI-generated explanations. It includes user login, progress tracking, and dynamic quiz generation. Built using FastAPI, HTML, CSS, JavaScript, and SQLite, it helps students learn interactively with instant feedback.

# Features  
AI-generated MCQ quizzes based on topic  
Difficulty levels: Beginner, Intermediate, Advanced  
Automatic explanations for answers  
YouTube video recommendations  
User login & signup system  
Progress tracking dashboard  

# Tech Stack  
Frontend: HTML, CSS, JavaScript  
Backend: FastAPI (Python)  
Database: SQLite  
AI: HuggingFace API  
Videos: YouTube Data API  

# How to Run
Start backend server:  
uvicorn main:app --reload  

Open index.html in browser  

Ensure backend runs at:
http://127.0.0.1:8000  

# API Endpoints
/signup – Create user  
/login – User login  
/get_quiz – Generate AI quiz  
/get_explanation – Get explanation  
/get_videos – Get videos
/dashboard/{user_id} – User progress  

# Author  
Jaisree B
