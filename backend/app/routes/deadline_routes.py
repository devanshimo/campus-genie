from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Deadline, Student
from ..schemas import DeadlineCreate
# Import the WhatsApp helper function we discussed earlier
from ..services.whatsapp_service import send_whatsapp_message 

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add_deadline")
def add_deadline(
    deadline: DeadlineCreate, 
    background_tasks: BackgroundTasks, # Added BackgroundTasks here
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(Student.id == deadline.student_id).first()

    if not student:
        return {"error": "Student not found"}

    new_deadline = Deadline(
        title=deadline.title,
        date=deadline.date,
        time=deadline.time,
        student_phone=student.phone,
        student_email=student.gmail
    )

    db.add(new_deadline)
    db.commit()

    # Format the personalized WhatsApp message
    msg_body = (
        f"🎓 *CampusFlow Reminder*\n\n"
        f"Hi {student.name},\n"
        f"📌 {deadline.title}\n"
        f"📅 {deadline.date}\n"
        f"⏰ {deadline.time}\n\n"
        f"Make sure to get this done!"
    )

    # Trigger the WhatsApp message to send in the background
    background_tasks.add_task(send_whatsapp_message, student.phone, msg_body)

    return {
        "message": "Deadline added and WhatsApp notification queued",
        "student": student.name
    }