import tkinter as tk
from tkinter import ttk, messagebox
import speech_recognition as sr
from gtts import gTTS
import tempfile
from googletrans import Translator
import threading
import pygame
import os
import time

class SpeechTranslationApp:
    def __init__(self, master):  # Corrected the initialization method name
        self.master = master
        master.title("Speech Translation Assistant")
        master.geometry("750x650")
        master.configure(bg="#f0f4f8")

        self.recognizer = sr.Recognizer()
        self.translator = Translator()

        self.languages = {
            'English': 'en', 'Spanish': 'es', 'French': 'fr', 'German': 'de', 'Italian': 'it',
            'Hindi': 'hi', 'Marathi': 'mr', 'Gujarati': 'gu', 'Tamil': 'ta', 'Telugu': 'te',
            'Kannada': 'kn', 'Malayalam': 'ml', 'Punjabi': 'pa', 'Bengali': 'bn', 'Urdu': 'ur',
            'Chinese': 'zh-cn', 'Japanese': 'ja', 'Russian': 'ru', 'Korean': 'ko', 'Arabic': 'ar'
        }

        # Setup GUI elements
        self.title_label = tk.Label(master, text="Speech Translation Assistant",
                                    font=("Helvetica", 18, "bold"), bg="#f0f4f8", fg="#344955")
        self.title_label.pack(pady=15)

        self.instruction_label = tk.Label(
            master, text="Select a language and click 'Start' to translate your speech.",
            bg="#f0f4f8", fg="#7a869a")
        self.instruction_label.pack(pady=5)

        self.input_frame = tk.Frame(master, bg="#f0f4f8")
        self.input_frame.pack(pady=15)

        self.language_label = tk.Label(self.input_frame, text="Select Language:", bg="#f0f4f8", fg="#344955")
        self.language_label.pack(side=tk.LEFT, padx=5)

        self.language_var = tk.StringVar()
        self.language_dropdown = ttk.Combobox(self.input_frame, textvariable=self.language_var,
                                            font=("Helvetica", 12), state="readonly")
        self.language_dropdown['values'] = list(self.languages.keys())
        self.language_dropdown.pack(side=tk.LEFT, padx=10)
        self.language_dropdown.set("Select Language")

        self.start_button = tk.Button(self.input_frame, text="Start Translation", command=self.start_translation,
                                    bg="#4caf50", fg="white", font=("Helvetica", 12, "bold"))
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.quit_button = tk.Button(self.input_frame, text="Quit", command=master.quit,
                                    bg="#d9534f", fg="white", font=("Helvetica", 12, "bold"))
        self.quit_button.pack(side=tk.LEFT)

        self.output_frame = tk.Frame(master, bg="#f0f4f8")
        self.output_frame.pack(pady=15)

        self.label1 = tk.Label(self.output_frame, text="Recognized Text:", bg="#f0f4f8",
                            font=("Helvetica", 12, "bold"), fg="#344955")
        self.label1.pack()

        self.recognized_text = tk.Text(self.output_frame, height=5, width=70, wrap=tk.WORD,
                                    font=("Helvetica", 12), bg="#e0e0e0")
        self.recognized_text.pack(pady=5)

        self.label2 = tk.Label(self.output_frame, text="Translated Text:", bg="#f0f4f8",
                            font=("Helvetica", 12, "bold"), fg="#344955")
        self.label2.pack()

        self.translated_text = tk.Text(self.output_frame, height=5, width=70, wrap=tk.WORD,
                                    font=("Helvetica", 12), bg="#e0e0e0")
        self.translated_text.pack(pady=5)

        self.status_label = tk.Label(master, text="", bg="#f0f4f8", font=("Helvetica", 10), fg="#7a869a")
        self.status_label.pack(pady=10)

        self.soundwave_label = tk.Label(master, text="", bg="#f0f4f8", fg="#4caf50", font=("Helvetica", 16))
        self.soundwave_label.pack(pady=5)

        # Initialize pygame mixer for audio playback
        try:
            pygame.mixer.init()
        except Exception as e:
            messagebox.showerror("Audio Initialization Error", f"Could not initialize audio: {e}")

    def animate_soundwave(self):
        """Simulate a soundwave animation while translating."""
        wave_texts = ["~ ~ ", " ~ ~ ", " ~ ~ ~ ~"]
        for _ in range(6):  # Run the animation for a few cycles
            for wave in wave_texts:
                self.soundwave_label.config(text=wave)
                self.master.update()
                self.master.after(300)

        self.soundwave_label.config(text="")  # Clear animation after the loop

    def start_translation(self):
        """Start the translation process."""
        target_lang = self.get_selected_language()
        if not target_lang:
            self.status_label.config(text="Please select a target language.", fg="red")
            return

        self.status_label.config(text="Listening...", fg="blue")
        threading.Thread(target=lambda: self.perform_translation(target_lang)).start()

    def get_selected_language(self):
        """Retrieve the selected language code from dropdown."""
        selected_lang = self.language_var.get()
        return self.languages.get(selected_lang)

    def perform_translation(self, target_lang):
        """Translate recognized speech and display results."""
        recognized_text = self.recognize_speech()
        if recognized_text is None:
            self.status_label.config(text="Speech recognition failed.", fg="red")
            return

        self.master.after(0, lambda: self.update_recognized_text(recognized_text))
        self.animate_soundwave()
        translated_text = self.translate_text(recognized_text, target_lang)
        self.master.after(0, lambda: self.update_translated_text(translated_text))
        self.status_label.config(text="Translation Complete.", fg="green")
        self.text_to_speech(translated_text, lang=target_lang)

    def update_recognized_text(self, text):
        self.recognized_text.delete(1.0, tk.END)
        self.recognized_text.insert(tk.END, text)

    def update_translated_text(self, text):
        self.translated_text.delete(1.0, tk.END)
        self.translated_text.insert(tk.END, text)

    def recognize_speech(self):
        """Capture audio and convert to text."""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

            try:
                return self.recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                messagebox.showerror("Speech Error", "Could not understand audio.")
                return None
            except sr.RequestError:
                messagebox.showerror("Network Error", "Check your network connection.")
                return None

    def translate_text(self, text, target_lang):
        """Translate text to the selected language using googletrans."""
        try:
            return self.translator.translate(text, dest=target_lang).text
        except Exception as e:
            return f"Translation Error: {str(e)}"

    def text_to_speech(self, text, lang='en'):
        """Convert translated text to speech and play using pygame."""
        try:
            # Generate the TTS audio and save it to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file_path = temp_file.name
                tts = gTTS(text=text, lang=lang)
                tts.save(temp_file_path)

            # Ensure pygame reinitializes the mixer to properly handle the file
            pygame.mixer.init()
            pygame.mixer.music.load(temp_file_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.1)  # Small delay to prevent high CPU usage

            # Stop and uninitialize the mixer to free the file
            pygame.mixer.music.stop()
            pygame.mixer.quit()

            # Allow some time for resources to be released
            time.sleep(0.2)
        except Exception as e:
            messagebox.showerror("TTS Error", f"An error occurred during TTS: {e}")
        finally:
            if temp_file_path:
                # Attempt to delete the file, ignore any persistent errors
                try:
                    os.remove(temp_file_path)
                except Exception as e:
                    # Log to a file or system log if needed, but do not show another error message
                    print(f"Error cleaning up temporary file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechTranslationApp(root)
    root.mainloop()
