🤖 Demo Robot for Psychological Support for Children and the Elderly

This project is an AI-powered interactive assistant designed to provide psychological and emotional support for children and the elderly.
It listens, speaks, and interacts using natural language — powered by OpenAI GPT models, speech recognition, and text-to-speech (TTS) engines.
The robot can also integrate with hardware components such as motors and OLED displays for a more engaging experience.

🧠 Features

🎤 Voice Interaction — Understands and responds to voice commands.

💬 AI Chat — Uses GPT-4 for empathetic and intelligent dialogue.

🔊 Speech Output — Speaks responses using gTTS and pyttsx3.

🎵 Music Mode — Plays random songs from a directory when triggered.

⚙️ Modular Hardware Control — Supports scripts for motor and OLED display control.

🎧 Audio Recording Tools — Includes scripts to record and split voice data.

📂 Project Structure
📁 Psychological Support Robot
│
├── AI.py              # Early prototype of the assistant
├── MARO10.py          # Original robot control version
├── Maro10.1.py        # Main program (recommended)
├── collect.py         # Record audio clips
├── chunk_1.py         # Split audio into chunks
├── config.json        # Configuration file for OpenAI, speech, and hardware
└── README.md          # Documentation file

⚙️ Installation
1. Clone or extract the project
git clone https://github.com/yourusername/psych-support-robot.git
cd psych-support-robot

2. Install dependencies

Install the required packages:

pip install openai python-dotenv speechrecognition pyttsx3 gTTS numpy pyaudio pydub

3. Set up your API key

Edit the config.json file:

{
  "openai": {
    "api_key": "YOUR_OPENAI_API_KEY",
    "model": "gpt-4"
  }
}


Or create a .env file with:

OPENAI_API_KEY=YOUR_OPENAI_API_KEY

▶️ Running the Assistant

Run the main program:

python Maro10.1.py


The robot will:

Listen for wake words (hi friend, special)

Respond to user speech

Play music when triggered

Optionally start motor and OLED display control threads

🎙️ Voice Commands
Command	Description
“Hi friend”	Activates AI listening mode
“Stop”	Stops listening
“Special”	Plays random music
“Please”	Runs a secondary script (like a to-do list)
Other speech	Generates a GPT-4 conversational reply
🧩 Optional Scripts

collect.py — Records live microphone input and saves audio.

python collect.py --seconds 5 --save_path voice.wav


chunk_1.py — Splits long recordings into smaller .wav chunks.

python chunk_1.py --audio_file_name voice.wav --seconds 10 --save_path ./SAVE_FILE/

⚙️ Configuration

Edit config.json to modify settings such as wake words, stop words, language, and connected modules.

Example:

"speech_recognition": {
  "language": "en",
  "wake_words": ["hi friend", "special"],
  "stop_word": "stop"
}

🧠 Future Development Ideas

Emotion detection using tone analysis

Facial recognition for user identification

Local chatbot fallback when offline

Logging system for therapy session summaries

⚠️ Important Notes

Ensure your microphone and speakers are properly configured.

Replace placeholder API keys in config.json.

Some scripts may reference external files (like motor.py, oled.py, or todo.py).

👩‍💻 Author

Demo Robot for Psychological Support
Created for assisting children and the elderly through conversational AI.
© 2025 – All rights reserved.
