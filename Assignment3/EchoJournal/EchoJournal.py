"""
Author: Jinying(Helen) Xie
Date: October 2025

Echo Journal - A Pygame GUI for real-time transcription and visualization.

Required Packages & Libraries:
    pip install faster-whisper[gpu] sounddevice numpy torch
    python -m textblob.download_corpora

This application captures audio from the microphone, transcribes it in real-time using
Faster-Whisper, and displays the text in a Pygame window. As more text is generated,
a visual representation of a person (the circle) gets "lighter," symbolizing emotional release.
"""
import torch
from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np
import queue
import threading
import time
import pygame
import random
from collections import deque
from nrclex import NRCLex

# --- Configuration ---
# Models: 'tiny.en', 'base.en', 'small.en', 'medium.en'
MODEL_SIZE = "base.en"
DEVICE = "cpu" # Forcing CPU as per user request for stability
COMPUTE_TYPE = "float32" # CPU requires float32

SAMPLE_RATE = 16000
CHUNK_SECONDS = 3
BLOCK_SIZE = int(SAMPLE_RATE * CHUNK_SECONDS)
TARGET_CHARS_FOR_RELEASE = 500  # Increased for a more gradual change

# --- Pygame Window Settings ---
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
BACKGROUND_COLOR = (255, 255, 255)  # White background
TEXT_COLOR = (0, 0, 0)          # Black text
BUTTON_COLOR = (220, 220, 220)
BUTTON_TEXT_COLOR = (0, 0, 0)

# --- Emotion Color Mapping ---
EMOTION_COLORS = {
    "fear": (100, 149, 237),      # Medium Blue
    "anger": (220, 20, 60),        # Crimson Red
    "sadness": (119, 136, 153),    # Slate Gray
    "disgust": (107, 142, 35),     # Olive Drab
    "joy": (255, 165, 0),        # Orange
    "surprise": (255, 215, 0),     # Gold
    "trust": (255, 182, 193),      # Light Pink
    "anticipation": (144, 238, 144), # Light Green
    "positive": (60, 179, 113),    # Medium Sea Green
    "negative": (169, 169, 169),    # Dark Gray
}
DEFAULT_TEXT_COLOR = (0, 0, 0)

# --- Queues for Inter-thread Communication ---
audio_queue = queue.Queue()
text_queue = queue.Queue()
model_loaded = threading.Event() # Used to signal that the model is ready

# --- Transcription Worker ---
def transcription_worker():
    """A worker thread that transcribes audio and passes text to the GUI."""
    print(f"Loading Whisper model '{MODEL_SIZE}' on device '{DEVICE}'...")
    try:
        model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
        print("Model loaded. Transcription is active.")
        model_loaded.set() # Signal that the model is ready
    except Exception as e:
        print(f"Error loading model: {e}")
        model_loaded.set() # Also signal on error to not block the main thread
        return

    while True:
        try:
            audio_chunk = audio_queue.get()
            if audio_chunk is None: # Sentinel value to stop the thread
                break
            
            audio_np = np.squeeze(audio_chunk).astype(np.float32)
            segments, _ = model.transcribe(audio_np, language="en", beam_size=5)
            
            transcription = "".join(segment.text for segment in segments).strip()
            if transcription:
                text_queue.put(transcription) # Send text to the GUI thread
        except Exception as e:
            print(f"An error occurred during transcription: {e}")
            break

# --- Audio Input ---
def audio_callback(indata, frames, time, status):
    """Captures audio and puts it into a queue."""
    if status:
        print(status, flush=True)
    audio_queue.put(indata.copy())

# --- Pygame Helper Functions ---
def draw_person(surface, lightness_level):
    """Draws the person figure. lightness_level is 0.0 (black) to 1.0 (white)."""
    color_val = int(255 * lightness_level)
    person_color = (color_val, color_val, color_val)
    
    center_x = surface.get_width() // 2
    center_y = surface.get_height() // 2
    
    # Head
    pygame.draw.circle(surface, person_color, (center_x, center_y - 50), 30)

