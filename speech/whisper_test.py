import whisper
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile as wav
import os
import sys
import string
from rapidfuzz import process, fuzz
import pyttsx3
import time

def snap_birds(text, birds, threshold=85):
    words = text.split()
    fixed = []
    i = 0
    best_best = None
    best_score = 0
    
    while i < len(words):
        matched = False
        # Try windows of 3 and 2 words only (no 1-word chunks)
        for window in [3, 2]:
            chunk_words = words[i:i+window]
            if len(chunk_words) < window:
                continue
            # Remove punctuation for better matching
            chunk = " ".join(word.strip(string.punctuation) for word in chunk_words)
            if not chunk:
                continue
            best, score, _ = process.extractOne(chunk, birds, scorer=fuzz.WRatio)
            # print(f"[DEBUG] '{chunk}' matched '{best}' with score {score}")
            if score >= threshold and score > best_score:
                fixed.append(best)  # canonical bird name
                i += window
                matched = True
                best_best = best
                best_score = score
                break  # no need to check smaller window if matched
        if not matched:
            fixed.append(words[i])
            i += 1
    return best_best


def get_user_input(model, duration, playback=False, birds=None, sample_rate=16000):
    print("🎤 Recording... Speak now.")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    print("📦 Recording finished. Transcribing...")
    if playback: sd.play(audio, sample_rate)

    # Save to temporary WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        wav.write(tmpfile.name, sample_rate, audio)
        tmp_path = tmpfile.name

    # Transcribe using Whisper
    result = model.transcribe(tmp_path)
    if birds:
        # Find the best matching bird name
        bird_name = snap_birds(result['text'].lower(), birds, threshold=70)

    # Clean up
    os.remove(tmp_path)

    return result['text'], bird_name if birds else None

def get_bird_name(model, engine, birds):
    bird_recongized = False

    while not bird_recongized:
        text, bird = get_user_input(model, 4, playback=False, birds=birds)
        print("Transcribed text:", text)
        print("Detected bird:", bird)
        if bird:
            bird_recongized = True
            return text, bird
        else:
            engine.say("Sorry, I couldn't identify the bird. Please try again.")
            engine.runAndWait()
            time.sleep(4)

def talk_to_female(model, engine, list_of_birds):
    engine.say("Hello lady! Which is your favorite bird?")
    engine.runAndWait()
    time.sleep(2)
    _, bird = get_bird_name(model, engine, list_of_birds)
    location = "center"
    color = "red"
    engine.say(f"Thank you for letting me know.")
    engine.runAndWait()
    engine.say(f'The {bird} is sitting on a {color} ring in the {location} part of the park.')
    engine.runAndWait()
    time.sleep(2)


def talk_to_male(model, engine, list_of_birds):
    engine.say("Hello sir! Which is your favorite bird?")
    engine.runAndWait()
    time.sleep(2)

    bird_confirmed = False
    _, pending_bird = get_bird_name(model, engine, list_of_birds)

    while not bird_confirmed:
        engine.say(f"Are you sure that it is {pending_bird}?")
        engine.runAndWait()
        time.sleep(1)
        text, bird = get_user_input(model, 4, playback=False, birds=list_of_birds)
        print("Transcribed text:", text)
        print("Detected bird:", bird)
        if "yes" in text.lower():
            bird_confirmed = True
            engine.say(f'Thanks for confirming that it is {pending_bird}  .')
            engine.runAndWait()
            time.sleep(1)
        elif bird == pending_bird:
            bird_confirmed = True
            engine.say(f'Thanks for confirming that it is {pending_bird}  .')
            engine.runAndWait()
            time.sleep(1)
        else:
            pending_bird = bird
            time.sleep(2)


    location = "center"
    color = "red"
    engine.say(f'The {pending_bird} is sitting on a {color} ring in the {location} part of the park  .')
    engine.runAndWait()
    time.sleep(1)

def main():

    model = whisper.load_model("medium.en")
    print("Whisper ASR model loaded.")

    str = "002.Laysan_Albatross 012.Yellow_headed_Blackbird 014.Indigo_Bunting 025.Pelagic_Cormorant 029.American_Crow 033.Yellow_billed_Cuckoo 035.Purple_Finch 042.Vermilion_Flycatcher 048.European_Goldfinch 050.Eared_Grebe 059.California_Gull 068.Ruby_throated_Hummingbird 073.Blue_Jay 081.Pied_Kingfisher 095.Baltimore_Oriole 101.White_Pelican 106.Horned_Puffin 108.White_necked_Raven 112.Great_Grey_Shrike 118.House_Sparrow 134.Cape_Glossy_Starling 138.Tree_Swallow 144.Common_Tern 191.Red_headed_Woodpecker"
    l = str.split(" ")
    l = [i.split(".")[1] for i in l]
    l = [i.replace("_", " ").lower() for i in l]
    list_of_birds = l

    # gender = 'F'

    engine = pyttsx3.init()
    engine.setProperty('rate', 140)         # words per minute
    engine.setProperty('volume', 1)       # 0.0–1.0
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[19].id)

    # Save original stderr fd
    stderr_fileno = sys.stderr.fileno()

    # Open /dev/null for writing
    devnull = os.open(os.devnull, os.O_WRONLY)

    # Duplicate /dev/null fd to stderr fd (2)
    os.dup2(devnull, stderr_fileno)


    talk_to_male(model, engine, list_of_birds)

    # text, bird = get_user_input(model, 4, playback=True, birds=list_of_birds)
    # print("You said: ", text)
    # print("Bird species: ", bird)

    # When done, restore stderr
    os.dup2(stderr_fileno, stderr_fileno)
    os.close(devnull)

if __name__ == "__main__":
    main()