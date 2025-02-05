import requests
import csv
from datetime import datetime

# Hugging Face API details
API_TOKEN = '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'
API_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Function to query the Hugging Face API
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Function to append data to a CSV file
def append_to_csv(date, journal, emotion_scores, strongest_emotion):
    csv_file = "emotions_journal.csv"
    headers = ["date", "journal", "anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise", "strongest_emotion"]

    # Write headers if the file doesn't exist
    try:
        with open(csv_file, "x", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
    except FileExistsError:
        pass  # File already exists

    # Append new data
    with open(csv_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([date, journal] + emotion_scores + [strongest_emotion])

# Journal entry input
journal_entry = """
I don’t even know where to begin. Today has been a storm—no, a full-blown hurricane—of emotions.

Morning started with excitement. I woke up to a message I’d been waiting for—an opportunity I thought was out of reach. For a moment, I felt unstoppable, like everything was finally aligning. But then, almost immediately, doubt crept in. Do I even deserve this? What if I fail?

By noon, frustration had taken over. A simple conversation turned into an argument, and suddenly, I was trapped in this cycle of replaying every word, thinking of better things I could’ve said. It’s strange how quickly anger fades into regret. Why do I let my temper win?

And then there was that moment of pure sadness. I don’t even know where it came from—maybe the weight of expectations, maybe just exhaustion. It sat heavy on my chest, this unshakable loneliness, even when surrounded by people. I felt invisible, unheard.

But tonight… I found a little piece of peace. A small thing—just stepping outside, feeling the cold air on my face. The world kept moving, and for once, I didn’t feel like I had to race to keep up. Maybe that’s what joy is—those fleeting moments where nothing needs to be perfect.

I don’t know what tomorrow holds, but I hope it's a little lighter.
"""

# Get current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Query the Hugging Face API with the journal entry
output = query({"inputs": journal_entry})

# Extract scores
if isinstance(output, list) and len(output) > 0:
    emotions = output[0]
    emotion_scores = {emotion['label']: round(emotion['score'], 4) for emotion in emotions}
    
    # Ensure all emotions exist in the correct order
    all_emotions = ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]
    scores = [emotion_scores.get(emotion, 0.0) for emotion in all_emotions]

    # Find the strongest emotion (no threshold)
    strongest_emotion = max(emotion_scores, key=emotion_scores.get)
else:
    scores = [0.0] * 7
    strongest_emotion = "None"

# Store and display results
append_to_csv(current_date, journal_entry, scores, strongest_emotion)
print(f"Date: {current_date}")
print(f"Journal Entry: {journal_entry.strip()[:100]}...")  # Print first 100 characters
print(f"Emotion Scores: {dict(zip(all_emotions, scores))}")
print(f"Strongest Emotion: {strongest_emotion}")