def draw_text_in_columns(surface, word_color_chunks, font):
    """Draws text word-by-word in two columns, with colors."""
    margin = 40
    person_area_width = 250
    col_width = (surface.get_width() - person_area_width - 2 * margin) // 2
    
    left_col_x = margin
    right_col_x = surface.get_width() - margin - col_width
    
    col_y = margin
    current_col_x = left_col_x
    
    screen_full = False
    space_width = font.size(' ')[0]

    # Start with a fresh line position for the first chunk
    current_line_x = current_col_x

    for chunk in word_color_chunks:
        for i, (word, color) in enumerate(chunk):
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()

            # Check for line break before drawing the word
            if current_line_x + word_width > current_col_x + col_width:
                col_y += word_height
                current_line_x = current_col_x

                # Check for column break
                if col_y + word_height > surface.get_height() - margin:
                    if current_col_x == left_col_x:
                        current_col_x = right_col_x
                        col_y = margin
                        current_line_x = current_col_x
                    else:
                        screen_full = True
                        break
            
            surface.blit(word_surface, (current_line_x, col_y))
            current_line_x += word_width + space_width
        
        if screen_full:
            break
        
        # After a chunk, move to the next line
        col_y += font.get_height()
        current_line_x = current_col_x # Reset x position for the new line
        if col_y + font.get_height() > surface.get_height() - margin:
            if current_col_x == left_col_x:
                current_col_x = right_col_x
                col_y = margin
            else:
                screen_full = True
                break

    return screen_full

def draw_onboarding(surface, font_name):
    """Draws the initial 'Press to Start' screen."""
    surface.fill(BACKGROUND_COLOR)
    try:
        title_font = pygame.font.SysFont(font_name, 74)
        subtitle_font = pygame.font.SysFont(font_name, 36)
    except:
        title_font = pygame.font.Font(None, 74)
        subtitle_font = pygame.font.Font(None, 36)

    title_text = title_font.render("Echo Journal", True, TEXT_COLOR)
    subtitle_text = subtitle_font.render("Press any key to start", True, (100, 100, 100))
    
    title_rect = title_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 50))
    subtitle_rect = subtitle_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 20))
    
    surface.blit(title_text, title_rect)
    surface.blit(subtitle_text, subtitle_rect)

def draw_loading(surface, font_name):
    """Draws the 'Loading...' screen."""
    surface.fill(BACKGROUND_COLOR)
    try:
        loading_font = pygame.font.SysFont(font_name, 50)
    except:
        loading_font = pygame.font.Font(None, 50)
    text = loading_font.render("Loading model, please wait...", True, TEXT_COLOR)
    text_rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(text, text_rect)

def draw_button(surface, rect, text, font):
    """Draws a button with text."""
    pygame.draw.rect(surface, BUTTON_COLOR, rect, border_radius=8)
    text_surf = font.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

