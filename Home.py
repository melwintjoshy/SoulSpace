# Directory structure:
# your_app/
# ├── app.py              # Main page (homepage)
# ├── pages/
# │   └── chatbot.py      # Chatbot page
# ├── utils/
# │   ├── emotion_detection.py
# │   ├── calendar_utils.py
# │   └── chart.py

# app.py
import pandas as pd
import streamlit as st
from datetime import datetime
from utils.emotion_detection import detect_emotion, append_to_csv
from utils.calendar_utils import load_journal_data, create_calendar_df, color_calendar, generate_legend
from utils.chart import plot_mood_chart

# Set page config
st.set_page_config(page_title="SoulSpace.", layout="wide")

# Custom CSS for dark mode styling
st.markdown("""
   <style>
   .stTextArea textarea {
       height: 300px !important;
   }
   .nav-links {
       text-align: right; 
       color: #E2E8F0;
       font-size: 16px;
   }
   .stSelectbox select {
       background-color: #1E1E1E;
       color: #E2E8F0;
       border: 1px solid #333;
   }
   </style>
""", unsafe_allow_html=True)

# Header with logo
col1, col2 = st.columns([1, 5])
with col1:
   st.markdown("❤ SoulSpace")
with col2:
   st.markdown('<div style="text-align: right; color: #E2E8F0;">Contact Us</div>', unsafe_allow_html=True)

# Main content columns
left_col, right_col = st.columns([1.5, .5])

with left_col:
   # Journal Entry Section
   st.header("What's on your mind? Wanna share?")
   journal_entry = st.text_area("", placeholder="Write your journal entry here...", height=200)
   
   if st.button("Submit Entry"):
       if journal_entry.strip():
           current_date = datetime.now().strftime("%Y-%m-%d")
           scores, strongest_emotion = detect_emotion(journal_entry)
           append_to_csv(current_date, journal_entry, scores, strongest_emotion)
           st.success("Journal entry saved successfully!")
           st.link_button("Do you wanna chat more?","/Companion" )

       else:
           st.error("Please write something in the journal entry.")

   # Add chatbot redirect button
   with st.sidebar:
        custom_title = """
                        <h1 style="font-size: 50px; font-family: 'Helvetica', sans-serif;">SoulSpace</h1>
                       """
        st.markdown(custom_title, unsafe_allow_html=True)
        st.write("Your Digital Journal & Wellness Companion!")
        st.write("")
   # Interactive Tools Section
#    st.header("Interactive Tools")
#    col1, col2, col3 = st.columns(3)
#    with col1:
#        st.link_button("Breathing Exercise", "https://www.youtube.com/watch?v=0BNejY1e9ik")
#    with col2:
#        st.link_button("⏱ Guided Meditation", "https://www.nccih.nih.gov/health/meditation-and-mindfulness-effectiveness-and-safety")
#    with col3:
#        st.link_button("🎧 Calm Music", "https://www.youtube.com/playlist?list=PLQ_PIlf6OzqIEvjMOCAZsD21T6xn9QUP6")

with right_col:
   # Mood Calendar
   st.header("Mood Calendar")
   
   # Initialize session state for calendar navigation
   if 'current_date' not in st.session_state:
       st.session_state.current_date = datetime.now()
   
   # Calendar navigation
   col1, col2, col3 = st.columns([1, 2, 1])
   with col1:
       if st.button("←"):
           if st.session_state.current_date.month == 1:
               st.session_state.current_date = st.session_state.current_date.replace(year=st.session_state.current_date.year - 1, month=12)
           else:
               st.session_state.current_date = st.session_state.current_date.replace(month=st.session_state.current_date.month - 1)
   with col2:
       st.write(st.session_state.current_date.strftime("%B %Y"))
   with col3:
       if st.button("→"):
           if st.session_state.current_date.month == 12:
               st.session_state.current_date = st.session_state.current_date.replace(year=st.session_state.current_date.year + 1, month=1)
           else:
               st.session_state.current_date = st.session_state.current_date.replace(month=st.session_state.current_date.month + 1)
   
   cal_df = create_calendar_df(st.session_state.current_date.year, st.session_state.current_date.month)
   journal_data = load_journal_data()
   cal_df = color_calendar(cal_df, journal_data, st.session_state.current_date.year, st.session_state.current_date.month)
   st.write(cal_df.to_html(escape=False), unsafe_allow_html=True)
   
   # Display the legend
   legend_html = generate_legend()
   st.markdown(legend_html, unsafe_allow_html=True)

left_col1, right_col1 = st.columns([1.2, 1])

with left_col1:
# Display journal entry for selected day with date-only format
    dates = [date.strftime("%Y-%m-%d") for date in journal_data['date'].unique()]  # Convert timestamp to string with date only
    selected_day = st.selectbox(
    "Select a day to view journal entry", 
    options=dates,
    index=len(dates) - 1
    )

    if selected_day:
    # Match the exact date format
        entry = journal_data[journal_data['date'].dt.strftime("%Y-%m-%d") == selected_day]
        if not entry.empty:
            # Display the journal entry
            st.write(f"**Journal Entry for {selected_day}:**")
            st.write(entry['journal'].values[0])

            # Find the strongest emotion
            emotions = entry[['anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise']]
            strongest_emotion = emotions.idxmax(axis=1).values[0]

            # Display the strongest emotion in the desired format
            st.success(f"**The emotion of the day is {strongest_emotion}.**")
    st.header("Interactive Tools")
    col1, col2, col3 = st.columns(3)
    with col1:
       st.link_button("Breathing Exercise", "https://www.youtube.com/watch?v=0BNejY1e9ik")
    with col2:
       st.link_button("⏱ Guided Meditation", "https://www.nccih.nih.gov/health/meditation-and-mindfulness-effectiveness-and-safety")
    with col3:
       st.link_button("🎧 Calm Music", "https://www.youtube.com/playlist?list=PLQ_PIlf6OzqIEvjMOCAZsD21T6xn9QUP6")

with right_col1:
    st.header("Mood Chart")
    plot_mood_chart("emotions_journal.csv")