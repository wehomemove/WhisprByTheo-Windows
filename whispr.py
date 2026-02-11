#!/usr/bin/env python3
"""
WhisprByTheo for Windows
Push-to-talk voice transcription using OpenAI Whisper API
"""

import os
import sys
import json
import tempfile
import threading
import time
import wave
import struct
from pathlib import Path

# Check dependencies
try:
    import webview
    import pyaudio
    import keyboard
    import pyperclip
    import requests
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: pip install pywebview pyaudio keyboard pyperclip requests")
    sys.exit(1)

# Config
CONFIG_DIR = Path.home() / ".config" / "whispr"
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_HOTKEY = "f8"

class WhisprApp:
    def __init__(self):
        self.api_key = None
        self.hotkey = DEFAULT_HOTKEY
        self.recording = False
        self.audio_frames = []
        self.pyaudio = None
        self.stream = None
        self.window = None
        self.load_config()

    def load_config(self):
        """Load config from file"""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE) as f:
                    config = json.load(f)
                    self.api_key = config.get("api_key")
                    self.hotkey = config.get("hotkey", DEFAULT_HOTKEY)
            except:
                pass

    def save_config(self):
        """Save config to file"""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump({
                "api_key": self.api_key,
                "hotkey": self.hotkey
            }, f)

    def set_api_key(self, key):
        """Set API key and save"""
        self.api_key = key
        self.save_config()
        return True

    def set_hotkey(self, key):
        """Set hotkey and save"""
        self.hotkey = key
        self.save_config()
        self.register_hotkey()
        return True

    def get_config(self):
        """Get current config for UI"""
        return {
            "api_key_set": bool(self.api_key),
            "hotkey": self.hotkey
        }

    def start_recording(self):
        """Start recording audio"""
        if self.recording:
            return

        self.recording = True
        self.audio_frames = []

        # Update UI
        if self.window:
            self.window.evaluate_js("setState('recording', 'Listening')")

        # Start recording in background
        def record():
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 16000

            self.pyaudio = pyaudio.PyAudio()
            self.stream = self.pyaudio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )

            while self.recording:
                try:
                    data = self.stream.read(CHUNK, exception_on_overflow=False)
                    self.audio_frames.append(data)
                except:
                    break

        self.record_thread = threading.Thread(target=record, daemon=True)
        self.record_thread.start()

    def stop_recording(self):
        """Stop recording and transcribe"""
        if not self.recording:
            return

        self.recording = False
        time.sleep(0.1)  # Let recording thread finish

        # Clean up audio stream
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.pyaudio:
            self.pyaudio.terminate()

        # Update UI
        if self.window:
            self.window.evaluate_js("setState('transcribing', 'Transcribing')")

        # Transcribe in background
        threading.Thread(target=self._transcribe, daemon=True).start()

    def _transcribe(self):
        """Send audio to OpenAI and paste result"""
        if not self.audio_frames:
            self._show_error("No audio")
            return

        if not self.api_key:
            self._show_error("No API key")
            return

        # Save audio to temp file
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        try:
            with wave.open(temp_file.name, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                wf.writeframes(b''.join(self.audio_frames))

            # Call OpenAI API
            with open(temp_file.name, 'rb') as audio_file:
                response = requests.post(
                    "https://api.openai.com/v1/audio/transcriptions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    files={"file": ("audio.wav", audio_file, "audio/wav")},
                    data={"model": "whisper-1"}
                )

            if response.status_code == 200:
                text = response.json().get("text", "").strip()
                if text:
                    # Copy to clipboard and paste
                    pyperclip.copy(text)
                    self._show_success()
                    time.sleep(0.3)
                    keyboard.send("ctrl+v")
                else:
                    self._show_error("No speech")
            else:
                self._show_error("API error")

        except Exception as e:
            self._show_error("Error")
            print(f"Transcription error: {e}")
        finally:
            os.unlink(temp_file.name)

    def _show_success(self):
        """Show success state"""
        if self.window:
            self.window.evaluate_js("setState('success', 'Done')")
            time.sleep(1)
            self.window.evaluate_js("setState('idle', '')")

    def _show_error(self, msg):
        """Show error state"""
        if self.window:
            self.window.evaluate_js(f"setState('error', '{msg}')")
            time.sleep(1.5)
            self.window.evaluate_js("setState('idle', '')")

    def register_hotkey(self):
        """Register the global hotkey"""
        keyboard.unhook_all()
        keyboard.on_press_key(self.hotkey, lambda _: self.start_recording())
        keyboard.on_release_key(self.hotkey, lambda _: self.stop_recording())

    def run(self):
        """Start the app"""
        # Register hotkey
        self.register_hotkey()

        # Create window
        html_path = Path(__file__).parent / "ui.html"
        self.window = webview.create_window(
            "WhisprByTheo",
            str(html_path),
            width=220,
            height=140,
            resizable=False,
            frameless=True,
            on_top=True,
            transparent=True,
            js_api=self
        )

        webview.start()


# Entry point for packaged app
def main():
    app = WhisprApp()

    # Check for API key on first run
    if not app.api_key:
        import tkinter as tk
        from tkinter import simpledialog

        root = tk.Tk()
        root.withdraw()

        key = simpledialog.askstring(
            "WhisprByTheo Setup",
            "Enter your OpenAI API key:\n\n(Get one at platform.openai.com/api-keys)",
            parent=root
        )

        if key:
            app.set_api_key(key.strip())
        else:
            print("API key required")
            sys.exit(1)

        root.destroy()

    app.run()


if __name__ == "__main__":
    main()
