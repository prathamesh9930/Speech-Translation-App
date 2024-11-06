# Speech Translation Assistant

A Python application that allows users to convert speech to text and translate it into different languages. The app uses `speech_recognition` to capture speech, `googletrans` for translation, and `gTTS` to convert translated text to speech.

## Features
- Speech recognition from the microphone.
- Translation of recognized text into selected languages.
- Text-to-speech (TTS) for the translated text.
- Visual feedback with sound wave animation during translation.
- User-friendly graphical interface using `tkinter`.

## Requirements

Before running the app, you need to install the following dependencies:

1. `speech_recognition` - For speech-to-text functionality.
2. `gTTS` (Google Text-to-Speech) - To convert translated text to speech.
3. `googletrans` - To perform translations.
4. `pygame` - For audio playback.
5. `tkinter` - For the graphical user interface.

### Install dependencies

You can install the required dependencies by running the following commands in your terminal:

```bash
pip install SpeechRecognition
pip install gTTS
pip install googletrans==4.0.0-rc1  # Version may vary; check compatibility
pip install pygame
pip install tk
