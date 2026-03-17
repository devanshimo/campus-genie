import streamlit as st
import requests
import base64
import os
from datetime import datetime, date, time
import random

# --- CONFIGURATION ---
# Using 127.0.0.1 is much more reliable than localhost on Windows
API_URL = "https://campusgenie-xyz.onrender.com"
st.set_page_config(page_title="CampusGenie", page_icon="🧞", layout="wide")

# --- LOAD LOGO AS BASE64 ---
def get_logo_b64():
    for logo_path in ["logo.png", "./logo.png"]:
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

LOGO_B64 = get_logo_b64()
LOGO_TAG = f'<img src="data:image/png;base64,{LOGO_B64}" style="width:56px;height:56px;object-fit:contain;image-rendering:pixelated;" />' if LOGO_B64 else "🧞"
LOGO_SMALL = f'<img src="data:image/png;base64,{LOGO_B64}" style="width:36px;height:36px;object-fit:contain;image-rendering:pixelated;" />' if LOGO_B64 else "🧞"

def try_api(method, endpoint, payload):
    if method == "POST":
        try:
            r = requests.post(f"{API_URL}/{endpoint}", json=payload, timeout=5)
            if r.status_code == 200:
                return r.json()
            else:
                print(f"API Error {r.status_code}: {r.text}")
                return None
        except Exception as e:
            print(f"Connection Error: {e}")
            return None
    return None

# ── PIXEL ART CSS ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323:wght@400&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }

