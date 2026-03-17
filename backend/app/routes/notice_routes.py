from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from ..schemas import NoticeInput
from ..services.ai_parser import parse_notice
from ..database import get_db  # Make sure this import matches your database.py location

from ..services.whatsapp_service import broadcast_whatsapp_reminder 

router = APIRouter()

@router.post("/parse_notice")
def parse_notice_route(
    data: NoticeInput, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    # 1. Parse the unstructured text using your Llama-3 parser
    result = parse_notice(data.notice_text)
    
    # 2. Safety check: Don't broadcast if the API failed or parsing broke
    error_titles = ["API Error", "Parsing Failed", "Server Error"]
    
    if result.get("title") and result.get("title") not in error_titles:
        # 3. Hand off the WhatsApp broadcasting to a background thread
        background_tasks.add_task(
            broadcast_whatsapp_reminder,
            db=db,
            title=result.get("title", "Important Notice"),
            date=result.get("date", "Date TBD"),
            time=result.get("time", "Time TBD")
        )
        
    # 4. Return the result immediately to Streamlit so the UI updates fast
    return result