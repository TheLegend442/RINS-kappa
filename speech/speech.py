import json, queue, sys, time
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from rapidfuzz import process, fuzz

def snap_birds(text, birds, threshold=85):
    """
    Find substrings in `text` that closely match any bird name in `birds`
    and replace them with the canonical spelling.
    """
    words = text.split()            # coarse tokenisation
    fixed = []
    i = 0
    best_best = ""
    best_score = 0
    while i < len(words):
        # try to match up to 3‑word windows (adjust as needed)
        matched = False
        for window in range(3, 0, -1):
            chunk = " ".join(words[i:i+window])
            if not chunk:
                continue
            best, score, _ = process.extractOne(
                chunk,
                birds,
                scorer=fuzz.WRatio
            )
            if score >= threshold and score > best_score:
                fixed.append(best)  # canonical bird name
                i += window
                matched = True
                best_best = best
                best_score = score
                break
        if not matched:
            fixed.append(words[i])
            i += 1
    return best_best




str = "002.Laysan_Albatross 012.Yellow_headed_Blackbird 014.Indigo_Bunting 025.Pelagic_Cormorant 029.American_Crow 033.Yellow_billed_Cuckoo 035.Purple_Finch 042.Vermilion_Flycatcher 048.European_Goldfinch 050.Eared_Grebe 059.California_Gull 068.Ruby_throated_Hummingbird 073.Blue_Jay 081.Pied_Kingfisher 095.Baltimore_Oriole 101.White_Pelican 106.Horned_Puffin 108.White_necked_Raven 112.Great_Grey_Shrike 118.House_Sparrow 134.Cape_Glossy_Starling 138.Tree_Swallow 144.Common_Tern 191.Red_headed_Woodpecker"
l = str.split(" ")
l = [i.split(".")[1] for i in l]
l = [i.replace("_", " ").lower() for i in l]
list_of_birds = list(set(l))  # remove duplicates


MODEL_PATH = "models/vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000  # model sample rate

# 1. Load model
model = Model(MODEL_PATH)

# 2. Build phrase-bias JSON (not a hard grammar)    
rec = KaldiRecognizer(model, SAMPLE_RATE, json.dumps(list_of_birds))

# 4. Audio callback
q = queue.Queue()
def callback(indata, frames, time_, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# 5. Start stream + recognizer loop
print("🎤  Speak; Ctrl-C to stop.")
with sd.RawInputStream(samplerate=SAMPLE_RATE,
                       blocksize=8000,
                       dtype="int16",
                       channels=1,
                       callback=callback):

    partial_printed = ""
    try:
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    fixed = snap_birds(text.lower())
                    print(f"\n✅  {fixed}")
                    partial_printed = ""
            else:
                # show partials in same line
                partial = json.loads(rec.PartialResult()).get("partial", "")
                if partial and partial != partial_printed:
                    sys.stdout.write("\r… " + partial + "   ")
                    sys.stdout.flush()
                    partial_printed = partial
    except KeyboardInterrupt:
        print("\nStopped.")