import os
from twilio.rest import Client
from sqlalchemy.orm import Session
from ..models import Student
import re

def clean_phone_number(phone: str) -> str:
    """Forcefully removes 'whatsapp:', spaces, and non-digits."""
    if not phone:
        return ""
    
    # 1. Remove the word 'whatsapp:' if it exists
    phone = phone.replace("whatsapp:", "")
    
    # 2. Remove EVERY character that isn't a digit or a plus sign (including spaces)
    # This regex [^\d+] means: "Anything that is NOT a digit or a +" -> Delete it.
    cleaned = re.sub(r"[^\d+]", "", phone)
    
    # 3. Final safety: ensure it starts with '+'
    if not cleaned.startswith("+"):
        cleaned = "+" + cleaned
        
    return cleaned

def get_twilio_client():
    """Helper function to initialize the Twilio client."""
    # Move the getenv calls INSIDE the function!
    # This guarantees they are only checked at execution time, not import time.
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

    if not all([account_sid, auth_token, whatsapp_number]):
        print("⚠️ Missing Twilio credentials in .env!")
        return None
        
    return Client(account_sid, auth_token)

def send_whatsapp_message(to_phone_number: str, message: str):
    """Sends a WhatsApp message to a single phone number."""
    client = get_twilio_client()
    if not client:
        return False

    # Ensure the phone number has the '+' country code
    if not to_phone_number.startswith("+"):
        to_phone_number = "+" + to_phone_number

    # Get the sender number fresh from memory
    from_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

    try:
        client.messages.create(
            from_=f"whatsapp:{from_number}",
            body=message,
            to=f"whatsapp:{to_phone_number}"
        )
        print(f"✅ WhatsApp message queued for {to_phone_number}")
        return True
    except Exception as e:
        print(f"❌ Failed to send WhatsApp message to {to_phone_number}: {e}")
        return False

def broadcast_whatsapp_reminder(db: Session, title: str, date: str, time: str):
    """Fetches all registered students and broadcasts a notice reminder."""
    client = get_twilio_client()
    if not client:
        return

    # Format the broadcast message
    message_body = (
        f"🎓 *CampusFlow Alert*\n\n"
        f"📌 *{title}*\n"
        f"📅 Date: {date}\n"
        f"⏰ Time: {time}\n\n"
        f"Stay on top of it!"
    )

    # Fetch all registered students from the database
    students = db.query(Student).all()
    
    if not students:
        print("⚠️ No students registered to receive messages.")
        return

    # Get the sender number fresh from memory
    from_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

    # Loop through and send the message to everyone
    for student in students:
        if not student.phone:
            continue # Skip if the student doesn't have a phone number saved
            
        phone = student.phone
        if not phone.startswith("+"):
            phone = "+" + phone
            
        try:
            client.messages.create(
                from_=f"whatsapp:{from_number}",
                body=message_body,
                to=f"whatsapp:{phone}"
            )
            print(f"✅ Broadcast sent to {student.name} ({phone})")
        except Exception as e:
            print(f"❌ Failed to send broadcast to {phone}: {e}")