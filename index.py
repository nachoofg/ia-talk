import speech_recognition as sr
import pyttsx3
from openai import OpenAI
from dotenv import load_dotenv
import os
import sys

load_dotenv()

api_key = os.getenv('tok')
client = OpenAI(api_key=api_key)

context = {"role": "system", "content": "idk"}
messages = [context]

recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150) 
engine.setProperty('volume', 1.0) 

while True:
    try:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.5)
            print("escucho...")
            audio = recognizer.listen(mic)

            text = recognizer.recognize_google(audio, language='es-es')
            text = text.lower()

            if text.startswith("system call"):
                text = str(text.lower()).split(" ")
                text.remove("system")
                text.remove("call")
                text = " ".join(text)
                print(text)
                os.system(text)
                sys.exit()
            
            print(f"Tú: {text}")
            messages.append({"role": "user", "content": text})

            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=messages,
                max_tokens=100,
                temperature=0.7,
            )
            response_content = response.choices[0].message.content
            messages.append({"role": "assistant", "content": response_content})

            print(f"AI: {response_content}")

            engine.say(response_content)
            engine.runAndWait() 

    except sr.UnknownValueError:
        print("no entendi nada ura")
    except sr.RequestError as e:
        print(f"err con servicio de reconocimiento: {e}")
    except Exception as e:
        print(f"err: {e}")
        continue