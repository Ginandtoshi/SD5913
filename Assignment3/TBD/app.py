"""
Author: Jinying(Helen) Xie
Date: October 2025

Real-time transcription of audio input with about 5 seconds of delay.

Dependencies:
  pip install faster-whisper[gpu] sounddevice numpy torch

Notes:
  - This script uses Faster-Whisper for transcription and sounddevice for capturing audio.
  - It is configured to run on a CUDA-enabled GPU.
  - It uses a smaller, English-only model for better real-time performance.
"""
import torch
from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np
import queue
import threading
import time

# --- Configuration ---
# Using a smaller, English-specific model for better performance.
# Other options: 'tiny.en', 'base.en', 'small.en', 'medium.en'
MODEL_SIZE = "base.en"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
SAMPLE_RATE = 16000  # Whisper models are trained on 16kHz audio.
CHUNK_SECONDS = 5    # Process audio in 5-second chunks.
BLOCK_SIZE = int(SAMPLE_RATE * CHUNK_SECONDS)

# --- Global Queue for Audio Chunks ---
audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, flush=True)
    audio_queue.put(indata.copy())

def transcription_worker():
    """A worker thread that transcribes audio from the queue."""
    print(f"Loading Whisper model '{MODEL_SIZE}' on device '{DEVICE}'...")
    # Use float16 for GPU, float32 for CPU
    compute_type = "float16" if DEVICE == "cuda" else "float32"
    model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=compute_type)
    print("Model loaded. Transcription is active.")
    
    while True:
        try:
            audio_chunk = audio_queue.get(timeout=1)
            
            # Convert to a flat float32 array
            audio_np = np.squeeze(audio_chunk).astype(np.float32)
            
            # Transcribe the audio chunk
            segments, _ = model.transcribe(audio_np, language="en", beam_size=5)
            
            transcription = "".join(segment.text for segment in segments).strip()
            if transcription:
                print(f"🗣️ {transcription}")

        except queue.Empty:
            # No audio in the queue, just continue
            continue
        except Exception as e:
            print(f"An error occurred during transcription: {e}")
            break

def main():
    """Main function to start the audio stream and transcription worker."""
    if DEVICE == "cpu":
        print("Warning: CUDA (GPU) not available. Running on CPU, which will be much slower.")

    # Start the transcription worker thread
    worker = threading.Thread(target=transcription_worker, daemon=True)
    worker.start()

    # Start the audio stream from the microphone
    try:
        with sd.InputStream(samplerate=SAMPLE_RATE, 
                             blocksize=BLOCK_SIZE, 
                             device=None, # Default input device
                             channels=1, 
                             dtype='float32',
                             callback=audio_callback):
            print("\n🎙️  Listening... Press Ctrl+C to stop.")
            while worker.is_alive():
                time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n🛑 Stopping...")
    except Exception as e:
        print(f"An error occurred with the audio stream: {e}")

if __name__ == "__main__":
    main()
