from pynput import keyboard
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import whisper
import threading

model = whisper.load_model("small")

recording = False
frames = []
lock = threading.Lock()

def audio_callback(indata, frames_count, time, status):
    global recording
    with lock:
        if recording:
            frames.append(indata.copy())

def on_press(key):
    global recording, frames

    if key == keyboard.Key.space and not recording:
        print("⏺️  Recording… hold Space")
        with lock:
            recording = True
            frames = []

def on_release(key):
    global recording

    if key == keyboard.Key.space and recording:
        with lock:
            recording = False
        print("⏹️  Stopped recording, processing...")
        # Save recording to file
        audio = np.concatenate(frames, axis=0)
        write("temp.wav", 16000, audio)
        # Transcribe
        result = model.transcribe("temp.wav", language="en")
        print("📝 Transcription:", result["text"])

    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Start audio input stream
stream = sd.InputStream(samplerate=16000, channels=1, callback=audio_callback)
stream.start()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

stream.stop()
stream.close()
print("🛑 Exiting...")