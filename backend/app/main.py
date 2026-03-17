from fastapi import FastAPI
from dotenv import load_dotenv # <-- 1. Import this

# 2. Load the .env file BEFORE importing your database or routes!
# This ensures every file in your app has access to the keys immediately.
load_dotenv("backend/.env") 

from .database import engine
from .models import Base
from fastapi.middleware.cors import CORSMiddleware
from .routes import student_routes, deadline_routes, notice_routes


app = FastAPI(title="Campus Genie API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"], # Your Streamlit URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create database tables
Base.metadata.create_all(bind=engine)

app.include_router(student_routes.router)
app.include_router(deadline_routes.router)
app.include_router(notice_routes.router)


@app.get("/")
def root():
    return {"message": "Campus Genie backend running"}