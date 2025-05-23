#!/usr/bin/env python3

from task_2s.srv import SpeechService
# from task_2s.msg import Bird
import rclpy
from rclpy.node import Node

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
    birds = list(birds.keys())
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
            print(f"List of birds in the park: {birds}")
            engine.runAndWait()
            time.sleep(4)

def talk_to_female(model, engine, list_of_birds):
    engine.say("Hello lady! Which is your favorite bird?")
    engine.runAndWait()
    time.sleep(2)
    _, bird = get_bird_name(model, engine, list_of_birds)
    location = list_of_birds[bird].location
    color = list_of_birds[bird].ring_color
    engine.say(f"Thank you for letting me know.")
    engine.runAndWait()
    engine.say(f'The {bird} is sitting on a {color} ring in the {location} part of the park.')
    engine.runAndWait()
    time.sleep(2)

    return bird


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
        elif bird != None:
            pending_bird = bird
            time.sleep(2)


    location = list_of_birds[pending_bird].location
    color = list_of_birds[pending_bird].ring_color
    engine.say(f'The {pending_bird} is sitting on a {color} ring in the {location} part of the park  .')
    engine.runAndWait()
    time.sleep(1)

    return pending_bird


class Bird():
    def __init__(self, species, image, location, ring_color, detection_time, description):
        self.species = species
        self.image = image
        self.location = location
        self.ring_color = ring_color
        self.detection_time = detection_time
        self.description = description

class SpeechServer(Node):
    def __init__(self):
        super().__init__('speech_server')
        self.srv = self.create_service(SpeechService, 'speech_service', self.speech_callback)
        self.model = whisper.load_model("medium.en")
        self.birds = {}

        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 140)         # words per minute
        self.engine.setProperty('volume', 1)       # 0.0–1.0
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[19].id)

        self.get_logger().info("Speech server ready to receive requests.")

    def speech_callback(self, request, response):
        self.get_logger().info("\nReceived request to talk to the person in front of me.\n")

        for bird in request.birds:

            bird_species = bird.species
            if "." in bird_species:
                bird_species = bird_species.split(".")[1]
            bird_species = bird_species.replace("_", " ")
            bird_species = bird_species.lower()

            bird_obj = Bird(
                species=bird_species,
                image=None,
                location=bird.location,
                ring_color=bird.ring_color,
                detection_time=bird.detection_time,
                description=None
            )

            self.birds[bird_species] = bird_obj

        gender = request.gender

        ## HIDE C ERROR MESSAGES - REDIRECT STDERR TO /dev/null
        # Save original stderr fd
        stderr_fileno = sys.stderr.fileno()

        # Open /dev/null for writing
        devnull = os.open(os.devnull, os.O_WRONLY)

        # Duplicate /dev/null fd to stderr fd (2)
        os.dup2(devnull, stderr_fileno)

        fav_bird = None
        if gender == "M":
            fav_bird = talk_to_male(self.model, self.engine, self.birds)
        elif gender == "F":
            fav_bird = talk_to_female(self.model, self.engine, self.birds)
        else:
            self.get_logger(f"Gender {gender} not supported.").error

        # When done, restore stderr
        os.dup2(stderr_fileno, stderr_fileno)
        os.close(devnull)

        # Prepare the response
        response.favourite_bird = fav_bird
        return response


def main(args=None):
    rclpy.init(args=args)
    node = SpeechServer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()