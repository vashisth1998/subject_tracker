import streamlit as st

# Page configuration
st.set_page_config(page_title="Revision Tracker", page_icon="📚", layout="wide")

st.title("📚 Daily Subject Revision Dashboard")
st.markdown("Track your daily video targets and revision schedule.")

# Initialize session state dictionary to hold subjects and their targets
if 'study_data' not in st.session_state:
    # Default subjects added for example
    st.session_state.study_data = {
        "Theory of Computation": {"target": 4, "completed": 0},
        "DBMS": {"target": 3, "completed": 0},
        "Computer Networks": {"target": 2, "completed": 0}
    }

# ----------------- SIDEBAR: ADD OR UPDATE TARGETS -----------------
with st.sidebar:
    st.header("🎯 Set Today's Target")
    
    new_sub = st.text_input("Subject Name")
    new_target = st.number_input("Target Videos/Topics", min_value=1, value=1, step=1)
    
    if st.button("Add / Update Subject"):
        if new_sub:
            # Add new subject or reset target for existing one
            st.session_state.study_data[new_sub] = {"target": new_target, "completed": 0}
            st.success(f"Added {new_sub} with target {new_target}!")
        else:
            st.error("Please enter a subject name.")
            
    st.divider()
    if st.button("Reset All Progress for Today"):
        for sub in st.session_state.study_data:
            st.session_state.study_data[sub]["completed"] = 0
        st.rerun()

# ----------------- MAIN DASHBOARD -----------------
st.header("📊 Today's Progress")

# If no subjects exist yet
if not st.session_state.study_data:
    st.info("No subjects added yet. Please add a subject from the sidebar.")

# Iterate through all subjects and display their progress
for subject, data in st.session_state.study_data.items():
    st.subheader(subject)
    
    target = data["target"]
    completed = data["completed"]
    
    # Create 3 columns for layout: Progress Bar | Button | Status Message
    col1, col2, col3 = st.columns([3, 1, 1.5])
    
    with col1:
        # Calculate percentage for progress bar (capped at 1.0 or 100%)
        progress_val = min(completed / target, 1.0)
        st.progress(progress_val)
        st.write(f"**Videos Watched:** {completed} / {target}")
        
    with col2:
        # Button to increment completed videos
        # Using a unique key for each button based on subject name
        if st.button(f"➕ Watch 1 Video", key=f"btn_{subject}"):
            st.session_state.study_data[subject]["completed"] += 1
            st.rerun()
            
    with col3:
        # Show success message if target is met
        if completed >= target:
            st.success("🎉 Target Achieved!")
            
    st.divider()
