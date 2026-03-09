from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_quiz")
def get_quiz(topic: str, sector: str):

    if sector == "technology":

        quiz = [
            {
                "question": f"What is the primary role of {topic} in modern IT systems?",
                "options": [
                    "Improving system performance",
                    "Managing network infrastructure",
                    "Enhancing data processing capabilities",
                    "Supporting scalable software solutions"
                ],
                "answer": "Supporting scalable software solutions"
            },
            {
                "question": f"{topic} is most closely associated with which discipline?",
                "options": [
                    "Computer Science",
                    "Information Technology",
                    "Software Engineering",
                    "Data Engineering"
                ],
                "answer": "Computer Science"
            },
            {
                "question": f"Which benefit does {topic} commonly provide in technology environments?",
                "options": [
                    "Operational efficiency",
                    "Improved system reliability",
                    "Scalable architecture",
                    "Optimized data processing"
                ],
                "answer": "Operational efficiency"
            },
            {
                "question": f"Organizations adopt {topic} primarily to achieve what objective?",
                "options": [
                    "Improved digital infrastructure",
                    "Enhanced information management",
                    "Better system integration",
                    "Increased computing efficiency"
                ],
                "answer": "Improved digital infrastructure"
            }
        ]

    elif sector == "business":

        quiz = [
            {
                "question": f"How can {topic} contribute to organizational strategy?",
                "options": [
                    "Supporting informed decision making",
                    "Enhancing operational planning",
                    "Improving resource allocation",
                    "Strengthening competitive advantage"
                ],
                "answer": "Supporting informed decision making"
            },
            {
                "question": f"{topic} primarily influences which business function?",
                "options": [
                    "Operational management",
                    "Strategic planning",
                    "Performance monitoring",
                    "Resource management"
                ],
                "answer": "Strategic planning"
            },
            {
                "question": f"What is a major advantage of applying {topic} in business operations?",
                "options": [
                    "Increased productivity",
                    "Better financial management",
                    "Improved decision accuracy",
                    "Enhanced operational efficiency"
                ],
                "answer": "Enhanced operational efficiency"
            },
            {
                "question": f"{topic} can help organizations achieve which outcome?",
                "options": [
                    "Improved organizational performance",
                    "Better market competitiveness",
                    "Efficient business processes",
                    "Enhanced strategic alignment"
                ],
                "answer": "Improved organizational performance"
            }
        ]

    elif sector == "management":

        quiz = [
            {
                "question": f"{topic} helps organizations improve which management capability?",
                "options": [
                    "Team coordination",
                    "Project planning",
                    "Workforce collaboration",
                    "Operational efficiency"
                ],
                "answer": "Team coordination"
            },
            {
                "question": f"{topic} commonly supports which project management objective?",
                "options": [
                    "Effective project execution",
                    "Improved team productivity",
                    "Better communication flow",
                    "Efficient workflow management"
                ],
                "answer": "Effective project execution"
            },
            {
                "question": f"{topic} can enhance organizational success by improving?",
                "options": [
                    "Leadership effectiveness",
                    "Team collaboration",
                    "Project outcomes",
                    "Strategic alignment"
                ],
                "answer": "Team collaboration"
            },
            {
                "question": f"Which workplace outcome results from effective use of {topic}?",
                "options": [
                    "Improved team performance",
                    "Better task prioritization",
                    "Efficient project delivery",
                    "Enhanced workplace coordination"
                ],
                "answer": "Efficient project delivery"
            }
        ]
    elif sector == "programming":

        quiz = [
        {
            "question": f"In programming, how is time complexity of {topic} usually expressed?",
            "options": [
                "Big-O notation",
                "Binary notation",
                "Decimal notation",
                "Scientific notation"
            ],
            "answer": "Big-O notation"
        },
        {
            "question": f"What is the primary goal of optimizing {topic} in software development?",
            "options": [
                "Reducing execution time and memory usage",
                "Increasing code length",
                "Adding more variables",
                "Reducing readability"
            ],
            "answer": "Reducing execution time and memory usage"
        },
        {
            "question": f"{topic} is commonly analyzed to understand what aspect of an algorithm?",
            "options": [
                "Efficiency",
                "User interface design",
                "Database schema",
                "Network configuration"
            ],
            "answer": "Efficiency"
        },
        {
            "question": f"Which factor most affects the complexity of {topic} in programming?",
            "options": [
                "Input size",
                "Color scheme",
                "Keyboard layout",
                "Operating system theme"
            ],
            "answer": "Input size"
        }
    ]

    else:

        quiz = [
            {
                "question": f"{topic} contributes primarily to which area of scientific development?",
                "options": [
                    "Scientific research",
                    "Technological innovation",
                    "Applied science",
                    "Interdisciplinary studies"
                ],
                "answer": "Scientific research"
            },
            {
                "question": f"Research in {topic} helps scientists understand?",
                "options": [
                    "Natural systems",
                    "Scientific processes",
                    "Environmental interactions",
                    "Technological applications"
                ],
                "answer": "Natural systems"
            },
            {
                "question": f"{topic} plays an important role in advancing?",
                "options": [
                    "Scientific advancement",
                    "Technological progress",
                    "Sustainable development",
                    "Global innovation"
                ],
                "answer": "Scientific advancement"
            },
            {
                "question": f"{topic} is commonly studied in which environment?",
                "options": [
                    "Research institutions",
                    "Scientific laboratories",
                    "Academic universities",
                    "Technology development centers"
                ],
                "answer": "Academic universities"
            }
        ]

    return {"quiz": quiz}


@app.get("/get_explanation")
def get_explanation(topic: str, level: str):

    explanation = f"{topic} explanation designed for {level} level learners. This section helps learners understand the key concepts, importance, and real-world applications of the topic."

    return {"explanation": explanation}


@app.get("/get_videos")
def get_videos(topic: str):

    videos = [
        {
            "title": f"{topic} Tutorial",
            "url": f"https://www.youtube.com/results?search_query={topic}+tutorial"
        },
        {
            "title": f"{topic} Lecture",
            "url": f"https://www.youtube.com/results?search_query={topic}+lecture"
        }
    ]

    return {"videos": videos}