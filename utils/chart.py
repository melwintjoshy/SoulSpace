# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import streamlit as st

# def plot_mood_chart(csv_file_path):
#     """
#     Generate a mood chart from a CSV file and display it using Streamlit.

#     :param csv_file_path: Path to the CSV file.
#     """
#     # Define colors for each emotion
#     emotion_colors = {
#         'anger': 'red',
#         'disgust': 'green',
#         'fear': 'purple',
#         'joy': 'yellow',
#         'neutral': 'gray',
#         'sadness': 'blue',
#         'surprise': 'orange'
#     }

#     # Load the CSV file
#     df = pd.read_csv(csv_file_path)

#     # Convert the 'date' column to datetime
#     df['date'] = pd.to_datetime(df['date'])

#     # Plot the chart
#     plt.figure(figsize=(12, 6))

#     # Plot each emotion with its corresponding color as a line plot
#     for emotion, color in emotion_colors.items():
#         plt.plot(df['date'], df[emotion], color=color, label=emotion)

#     # Format the X-axis to show time properly
#     plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#     plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
#     plt.gcf().autofmt_xdate()  # Rotate date labels

#     # Add labels and title
#     plt.xlabel('Date')
#     plt.ylabel('Intensity')
#     plt.title('Emotion Intensity Over Time')
#     plt.legend(title='Emotions')

#     # Display the chart using Streamlit
#     st.pyplot(plt)

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st

def plot_mood_chart(csv_file_path):
    """
    Generate a weekly mood chart from a CSV file and display it using Streamlit.

    :param csv_file_path: Path to the CSV file.
    """
    # Define colors for each emotion
    emotion_colors = {
        'anger': '#FF7F7F',  # Light Red
        'disgust': '#90EE90',  # Light Green
        'fear': '#DDA0DD',  # Light Purple
        'joy': '#FFFFE0',  # Light Yellow
        'neutral': '#D3D3D3',  # Light Gray
        'sadness': '#ADD8E6',  # Light Blue
        'surprise': '#FFDAB9',  # Light Orang
    }

    # Load the CSV file
    df = pd.read_csv(csv_file_path)

    # Convert the 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Set the 'date' column as the index
    df.set_index('date', inplace=True)

    # Exclude non-numeric columns (e.g., 'journal' and 'strongest_emotion')
    numeric_df = df.drop(columns=['journal', 'strongest_emotion'])

    # Resample the data by week and calculate the mean for each emotion
    weekly_df = numeric_df.resample('W').mean()

    # Plot the chart
    plt.figure(figsize=(12, 6))

    # Plot each emotion with its corresponding color as a line plot
    for emotion, color in emotion_colors.items():
        plt.plot(weekly_df.index, weekly_df[emotion], color=color, label=emotion, marker='o')

    # Format the X-axis to show time properly
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))  # Show weekly ticks
    plt.gcf().autofmt_xdate()  # Rotate date labels

    plt.tick_params(axis='x', which='both', bottom=False, labelbottom=False)  # Hide X-axis tick labels
    plt.tick_params(axis='y', which='both', left=False, labelleft=False)  

    # Add labels and title
    plt.xlabel('Week')
    plt.ylabel('Average Intensity')
    plt.title('Weekly Emotion Intensity Over Time')
    plt.legend(title='Emotions')

    # Display the chart using Streamlit
    st.pyplot(plt)