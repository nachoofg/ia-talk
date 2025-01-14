"""
me rendi con esto porque no me funcionan las traducciones
ni chatgpt pudo resolver esto
"""
import requests
import json
import sys
import asyncio
from googletrans import Translator

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

async def translate_google(text, source, target):
    """
    Traduce el texto utilizando Google Translate de forma asincrónica.
    """
    try:
        translator = Translator()
        result = await asyncio.to_thread(translator.translate, text, src=source, dest=target)
        return result.text
    except Exception as e:
        print(f"Error en la traducción con Google Translate: {e}")
        return None

async def detect_google(text):
    """
    Detecta el idioma de un texto utilizando Google Translate de forma asincrónica.
    """
    try:
        translator = Translator()
        result = await asyncio.to_thread(translator.detect, text)
        return result.lang.upper()
    except Exception as e:
        print(f"Error en la detección de idioma con Google Translate: {e}")
        return None

def translate_deeplx(text, source, target):
    """
    Traduce el texto utilizando un servidor DeepLx local.
    """
    url = "http://localhost:1188/translate"
    headers = {"Content-Type": "application/json"}

    params = {
        "text": text,
        "source_lang": source,
        "target_lang": target
    }

    try:
        payload = json.dumps(params)
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status() 
        data = response.json()
        translated_text = data.get('data', None)
        if translated_text:
            return translated_text
        else:
            print("Error en la respuesta de DeepLx:", data)
            return None
    except requests.RequestException as e:
        print(f"Error al conectarse a DeepLx: {e}")
        return None
