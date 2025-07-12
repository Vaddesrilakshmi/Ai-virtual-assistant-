import os, webbrowser, requests, datetime, nltk
from gtts import gTTS
import openai, speech_recognition as sr
from io import BytesIO
import tempfile

nltk.download('punkt')

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OWM_API_KEY = os.getenv("OWM_API_KEY")
openai.api_key = OPENAI_API_KEY

def fetch_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=YourCity&appid={OWM_API_KEY}&units=metric"
    r = requests.get(url).json()
    desc = r['weather'][0]['description']
    temp = r['main']['temp']
    return f"It's {desc}, {temp}°C"

def get_time():
    now = datetime.datetime.now()
    return now.strftime("It's %I:%M %p on %B %d, %Y")

def gpt_response(prompt):
    resp = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=150)
    return resp.choices[0].text.strip()

def speak(text, lang="en"):
    tts = gTTS(text=text, lang=lang)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.write_to_fp(tmp)
    tmp.flush()
    return tmp.name

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as mic:
        audio = r.listen(mic)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
