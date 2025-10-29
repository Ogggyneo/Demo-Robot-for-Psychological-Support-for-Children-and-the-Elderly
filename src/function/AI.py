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
mytext = 'Welcome to me'
language = 'en'
openai.api_key='ENTER YOU API_KEY'
load_dotenv()
model = 'gpt-3.5-turbo'
model = 'gpt-4'
client = openai.AsyncOpenAI(api_key=openai.api_key)
r = sr.Recognizer()
engine = pyttsx3.init("dummy")
voice = engine.getProperty('voices')[1]
engine.setProperty('voice', voice.id)
name = "everyone"
greetings = [f"whats up master {name}",
             "yeah?",
             "Well, hello there, Master of Puns and Jokes - how's it going today?",
             f"Ahoy there, Captain {name}! How's the ship sailing?",
             f"Bonjour, Monsieur {name}! Comment ça va? Wait, why the hell am I speaking French?" ]
def listen_for_wake_word(source):
    print("Listening for 'Hi friend' or 'skill'...")
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(text)
            if 'stop' in text.lower():
                break
            if "hi friend" in text.lower():
                print("Wake word detected.")
                listen_and_respond(source)
                engine.say(np.random.choice(greetings))
                engine.runAndWait()
                break
            elif 'special' in text.lower():
                music_dir = 'Nhạc nhẽo'
                songs = os.listdir(music_dir)
                random.shuffle(songs)
                for song_name in songs :
                    if songs.endswith(".wav"):
                        song_path = os.path.join(music_dir, song_name)
                    print(f'playing... {song_name}')
                    os.startfile(song_path)
            elif "please" in text.lower():
                subprocess.run(["python", "todo.py"])
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
            if "tell me"  in text.lower():
                 print("generating audio")
            response =  openai.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{text}"}])
            if response.choices[0].message.content is not None:
                print(response.choices[0].message.content, end="")
                response_text = response.choices[0].message.content
                print(response_text)
                myobj = gTTS(text = response_text, lang = language, slow = False)
                myobj.save("savefile.mp3")
                print("speaking")
                os.system("savefile.mp3")
                print("speaking")
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
with sr.Microphone() as source:
    listen_for_wake_word(source)