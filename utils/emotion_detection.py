# utils/emotion_detection.py
import requests
import csv
from datetime import datetime


# Hugging Face API details
API_TOKEN = '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'
API_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    """Query the Hugging Face API for emotion detection."""
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def append_to_csv(date, journal, emotion_scores, strongest_emotion):
    """Append journal entry and emotion scores to a CSV file."""
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

def detect_emotion(journal_entry):
    """Detect emotions from a journal entry and return scores and strongest emotion."""
    output = query({"inputs": journal_entry})
    
    if isinstance(output, list) and len(output) > 0:
        emotions = output[0]
        emotion_scores = {emotion['label']: round(emotion['score'], 4) for emotion in emotions}
        
        # Ensure all emotions exist in the correct order
        all_emotions = ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]
        scores = [emotion_scores.get(emotion, 0.0) for emotion in all_emotions]

        # Find the strongest emotion
        strongest_emotion = max(emotion_scores, key=emotion_scores.get)
    else:
        scores = [0.0] * 7
        strongest_emotion = "None"
    
    return scores, strongest_emotion