# utils/calendar_utils.py
# import pandas as pd
# import calendar
# from datetime import datetime

# def create_calendar_df(year, month):
#     """Create a calendar DataFrame for the given year and month."""
#     cal = calendar.monthcalendar(year, month)
#     df = pd.DataFrame(cal)
#     df.columns = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']
#     return df.replace(0, '')

# def color_calendar(cal_df, journal_data, year, month):
#     """Color-code the calendar based on the strongest emotion for each day."""
#     for i, row in cal_df.iterrows():
#         for j, day in enumerate(row):
#             if day != '':
#                 date_str = f"{year}-{month:02d}-{int(day):02d}"
#                 date = pd.to_datetime(date_str)
#                 entry = journal_data[journal_data['date'] == date]
#                 if not entry.empty:
#                     strongest_emotion = entry['strongest_emotion'].values[0]
#                     # print(strongest_emotion)
#                     # Assign colors based on emotion
#                     colors = {
#                         'anger': '#FF7F7F',  # Light Red
#                         'disgust': '#90EE90',  # Light Green
#                         'fear': '#DDA0DD',  # Light Purple
#                         'joy': '#FFFFE0',  # Light Yellow
#                         'neutral': '#D3D3D3',  # Light Gray
#                         'sadness': '#ADD8E6',  # Light Blue
#                         'surprise': '#FFDAB9',  # Light Orange
#                     }
#                     cal_df.iloc[i, j] = f'<div style="background-color: {colors.get(strongest_emotion, colors[strongest_emotion])}; color: black; text-align: center;">{day}</div>'
#     return cal_df

# def load_journal_data():
#     """Load journal data from the CSV file."""
#     try:
#         journal_data = pd.read_csv("emotions_journal.csv")
#         journal_data['date'] = pd.to_datetime(journal_data['date'])
#         return journal_data
#     except FileNotFoundError:
#         return pd.DataFrame(columns=["date", "journal", "anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise", "strongest_emotion"])


# utils/calendar_utils.py
import pandas as pd
import calendar
from datetime import datetime

def create_calendar_df(year, month):
    """Create a calendar DataFrame for the given year and month."""
    cal = calendar.monthcalendar(year, month)
    df = pd.DataFrame(cal)
    df.columns = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']
    return df.replace(0, '')

def color_calendar(cal_df, journal_data, year, month):
    """Color-code the calendar based on the strongest emotion for each day."""
    for i, row in cal_df.iterrows():
        for j, day in enumerate(row):
            if day != '':
                date_str = f"{year}-{month:02d}-{int(day):02d}"
                date = pd.to_datetime(date_str)
                entry = journal_data[journal_data['date'] == date]
                if not entry.empty:
                    strongest_emotion = entry['strongest_emotion'].values[0]
                    # Assign colors based on emotion
                    colors = {
                        'anger': '#FF7F7F',  # Light Red
                        'disgust': '#90EE90',  # Light Green
                        'fear': '#DDA0DD',  # Light Purple
                        'joy': '#FFFFE0',  # Light Yellow
                        'neutral': '#D3D3D3',  # Light Gray
                        'sadness': '#ADD8E6',  # Light Blue
                        'surprise': '#FFDAB9',  # Light Orange
                    }
                    cal_df.iloc[i, j] = f'<div style="background-color: {colors.get(strongest_emotion, colors[strongest_emotion])}; color: black; text-align: center;">{day}</div>'
    return cal_df

def load_journal_data():
    """Load journal data from the CSV file."""
    try:
        journal_data = pd.read_csv("emotions_journal.csv")
        journal_data['date'] = pd.to_datetime(journal_data['date'])
        return journal_data
    except FileNotFoundError:
        return pd.DataFrame(columns=["date", "journal", "anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise", "strongest_emotion"])

def generate_legend():
    """Generate an HTML legend for the color codes."""
    colors = {
        'anger': '#FF7F7F',  # Light Red
        'disgust': '#90EE90',  # Light Green
        'fear': '#DDA0DD',  # Light Purple
        'joy': '#FFFFE0',  # Light Yellow
        'neutral': '#D3D3D3',  # Light Gray
        'sadness': '#ADD8E6',  # Light Blue
        'surprise': '#FFDAB9',  # Light Orange
    }
    legend_html = '<div style="display: flex; flex-wrap: wrap;">'
    for emotion, color in colors.items():
        legend_html += f'<div style="background-color: {color}; color: black; padding: 5px; margin: 5px; text-align: center;">{emotion.capitalize()}</div>'
    legend_html += '</div>'
    return legend_html