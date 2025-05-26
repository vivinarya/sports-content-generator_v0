import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print("GROQ_API_KEY loaded:", api_key is not None)  # Debug key loading

client = Groq(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    sport: str
    content_type: str
    tone: str
    length: str
    language: str

@app.post("/generate")
async def generate_content(req: GenerateRequest):
    prompt = (
        f"Generate a {req.length} {req.content_type.replace('_', ' ')} for {req.sport} "
        f"in a {req.tone} tone. Language: {req.language}."
    )
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content
    except Exception as e:
        content = f"Error generating content: {str(e)}"
    return {"content": content}

@app.get("/")
def read_root():
    return {"message": "Hello, Sports AI!"}

