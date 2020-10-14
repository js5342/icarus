from vosk import Model, KaldiRecognizer
import json
import os

import pyaudio

class VoskRecognizer:
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

        while retval is None:

            input = stream.read(4000)
            if self.recognizer.AcceptWaveform(input):
                print("recognition finished")
                vosk_result = self.recognizer.Result()

                dict_result = json.loads(vosk_result)

                retval = dict_result["text"]
        return retval
