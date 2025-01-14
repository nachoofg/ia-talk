""" 
Este es un archivo de implementacion para detectar audio de una mejor forma,
este sistema deberia de guardar lo que se diga en un archivo de audio y luego
procesar ese archivo para que la vtuber pueda hablar

Este metodo se termino descartando porque genera un delay que no es bueno y se puede
hacer mas eficiente con una libreria de deteccion de voz al momento
"""

import pyaudio
import keyboard
import wave
import openai

def catchaudio():
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
    print("escuchando...")
    while keyboard.is_pressed("RIGHT_SHIFT"):
        data = stream.read(CHUNK)
        frames.append(data)
    print("termine de esuchar...")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
while True:
    try:
        print("apreta shift derecho")
        while True:
            if keyboard.is_pressed('RIGHT_SHIFT'):
                catchaudio()
    except KeyboardInterrupt:
        print("saliendo...")
        break