/* Background with subtle pixel grid */
.stApp {
    background-color: #060d1a !important;
    background-image:
        linear-gradient(rgba(30,111,168,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(30,111,168,0.04) 1px, transparent 1px) !important;
    background-size: 24px 24px !important;
    color: #c8dff0 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0a1628 !important;
    border-right: 3px solid #1e4d7a !important;
}
[data-testid="stSidebar"] * { color: #6a9bbf !important; }

#MainMenu, footer, header { visibility: hidden; }

/* Pixel title font */
h1 {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 1.8rem !important;
    color: #f5c842 !important;
    text-shadow: 3px 3px 0px #b8860b, 6px 6px 0px rgba(0,0,0,0.4) !important;
    letter-spacing: 0.02em !important;
    line-height: 1.4 !important;
    margin-bottom: 0 !important;
}

h2 {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 0.9rem !important;
    color: #5bc4f5 !important;
    letter-spacing: 0.05em !important;
    text-shadow: 2px 2px 0px #0a4a6e !important;
}

h3, h4 {
    font-family: 'VT323', monospace !important;
    font-size: 1.5rem !important;
    color: #5bc4f5 !important;
    letter-spacing: 0.05em !important;
}

/* Pixel-style tabs */
[data-testid="stTabs"] button {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 0.55rem !important;
    color: #3a6a8a !important;
    border-radius: 0 !important;
    border: 2px solid transparent !important;
    border-bottom: 3px solid transparent !important;
    padding: 0.8rem 1.2rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.04em !important;
    background: transparent !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #f5c842 !important;
    border-bottom: 3px solid #f5c842 !important;
    text-shadow: 1px 1px 0px #8b6914 !important;
    background: rgba(245,200,66,0.05) !important;
}
[data-testid="stTabs"] button:hover {
    color: #5bc4f5 !important;
    background: rgba(91,196,245,0.05) !important;
}

/* Pixel input fields */
input, textarea {
    background: #0d1e33 !important;
    border: 2px solid #1e4d7a !important;
    border-radius: 0 !important;
    color: #c8dff0 !important;
    font-family: 'DM Sans', sans-serif !important;
    box-shadow: 3px 3px 0px #0a1628 !important;
    transition: border-color 0.15s !important;
}
input:focus, textarea:focus {
    border-color: #f5c842 !important;
    box-shadow: 3px 3px 0px #8b6914 !important;
    outline: none !important;
}

/* Labels */
label {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 0.5rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #3a6a8a !important;
}

/* Primary button — pixel style */
[data-testid="baseButton-primary"],
[data-testid="baseButton-secondaryFormSubmit"] {
    background: #f5c842 !important;
    color: #0a1628 !important;
    font-family: 'Press Start 2P', monospace !important;
    font-weight: 400 !important;
    font-size: 0.55rem !important;
    letter-spacing: 0.06em !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: 4px 4px 0px #8b6914 !important;
    transition: all 0.1s !important;
    text-transform: uppercase !important;
}
[data-testid="baseButton-primary"]:hover,
[data-testid="baseButton-secondaryFormSubmit"]:hover {
    background: #ffd84d !important;
    transform: translate(2px, 2px) !important;
    box-shadow: 2px 2px 0px #8b6914 !important;
}
[data-testid="baseButton-primary"]:active,
[data-testid="baseButton-secondaryFormSubmit"]:active {
    transform: translate(4px, 4px) !important;
    box-shadow: 0px 0px 0px #8b6914 !important;
}

/* Secondary button */
[data-testid="baseButton-secondary"] {
    background: transparent !important;
    color: #3a6a8a !important;
    border: 2px solid #1e4d7a !important;
    border-radius: 0 !important;
    font-family: 'Press Start 2P', monospace !important;
    font-size: 0.5rem !important;
    box-shadow: 3px 3px 0px #0a1628 !important;
    transition: all 0.1s !important;
}
[data-testid="baseButton-secondary"]:hover {
    border-color: #5bc4f5 !important;
    color: #5bc4f5 !important;
    transform: translate(2px, 2px) !important;
    box-shadow: 1px 1px 0px #0a1628 !important;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 0 !important;
    border-left: 4px solid !important;
    background: #0d1e33 !important;
    box-shadow: 3px 3px 0px #060d1a !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #0d1e33 !important;
    border: 2px solid #1e4d7a !important;
    border-radius: 0 !important;
    padding: 1.2rem 1.4rem !important;
    box-shadow: 4px 4px 0px #060d1a !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 0.45rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #3a6a8a !important;
}
[data-testid="stMetricValue"] {
    font-family: 'VT323', monospace !important;
    font-size: 2rem !important;
    font-weight: 400 !important;
    color: #f5c842 !important;
}

hr { border-color: #1e4d7a !important; margin: 1.5rem 0 !important; }

/* Spinner */
[data-testid="stSpinner"] { color: #f5c842 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #060d1a; }
::-webkit-scrollbar-thumb { background: #1e4d7a; }
</style>
""", unsafe_allow_html=True)

# --- STATE ---
if 'activity_log'  not in st.session_state: st.session_state.activity_log  = []
if 'registered'    not in st.session_state: st.session_state.registered    = False
if 'student_name'  not in st.session_state: st.session_state.student_name  = ""
if 'students'      not in st.session_state: st.session_state.students      = []
if 'deadlines'     not in st.session_state: st.session_state.deadlines     = []
if 'student_id'    not in st.session_state: st.session_state.student_id = None
if 'student_phone' not in st.session_state: st.session_state.student_phone = ""
if 'student_email' not in st.session_state: st.session_state.student_email = ""

def log_activity(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.activity_log.insert(0, f"**{ts}** — {msg}")

# --- SIDEBAR ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=180)
    st.markdown("<hr style='border-color:#1e4d7a;margin:0.75rem 0;'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-family:\"Press Start 2P\",monospace;font-size:0.45rem;"
        "color:#3a6a8a;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.75rem;'>"
        "Activity Log</p>",
        unsafe_allow_html=True
    )
    if not st.session_state.activity_log:
        st.markdown("<p style='font-size:0.8rem;color:#2a4a6a;font-family:VT323,monospace;'>No activity yet...</p>", unsafe_allow_html=True)
    else:
        for log in st.session_state.activity_log:
            st.markdown(
                f"<div style='font-size:0.78rem;color:#4a7a9a;padding:5px 0;"
                f"border-bottom:1px solid #0f2540;font-family:VT323,monospace;'>{log}</div>",
                unsafe_allow_html=True
            )
    if st.button("Clear Log"):
        st.session_state.activity_log = []
        st.rerun()

# --- HEADER ---
col_logo, col_title = st.columns([0.4, 3])
with col_logo:
    if os.path.exists("logo.png"):
        st.markdown("<div style='padding-top:0.5rem;'>", unsafe_allow_html=True)
        st.image("logo.png", width=110)
        st.markdown("</div>", unsafe_allow_html=True)
with col_title:
    st.markdown(
        "<div style='padding-top:2.5rem;'>",
        unsafe_allow_html=True
    )
    st.title("CampusGenie")
    st.markdown(
        "<p style='font-family:VT323,monospace;font-size:1.1rem;color:#3a6a8a;"
        "margin-top:-1.5rem;letter-spacing:0.08em;'>AI CAMPUS ASSISTANT // v1.0</p>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<hr style='border-color:#1e4d7a;border-width:2px;'>", unsafe_allow_html=True)

# GATE: Registration
# ============================================================
# GATE: Registration / Login
# ============================================================
if not st.session_state.registered:

    _, col_form, _ = st.columns([1, 2, 1])
    with col_form:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<div style='background:#0d1e33;border:2px solid #1e4d7a;padding:2rem;"
            "box-shadow:6px 6px 0px #060d1a;'>",
            unsafe_allow_html=True
        )
        
        auth_tab1, auth_tab2 = st.tabs(["LOGIN", "REGISTER"])
        
        # --- LOGIN TAB ---
        with auth_tab1:
            st.markdown("<h2 style='font-size:0.75rem;margin-top:1rem;'>EXISTING PLAYER</h2>", unsafe_allow_html=True)
            with st.form("login_form"):
                login_phone = st.text_input("Enter your registered WhatsApp Number", placeholder="+91 XXXXX XXXXX")
                st.markdown("<br>", unsafe_allow_html=True)
                submit_login = st.form_submit_button(">> LOGIN <<", use_container_width=True)
                
                if submit_login:
                    if login_phone:
                        try:
                            r = requests.post(f"{API_URL}/login", json={"phone": login_phone})
                            if r.status_code == 200:
                                data = r.json()
                                st.session_state.registered   = True
                                st.session_state.student_name = data.get("name")
                                st.session_state.student_id   = data.get("id")
                                st.session_state.student_phone = data.get("phone")
                                st.session_state.student_email = data.get("gmail")
                                log_activity(f"Player logged in — {data.get('name')}")
                                st.rerun()
                            elif r.status_code == 404:
                                st.error("Number not found. Please register first!")
                            else:
                                st.error("Server error.")
                        except requests.exceptions.ConnectionError:
                            st.error("⚠ Backend not reachable. Is Uvicorn running?")
                    else:
                        st.warning("Please enter your phone number.")

        # --- REGISTER TAB ---
        with auth_tab2:
            st.markdown("<h2 style='font-size:0.75rem;margin-top:1rem;'>NEW PLAYER</h2>", unsafe_allow_html=True)
            with st.form("registration_form"):
                name  = st.text_input("Full Name")
                phone = st.text_input("WhatsApp Number", placeholder="+91 XXXXX XXXXX")
                gmail = st.text_input("Gmail Address")
                st.markdown("<br>", unsafe_allow_html=True)
                submit_reg = st.form_submit_button(">> START <<", use_container_width=True)

                if submit_reg:
                    if name and phone and gmail:
                        try:
                            r = requests.post(f"{API_URL}/register_student", json={"name": name, "phone": phone, "gmail": gmail})
                            if r.status_code == 200:
                                data = r.json()
                                st.session_state.students.append({"name": name, "phone": phone, "gmail": gmail})
                                st.session_state.registered   = True
                                st.session_state.student_name = name
                                st.session_state.student_id   = data.get("id", 1)
                                st.session_state.student_phone = data.get("phone")
                                st.session_state.student_email = data.get("gmail")
                                log_activity(f"New player registered — {name}")
                                st.rerun()
                            elif r.status_code == 400:
                                st.error("Number already exists! Please use the LOGIN tab.")
                            else:
                                st.error("Server error or Schema mismatch.")
                        except requests.exceptions.ConnectionError:
                            st.error("⚠ Backend not reachable. Is Uvicorn running?")
                    else:
                        st.warning("Please fill in all fields.")

        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# DASHBOARD
# ============================================================
else:
    col_name, col_logout = st.columns([5, 1])
    with col_name:
        st.markdown(
            f"<p style='font-family:\"Press Start 2P\",monospace;font-size:0.45rem;"
            f"color:#3a6a8a;letter-spacing:0.08em;'>"
            f"PLAYER: <span style='color:#f5c842;'>{st.session_state.student_name.upper()}</span></p>",
            unsafe_allow_html=True
        )
    with col_logout:
        if st.button("Switch account"):
            st.session_state.registered   = False
            st.session_state.student_name = ""
            st.session_state.student_id = None
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    tab_deadlines, tab_notices = st.tabs(["Deadlines", "Notice Parser"])

    # ── TAB 2: Deadlines ─────────────────────────────────────
    with tab_deadlines:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Deadlines")
        st.markdown(
            "<p style='font-family:VT323,monospace;font-size:1rem;color:#3a6a8a;'>"
            "Upcoming events — reminders auto-sent via WhatsApp</p>",
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.deadlines:
            for d in st.session_state.deadlines:
                st.markdown(
                    f"""<div style='display:flex;justify-content:space-between;align-items:center;
                        padding:14px 18px;background:#0d1e33;border:2px solid #1e4d7a;
                        margin-bottom:8px;box-shadow:4px 4px 0px #060d1a;'>
                        <div>
                            <p style='margin:0;font-weight:500;font-size:0.95rem;color:#c8dff0;'>{d['title']}</p>
                            <p style='margin:0;font-size:0.85rem;color:#3a6a8a;margin-top:3px;
                                font-family:VT323,monospace;letter-spacing:0.04em;'>
                                {d['date']} · {d['time']}
                            </p>
                        </div>
                        <span style='font-family:"Press Start 2P",monospace;font-size:0.4rem;
                            background:#0a1f10;color:#4ade80;padding:5px 10px;
                            border:1px solid #4ade80;letter-spacing:0.06em;'>UPCOMING</span>
                    </div>""",
                    unsafe_allow_html=True
                )
        else:
            st.info("No deadlines yet.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Add New Deadline")

        with st.form("deadline_form"):
            event_title = st.text_input("Event Title", placeholder="e.g., End Semester Project Submission")
            col1, col2 = st.columns(2)
            with col1:
                event_date = st.date_input("Date")
            with col2:
                event_time = st.time_input("Time")
            st.markdown("<br>", unsafe_allow_html=True)
            submit_deadline = st.form_submit_button(">> Add Deadline <<", use_container_width=True)

            if submit_deadline:
                if event_title:
                    # ✅ FIX: Properly attaching the dynamic student_id
                    res = try_api("POST", "add_deadline", {
                        "title": event_title, 
                        "date": str(event_date), 
                        "time": str(event_time), 
                        "student_id": st.session_state.student_id,
                        "student_phone": st.session_state.student_phone,
                        "student_email": st.session_state.student_email
                    })
                    
                    if res:
                        st.session_state.deadlines.insert(0, {
                            "title": event_title, "date": str(event_date), "time": str(event_time)
                        })
                        st.success("Deadline added. Reminders queued.")
                        log_activity(f"Deadline created — {event_title}")
                        st.rerun()
                    else:
                        st.error("⚠ Backend not reachable or validation error.")
                else:
                    st.warning("Event title is required.")

    # ── TAB 3: Notice Parser ──────────────────────────────────
    with tab_notices:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### AI Notice Parser")
        st.markdown(
            "<p style='font-family:VT323,monospace;font-size:1rem;color:#3a6a8a;'>"
            "Paste a raw college notice — AI extracts the key details instantly</p>",
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)

        notice_text = st.text_area("Paste Notice Here", height=200, placeholder="Paste unstructured college notice text here...")

        if st.button(">> Parse Notice <<", type="primary"):
            if notice_text:
                with st.spinner("Analyzing..."):
                    # ✅ FIX: Matching the NoticeInput Pydantic Schema
                    data = try_api("POST", "parse_notice", {"notice_text": notice_text})
                    
                    if data:
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("<h4>Extracted Details</h4>", unsafe_allow_html=True)
                        st.markdown("<br><br>", unsafe_allow_html=True)

                        col_a, col_b, col_c = st.columns(3)
                        col_a.metric("Title", data.get("title", "N/A"))
                        col_b.metric("Date",  data.get("date",  "N/A"))
                        col_c.metric("Time",  data.get("time",  "N/A"))

                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("#### Key Takeaways")
                        summary = data.get("summary", [])
                        if isinstance(summary, list):
                            for bullet in summary:
                                st.markdown(
                                    f"<div style='padding:10px 14px;margin:6px 0;background:#0d1e33;"
                                    f"border-left:4px solid #f5c842;font-size:0.9rem;color:#c8dff0;"
                                    f"font-family:VT323,monospace;letter-spacing:0.03em;font-size:1rem;'>{bullet}</div>",
                                    unsafe_allow_html=True
                                )
                        else:
                            st.write(summary)

                        log_activity(f"Notice parsed — {data.get('title','')}")
                    else:
                        st.error("⚠ Backend not reachable on port 8000 or Schema Mismatch.")
            else:
                st.warning("Please paste a notice first.")