"""
Esta es la implementacion del otro archivo que use como prueba
no se si es necesario pero lo pongo porque parece mas eficiente
"""
import pyaudio
import keyboard
import wave
import openai
import speech_recognition as sr
import pyttsx3
import os
import winsound
import sys
from dotenv import load_dotenv
from utils.speech import silero_tts
""" 
no se que mierda pero no funciona
from utils.translate import translate_google
"""
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

load_dotenv()

api_key = os.getenv('tok')
client = openai.OpenAI(api_key=api_key)

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)
context = {"role": "system", "content": "idk"}
messages = [context]

def catch_audio_and_process():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    WAVE_OUTPUT_FILENAME = "input.wav"
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []

    try:
        while keyboard.is_pressed("RIGHT_SHIFT"):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
    except Exception as e:
        print(f"error capturando el audio: {e}")

    print("procesando audio...")
    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    recognizer = sr.Recognizer()
    with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language='es-es')
        print(f"yo: {text}")
        return text
    except sr.UnknownValueError:
        print("no entendi nada ura")
        return None
    except sr.RequestError as e:
        print(f"problema con speechrecognition: {e}")
        return None


def chat_with_gpt(text):
    """
    contexto
    """
    with open("identity.txt", "r", encoding="utf-8") as f:
        identityContext = f.read()
        messages.append({"role": "user", "content": identityContext})
    
    messages.append({"role": "user", "content": text})

    try:
        response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=messages,
                temperature=0.7,
            )
        response_content = response.choices[0].message.content
        messages.append({"role": "assistant", "content": response_content})
        """ 
        pincho totalmente
        textofinal = translate_google(response_content, "es", "en")
        """

        print(f"ia es: {response_content.split('--')[1]}")
        print(f"ia en: {response_content.split('--')[0]}")
        silero_tts(response_content.split('--')[0], "en", "v3_en", "en_21")
        winsound.PlaySound("test.wav", winsound.SND_FILENAME)
    except Exception as e:
        print(f"error: {e}")


print("apreta shhift derecho para hablar")
while True:
    try:
        if keyboard.is_pressed('RIGHT_SHIFT'):
            user_text = catch_audio_and_process()
            if user_text:
                chat_with_gpt(user_text)
    except KeyboardInterrupt:
        """ 
        no se por que no funciona eso voy a romper todo
        """
        print("saliendo")
        break
