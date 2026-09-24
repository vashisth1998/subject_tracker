import streamlit as st
import json
import os
import time
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="CS Revision Tracker", page_icon="💻", layout="centered")

DATA_FILE = "study_data.json"

# --- DATA MANAGEMENT ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    # Default CS subjects pre-loaded
    return {
        "subjects": {
            "Theory of Computation": {"target": 5, "completed": 0},
            "Compiler Design": {"target": 3, "completed": 0},
            "Computer Networks": {"target": 4, "completed": 0},
            "Operating Systems": {"target": 4, "completed": 0},
            "DBMS & SQL": {"target": 5, "completed": 0},
            "COA": {"target": 3, "completed": 0},
            "Data Structures & Algorithms": {"target": 5, "completed": 0}
        },
        "logs": [] # To track daily study history
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

if 'app_data' not in st.session_state:
    st.session_state.app_data = load_data()

# Helper function to log activity
def log_activity(msg):
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.app_data["logs"].insert(0, f"[{today}] {msg}")
    # Keep only last 20 logs
    st.session_state.app_data["logs"] = st.session_state.app_data["logs"][:20]
    save_data(st.session_state.app_data)

# --- UI HEADER ---
st.title("💻 Computer Science Tracker")
st.markdown("Track syllabus progress, manage daily video targets, and use Pomodoro.")

# --- TABS FOR FULL-FLEDGED APP ---
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🍅 Pomodoro", "📝 Study Logs"])

# ================= TAB 1: DASHBOARD =================
with tab1:
    # Add New Subject Expander
    with st.expander("🎯 Set New Target / Add Subject"):
        new_sub = st.text_input("Subject Name")
        new_target = st.number_input("Target Videos/Topics", min_value=1, value=1, step=1)
        
        if st.button("Add / Update Subject", use_container_width=True):
            if new_sub:
                st.session_state.app_data["subjects"][new_sub] = {"target": new_target, "completed": 0}
                log_activity(f"Added new target: {new_sub} ({new_target} videos)")
                st.success(f"Added {new_sub}!")
                st.rerun()
            else:
                st.error("Please enter a subject name.")

    # Reset Progress Button
    if st.button("🔄 Reset All Progress for Today", use_container_width=True):
        for sub in st.session_state.app_data["subjects"]:
            st.session_state.app_data["subjects"][sub]["completed"] = 0
        log_activity("Reset all daily progress counters.")
        st.rerun()

    st.divider()
    st.subheader("Today's Revision Progress")

    if not st.session_state.app_data["subjects"]:
        st.info("No subjects added yet.")

    # Subject Iteration
    for subject in list(st.session_state.app_data["subjects"].keys()):
        data = st.session_state.app_data["subjects"][subject]
        
        # Display Subject Name
        st.markdown(f"#### {subject}")
        
        target = data["target"]
        completed = data["completed"]
        
        # Progress Bar Estimator
        progress_val = min(completed / target, 1.0)
        st.progress(progress_val)
        
        # Action Buttons (Watch | Delete)
        col1, col2, col3 = st.columns([3, 3, 2])
        
        with col1:
            st.write(f"**Completed:** {completed}/{target}")
            if completed >= target:
                st.success("🎉 Achieved!")
                
        with col2:
            if completed < target:
                if st.button("➕ Watch 1", key=f"btn_{subject}", use_container_width=True):
                    st.session_state.app_data["subjects"][subject]["completed"] += 1
                    log_activity(f"Watched 1 video for {subject}")
                    st.rerun()
                    
        with col3:
            if st.button("🗑️ Del", key=f"del_{subject}", use_container_width=True):
                del st.session_state.app_data["subjects"][subject]
                log_activity(f"Deleted subject: {subject}")
                st.rerun()
                
        st.markdown("---")

# ================= TAB 2: POMODORO TIMER =================
with tab2:
    st.header("🍅 Pomodoro Timer")
    st.markdown("Use block scheduling to maintain focus during long study sessions.")
    
    pomodoro_time = st.selectbox("Select Block Duration", [25, 50, 90], index=0, format_func=lambda x: f"{x} Minutes")
    
    start_pomodoro = st.button("▶️ Start Focus Session", type="primary", use_container_width=True)
    timer_placeholder = st.empty()
    
    if start_pomodoro:
        # Convert minutes to seconds
        total_seconds = pomodoro_time * 60
        log_activity(f"Started a {pomodoro_time}-minute Pomodoro session.")
        
        for ts in range(total_seconds, -1, -1):
            mins, secs = divmod(ts, 60)
            timer_placeholder.markdown(f"<h1 style='text-align: center; color: #ff4b4b;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
            time.sleep(1)
            
        st.success(f"🍅 {pomodoro_time} Minutes Complete! Take a break.")
        log_activity(f"Completed a {pomodoro_time}-minute Pomodoro session.")
        st.balloons()

# ================= TAB 3: STUDY LOGS =================
with tab3:
    st.header("📝 Daily History & Logs")
    st.markdown("Track your consistency and see what you accomplished recently.")
    
    if not st.session_state.app_data["logs"]:
        st.info("No activity logged yet.")
    else:
        for log in st.session_state.app_data["logs"]:
            st.text(log)
            
    if st.button("Clear Logs"):
        st.session_state.app_data["logs"] = []
        save_data(st.session_state.app_data)
        st.rerun()
