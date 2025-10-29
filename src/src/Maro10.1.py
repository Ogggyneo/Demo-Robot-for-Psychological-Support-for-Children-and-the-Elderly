import os
import openai
from dotenv import load_dotenv
import time
import datetime
import speech_recognition as sr
import pyttsx3
import numpy as np
from gtts import gTTS
import subprocess
import random
import json
import threading
import importlib

# Load environment variables from .env file
load_dotenv()

# Load configuration from JSON file with error handling
config = {}
try:
    with open("config.json", "r") as file:
        config = json.load(file)
except json.JSONDecodeError:
    print("Error: config.json is not a valid JSON file.")
    exit(1)
except FileNotFoundError:
    print("Error: config.json file not found.")
    exit(1)

# Set OpenAI API key
openai.api_key = config["openai"]["api_key"]

# Set up the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()
voice = engine.getProperty('voices')[1]
engine.setProperty('voice', voice.id)

greetings = config["greetings"]

def listen_for_wake_word(source):
    print(f"Listening for wake words: {config['speech_recognition']['wake_words']}...")
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(text)
            if config['speech_recognition']['stop_word'] in text.lower():
                break
            if any(wake_word in text.lower() for wake_word in config['speech_recognition']['wake_words']):
                print("Wake word detected.")
                listen_and_respond(source)
                engine.say(np.random.choice(greetings))
                engine.runAndWait()
                break
            elif 'special' in text.lower():
                music_dir = config['music']['directory']
                songs = os.listdir(music_dir)
                random.shuffle(songs)
                for song_name in songs:
                    if song_name.endswith(config['music']['file_extension']):
                        song_path = os.path.join(music_dir, song_name)
                        print(f'Playing... {song_name}')
                        os.startfile(song_path)
            elif "please" in text.lower():
                subprocess.run(["python", config['todo']['script']])
        except sr.UnknownValueError:
            pass

def listen_and_respond(source):
    print("Listening...")
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if not text:
                continue
            print(text)
            if "tell me" in text.lower():
                print("Generating audio...")
            response = openai.ChatCompletion.create(
                model=config["openai"]["model"],
                messages=[{"role": "user", "content": text}]
            )
            if response.choices[0].message['content'] is not None:
                response_text = response.choices[0].message['content']
                print(response_text)
                myobj = gTTS(text=response_text, lang=config['speech_recognition']['language'], slow=False)
                myobj.save("savefile.mp3")
                print("Speaking...")
                os.system("start savefile.mp3")
                engine.say(response_text)
                engine.runAndWait()
            if not audio:
                listen_for_wake_word(source)
        except sr.UnknownValueError:
            time.sleep(2)
            print("Silence found, shutting up, listening...")
            listen_for_wake_word(source)
            break
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            engine.say(f"Could not request results; {e}")
            engine.runAndWait()
            listen_for_wake_word(source)
            break

def start_oled_display():
    oled_module = importlib.import_module(config['oled']['script'].replace('.py', ''))
    oled_module.main()

def start_motor():
    motor_module = importlib.import_module(config['motor']['script'].replace('.py', ''))
    motor_module.main()

# Start the OLED display and motor in separate threads
threading.Thread(target=start_oled_display).start()
threading.Thread(target=start_motor).start()

# Start listening for wake words
with sr.Microphone() as source:
    listen_for_wake_word(source)
