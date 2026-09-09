import sounddevice as sd
import numpy as np
import threading
import time
import pyperclip
import sys
import os
from faster_whisper import WhisperModel
from llama_cpp import Llama
import keyboard
import traceback

# 1. Global Variables
is_holding = False
is_processing = False
audio_chunks = []
active_stream = None 

# --- Find the exact folder where the .exe is installed ---
if getattr(sys, 'frozen', False):
    APP_FOLDER = os.path.dirname(sys.executable)
else:
    APP_FOLDER = os.path.dirname(os.path.abspath(__file__))

print("Initializing local AI brains...")
sys.stdout.flush() 

# Load Whisper (The Stenographer)
print("Loading Whisper...")
sys.stdout.flush()
whisper_model = WhisperModel("base", device="cpu", compute_type="int8")

# Load Llama (The Editor)
model_path = os.path.join(APP_FOLDER, "llama-3.2-1b-instruct-q4_k_m.gguf")
print(f"Looking for AI brain at: {model_path}")
sys.stdout.flush()

if not os.path.exists(model_path):
    print(f"!!! FATAL ERROR: Could not find the AI brain file (.gguf) in {APP_FOLDER} !!!")
    input("Press Enter to exit...") 
    sys.exit()

print("Loading Llama...")
sys.stdout.flush()
llama_model = Llama(
    model_path=model_path, 
    n_ctx=512,      
    n_threads=4,    
    verbose=False   
)
print("✅ Agent is ready and listening in the background!")
sys.stdout.flush()

# 2. The Audio Catcher
def audio_callback(indata, frames, time, status):
    if is_holding:
        audio_chunks.append(indata.copy())

# 3. The Line Cook's job
def process_voice():
    global is_processing
    try:
        # Safety net: If no audio was recorded, abort safely.
        if not audio_chunks:
            print("   -> (No audio captured, skipping)")
            is_processing = False
            return

        full_audio = np.concatenate(audio_chunks, axis=0)
        
        if len(full_audio) < 8000: 
            print("   -> (Tap too short, ignoring)")
            is_processing = False
            return

        segments, _ = whisper_model.transcribe(full_audio.flatten(), beam_size=5)
        raw_text = " ".join([seg.text for seg in segments])
        print(f"   -> Raw: {raw_text}")
        sys.stdout.flush()

        if raw_text.strip(): 
            output = llama_model.create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are a text formatting tool. You only output the corrected text. Never add conversational filler."},
                    {"role": "user", "content": f"Fix this: {raw_text}"}
                ],
                max_tokens=100,
                temperature=0.1, 
                # THE FIX: Aggressively cut off the AI if it starts being chatty or refusing
                stop=["<|eot_id|>", "<|end_of_text|>", "\n\n", "Here is the", "I cannot", "Sure,", "Certainly"] 
            )
            
            clean_text = output['choices'][0]['message']['content'].strip()
            
            # Clean up any leftover punctuation from the cut-off text
            if clean_text.endswith(":"):
                clean_text = clean_text[:-1]
                
            print(f"   -> Clean: {clean_text}")
            print("   -> Pasting in 1.5 seconds... CLICK NOTEPAD NOW!")
            sys.stdout.flush()
            
            time.sleep(1.5) 
            
            pyperclip.copy(clean_text)
            time.sleep(0.2) 
            keyboard.press_and_release('ctrl+v') 
            print("   -> Done!")
            sys.stdout.flush()
            
    except Exception as e:
        print(f"\n!!! ERROR: {e}\n")
        traceback.print_exc()
        sys.stdout.flush()
    finally:
        is_processing = False

# 4. The Manager's logic
def on_key_press(_):
    global is_holding, is_processing, audio_chunks, active_stream
    if not is_processing and not is_holding:
        is_holding = True
        audio_chunks = [] 
        
        active_stream = sd.InputStream(samplerate=16000, channels=1, dtype='float32', callback=audio_callback)
        active_stream.start()

def on_key_release(_):
    global is_holding, active_stream
    if is_holding:
        is_holding = False
        if active_stream: 
            active_stream.stop()
            active_stream.close()
        threading.Thread(target=process_voice).start()

# 5. Main Loop
print("\nHOLD 'F8' to speak. Release to process.")
print("Waiting for hotkey...")
sys.stdout.flush()

keyboard.on_press_key('f8', on_key_press)
keyboard.on_release_key('f8', on_key_release)

# Keep the app alive
try:
    while True:
        time.sleep(1)
except Exception as e:
    print(f"\n\n!!! CRITICAL ERROR: {e}\n")
    traceback.print_exc()
    sys.stdout.flush()
    input("\nPress Enter to exit...") 