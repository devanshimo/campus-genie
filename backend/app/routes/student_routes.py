from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import SessionLocal
from ..models import Student
from ..schemas import StudentCreate

router = APIRouter()

# --- 1. NEW LOGIN SCHEMA ---
# We define what the incoming login package should look like
class LoginRequest(BaseModel):
    phone: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 2. NEW LOGIN ROUTE ---
@router.post("/login")
def login_student(req: LoginRequest, db: Session = Depends(get_db)):
    # Check if the phone number exists in the database
    student = db.query(Student).filter(Student.phone == req.phone).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Player not found. Register first!")
    
    # Return the full student object (including ID) back to Streamlit
    return student


# --- 3. UPDATED REGISTRATION ROUTE ---
@router.post("/register_student")
def register_student(student: StudentCreate, db: Session = Depends(get_db)):
    
    # Check if someone is already registered with this phone number
    existing_student = db.query(Student).filter(Student.phone == student.phone).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="Number already registered! Please login.")

    # If it is a new number, create the student
    new_student = Student(
        name=student.name,
        phone=student.phone,
        gmail=student.gmail
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    # CRITICAL FIX: Return the full 'new_student' object, not just a message. 
    # This allows Streamlit to read new_student.id and save it!
    return new_student