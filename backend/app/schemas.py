from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    phone: str
    gmail: str


class DeadlineCreate(BaseModel):
    title: str
    date: str
    time: str
    student_id: int
    student_id: int    # <-- MAKE SURE THIS LINE IS HERE
    student_phone: str # <-- MUST BE HERE
    student_email: str

class NoticeInput(BaseModel):
    notice_text: str