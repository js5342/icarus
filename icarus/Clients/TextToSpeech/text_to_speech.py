import pyttsx3

from gtts import gTTS
import os
import platform
from playsound import playsound


class TtsSuper:
    def tts(self, message: str):
        pass

    @staticmethod
    def create_tts(tts_type):
        tts: TtsSuper = None
        if tts_type == "pyttsx3":
            tts = TtsPyttsx3()
        elif tts_type == "google":
            tts = TtsGoogle()
        return tts


class TtsPyttsx3(TtsSuper):
    def __init__(self):
        self.engine = pyttsx3.init()

    def tts(self, message: str):
        self.engine.say(message)
        # engine.setProperty('rate', 120)
        # engine.setProperty('volume', 0.9)
        self.engine.runAndWait()


class TtsGoogle(TtsSuper):
    def tts(self, message: str):
        tts = gTTS(text=message, lang='en')
        tts.save(f"{os.path.dirname(__file__)}/../resources/tts_message.mp3")

        if platform.system().lower() == 'windows':
            playsound(f"{os.path.dirname(__file__)}/../resources/tts_message.mp3")
        else:
            os.system(f"mpg123 {os.path.dirname(__file__)}/../../resources/tts_message.mp3")  # >/dev/null 2>&1")
        if os.path.isfile(f"{os.path.dirname(__file__)}/../../resources/tts_message.mp3"):
            os.remove(f"{os.path.dirname(__file__)}/../../resources/tts_message.mp3")