# --- Main GUI Application ---
def main():
    # Application state
    app_state = "ONBOARDING" # ONBOARDING, LOADING, RUNNING, FINISHED
    
    # Start the transcription worker thread
    worker = threading.Thread(target=transcription_worker, daemon=True)
    worker.start()

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Echo Journal")

    # --- FONT SETUP ---
    try:
        font_name = 'VCR OSD Mono'
        pixel_font = pygame.font.SysFont(font_name, 30)
    except:
        print("VCR OSD Mono font not found. Using default monospace font.")
        font_name = 'monospace'
        pixel_font = pygame.font.SysFont(font_name, 24)

    # --- Button Setup ---
    button_font = pygame.font.SysFont(font_name, 24)
    stop_button_rect = pygame.Rect(WINDOW_WIDTH - 270, WINDOW_HEIGHT - 60, 250, 40)
    save_button_rect = pygame.Rect(WINDOW_WIDTH - 270, WINDOW_HEIGHT - 60, 250, 40)
    resume_button_rect = pygame.Rect(WINDOW_WIDTH - 460, WINDOW_HEIGHT - 60, 170, 40)

    word_color_chunks = []
    total_chars = 0
    running = True
    stream_active = False

    # Main GUI loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if app_state == "ONBOARDING" and event.type == pygame.KEYDOWN:
                app_state = "LOADING"
            if event.type == pygame.MOUSEBUTTONDOWN:
                # --- Button Click Handling ---
                if app_state == "RUNNING" and stop_button_rect.collidepoint(event.pos):
                    app_state = "FINISHED"
                    if stream_active: stream.stop()
                    print("Recording paused by user.")
                
                elif app_state == "FINISHED":
                    if save_button_rect.collidepoint(event.pos):
                        timestamp = time.strftime("%Y%m%d_%H%M%S")
                        filename = f"EchoJournal_{timestamp}.png"
                        pygame.image.save(screen, filename)
                        print(f"Screenshot saved as {filename}")
                    
                    elif resume_button_rect.collidepoint(event.pos):
                        app_state = "RUNNING"
                        if stream_active: stream.start()
                        print("Recording resumed.")
        
        screen.fill(BACKGROUND_COLOR)

        # --- State Machine for Drawing ---
        if app_state == "ONBOARDING":
            draw_onboarding(screen, font_name)
        
        elif app_state == "LOADING":
            draw_loading(screen, font_name)
            if model_loaded.is_set():
                # Model is ready, start the audio stream
                try:
                    stream = sd.InputStream(
                        samplerate=SAMPLE_RATE, 
                        blocksize=BLOCK_SIZE, 
                        channels=1, 
                        dtype='float32',
                        callback=audio_callback
                    )
                    stream.start()
                    stream_active = True
                    print("\n🎙️  Listening... Close the Pygame window to stop.")
                    app_state = "RUNNING"
                except Exception as e:
                    print(f"Fatal error starting audio stream: {e}")
                    running = False
        
        if app_state in ["RUNNING", "FINISHED"]:
            if app_state == "RUNNING":
                try:
                    new_text = text_queue.get_nowait()
                    total_chars += len(new_text)
                    
                    # --- Emotion Analysis ---
                    emotion_analysis = NRCLex(new_text)
                    words = new_text.split()
                    new_chunk = []
                    for word in words:
                        # Find the most prominent emotion for the word
                        # Make word lowercase for better matching in lexicon
                        affect_list = emotion_analysis.affect_dict.get(word.lower(), [])
                        color = DEFAULT_TEXT_COLOR
                        if affect_list:
                            # Prioritize specific emotions over general positive/negative
                            primary_emotion = affect_list[0]
                            if primary_emotion in EMOTION_COLORS:
                                color = EMOTION_COLORS[primary_emotion]
                        new_chunk.append((word, color))
                    
                    if new_chunk:
                        word_color_chunks.append(new_chunk)

                except queue.Empty:
                    pass

            # --- Drawing ---
            # Calculate lightness level (0.0 is black, 1.0 is white)
            lightness_level = min(1.0, total_chars / TARGET_CHARS_FOR_RELEASE)
            draw_person(screen, lightness_level)

            # Draw text and check if screen is full
            screen_is_full = draw_text_in_columns(screen, word_color_chunks, pixel_font)

            if screen_is_full and app_state == "RUNNING":
                app_state = "FINISHED"
                if stream_active: stream.stop()
                print("Screen is full. Recording paused.")

            # Draw UI elements based on state
            if app_state == "RUNNING":
                # Draw "Recording in progress" indicator
                rec_font = pygame.font.SysFont(font_name, 24)
                rec_text = rec_font.render("Recording in progress", True, (200, 0, 0))
                screen.blit(rec_text, (20, WINDOW_HEIGHT - 40))
                # Draw Pause Button
                draw_button(screen, stop_button_rect, "Pause Recording", button_font)
            
            elif app_state == "FINISHED":
                # Draw Save Screenshot and Resume Buttons
                draw_button(screen, save_button_rect, "Save Screenshot", button_font)
                if not screen_is_full:
                    draw_button(screen, resume_button_rect, "Resume", button_font)

        pygame.display.flip()
        pygame.time.wait(10)

    # --- Cleanup ---
    print("\n🛑 Stopping...")
    if 'stream' in locals() and stream_active:
        stream.stop()
        stream.close()
    audio_queue.put(None)
    worker.join()
    pygame.quit()

if __name__ == "__main__":
    main()
