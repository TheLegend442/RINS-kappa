import time
import keyboard   # pip install keyboard

print("→  Hold SPACE to record; press Esc to quit.")

try:
    while True:
        keyboard.wait("space")          # blocks until Space pressed
        print("Recording...")
        # ---- your recording code here ----
        while keyboard.is_pressed("space"):
            time.sleep(0.01)            # keep looping while held
        # ---- stop / process audio here ----
        print("Stopped.")
        if keyboard.is_pressed("esc"):
            break
except KeyboardInterrupt:
    pass