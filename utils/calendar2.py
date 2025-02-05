import pandas as pd
import calendar
import streamlit as st
# Define lighter emotion colors
emotion_colors = {
    'anger': '#FF7F7F',  # Light Red
    'disgust': '#90EE90',  # Light Green
    'fear': '#DDA0DD',  # Light Purple
    'joy': '#FFFFE0',  # Light Yellow
    'neutral': '#D3D3D3',  # Light Gray
    'sadness': '#ADD8E6',  # Light Blue
    'surprise': '#FFDAB9',  # Light Orange
}

# Define emojis for each emotion
emotion_emojis = {
    'anger': '😡',  # Angry face
    'disgust': '🤢',  # Nauseated face
    'fear': '😨',  # Fearful face
    'joy': '😊',  # Smiling face
    'neutral': '😐',  # Neutral face
    'sadness': '😢',  # Crying face
    'surprise': '😮',  # Surprised face
}

# Load the CSV file
def load_journal_data():
    return pd.read_csv('emotions_journal.csv')

# Function to display calendar with emotions
def display_calendar(year, month, journal_data):
    # Create a calendar
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    
    # Display the calendar
    st.write(f"## {month_name} {year}")
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].write("")  # Empty cell for days outside the month
            else:
                date_str = f"{month:02d}-{day:02d}-{year}"
                entry = journal_data[journal_data['date'] == date_str]
                if not entry.empty:
                    strongest_emotion = entry['strongest_emotion'].values[0]
                    emotion_color = emotion_colors.get(strongest_emotion, '#FFFFFF')  # Default to white if not found
                    cols[i].markdown(
                        f"<div style='background-color: {emotion_color}; padding: 20px; border-radius: 5px; text-align: center; color: white; font-size: 18px;'>{day}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    cols[i].markdown(
                        f"<div style='background-color: #FFFFFF; padding: 20px; border-radius: 5px; text-align: center; color: black; font-size: 18px;'>{day}</div>",
                        unsafe_allow_html=True
                    )

# Function to display the legend
def display_legend():
    st.write("### Legend")
    cols = st.columns(7)
    for i, (emotion, color) in enumerate(emotion_colors.items()):
        emoji = emotion_emojis.get(emotion, '')
        cols[i].markdown(
            f"<div style='background-color: {color}; padding: 10px; border-radius: 5px; text-align: center; color: white; font-size: 14px;'>{emoji} {emotion}</div>",
            unsafe_allow_html=True
        )