from vosk import Model, KaldiRecognizer
import json
import os

import speech_recognition as sr
from playsound import playsound


import pyaudio

PLING_MP3 = os.path.join(os.path.dirname(__file__), '../../resources/pling.mp3')


class SttSuper:
    def prepare_listen(self):
        pass

    def listen_and_recognize(self):
        pass

    @staticmethod
    def create_recognizer(recog_type):
        recognizer: SttSuper = None
        if recog_type == "vosk":
            recognizer = SttVosk()
        elif recognizer == "google":
            recognizer = SttGoogle()
        return recognizer

    @staticmethod
    def _play_init():
        try:
            playsound(PLING_MP3)
        except ModuleNotFoundError:
            # arch has a problem with python-gobject, using mpg123 as fallback
            os.system(f"mpg123 {os.path.dirname(__file__)}/../resources/pling.mp3 >/dev/null 2>&1")


class SttVosk(SttSuper):
    def __init__(self):
        if not os.path.exists("model"):
            print("Please download the model from "
                  "https://github.com/alphacep/vosk-api/blob/master/doc/models.md"
                  " and unpack as 'model' in the current folder.")
            exit(1)
        self.model = Model("model")

        self.recognizer = KaldiRecognizer(self.model, 16000)

    def listen_and_recognize(self):
        retval = None

        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        stream.start_stream()

        self._play_init()
        print("Speak:")

        while retval is None:

            input = stream.read(4000)
            if self.recognizer.AcceptWaveform(input):
                print("recognition finished")
                vosk_result = self.recognizer.Result()

                dict_result = json.loads(vosk_result)

                retval = dict_result["text"]
        return retval


class SttGoogle(SttSuper):
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen_and_recognize(self):
        result = ""
        with self.recognizer.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, 0.5)
            self._play_init()
            print("Speak:")
            audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=4)

        try:
            result = self.recognizer.recognize_google(audio)

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        return result
