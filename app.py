import streamlit as st
import speech_recognition as sr
import pyttsx3
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import io
from oauth2client.service_account import ServiceAccountCredentials



# Connect to Google Sheet
# def connect_sheet():
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
#     client = gspread.authorize(creds)
#     sheet = client.open("AI Voice Sheet").sheet1
#     sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet.spreadsheet.id}"
#     return sheet, sheet_url

def connect_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    creds_json = os.getenv("GOOGLE_CREDENTIALS")  # Match exactly!
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    
    client = gspread.authorize(creds)
    sheet = client.open("AI Voice Sheet").sheet1
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet.spreadsheet.id}"
    return sheet, sheet_url

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="en-US")
        st.info(f"🗣️ You said: {text}")
        return text
    except:
        return ""
    
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def save_response(sheet, q_id, q_text, answer):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    sheet.append_row([q_id, q_text, answer, timestamp])

def insert_header(sheet):
    headers = ["Question ID", "Question Text", "User Response", "Timestamp"]
    if not sheet.row_values(1):
        sheet.insert_row(headers, 1)




def main():
    st.title("🧠 AI Voice Agent with Google Sheet")
    sheet, sheet_url = connect_sheet()
    sheet.clear()
    insert_header(sheet)

    # Add a start button
    if st.button("🎤 Start Voice Agent"):
        with open("questions.json", "r") as f:
            questions = json.load(f)

        for q in questions:
            while True:
                speak(q["text"])
                user_input = get_voice_input()
                if not user_input:
                    continue
                if user_input:
                    save_response(sheet, q["id"], q["text"], user_input)
                    break

        speak("Thank you for your feedback!")
        st.success("✅ All questions answered. Thank you!")
        st.markdown(f"📊 [View your responses in Google Sheet]({sheet_url})")


if __name__ == "__main__":
    main()
