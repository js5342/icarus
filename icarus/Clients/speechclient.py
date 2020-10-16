from icarus.Clients.superclient import SuperClient
import platform
from icarus.logging import icarus_logger

from icarus.Clients.SpeechToText.speech_to_text import SttSuper
from icarus.Clients.TextToSpeech.text_to_speech import TtsSuper

try:
    from icarus.Clients.WakeWordEngines.porcupine import Porcupine
except OSError:
    icarus_logger.warning('Tried using porcupine with windows')


class SpeechClient(SuperClient):
    wake_word_handler = None

    def __init__(self, skill_handler, persistence):
        if platform.system() == 'Windows':
            raise OSError
        super().__init__(skill_handler, persistence)

        self.stt_type = ""
        self. tts_type = ""
        self.stt_engine: SttSuper = None
        self.tts_engine: TtsSuper = None

    def setup(self):
        self.wake_word_handler = Porcupine()
        # initialize the stt and tts objects
        self.__update_on_config_change()

    def run(self):
        self.setup()
        while True:
            self.wake_word_handler.monitor_audio(self.stt)

    def stt(self):
        self.__update_on_config_change()
        result = self.stt_engine.listen_and_recognize()

        print("You said " + result)
        self._queue_new_message(result)

    def send(self, message: str, client_attr):
        self.__update_on_config_change()

        if self.persistence.get_config('SpeechClient', 'morse') == "true":
            message = SpeechClient._message2morse(message)
        self.tts_engine.tts(message)

    @staticmethod
    def _message2morse(message):
        # Dictionary representing the morse code chart
        MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                            'C':'-.-.', 'D':'-..', 'E':'.',
                            'F':'..-.', 'G':'--.', 'H':'....',
                            'I':'..', 'J':'.---', 'K':'-.-',
                            'L':'.-..', 'M':'--', 'N':'-.',
                            'O':'---', 'P':'.--.', 'Q':'--.-',
                            'R':'.-.', 'S':'...', 'T':'-',
                            'U':'..-', 'V':'...-', 'W':'.--',
                            'X':'-..-', 'Y':'-.--', 'Z':'--..',
                            '1':'.----', '2':'..---', '3':'...--',
                            '4':'....-', '5':'.....', '6':'-....',
                            '7':'--...', '8':'---..', '9':'----.',
                            '0':'-----', ', ':'--..--', '.':'.-.-.-',
                            '?':'..--..', '/':'-..-.', '-':'-....-',
                            '(':'-.--.', ')':'-.--.-'}
        morse = ''
        for letter in message.upper():
            if letter == ' ':
                morse += ' '
            elif letter in MORSE_CODE_DICT:
                morse += MORSE_CODE_DICT[letter] + ' '
            else:
                morse += ''
        morse = morse.replace('.', "Beep")
        morse = morse.replace('_', "Beeeeeeep")
        return morse

    def __update_on_config_change(self):
        config_stt_type = self.persistence.get_config("SpeechClient", "stt")
        config_tts_type = self.persistence.get_config("SpeechClient", "tts")

        if self.stt_type != config_stt_type:
            self.set_stt_recognizer(config_stt_type)

        if self.tts_type != config_tts_type:
            self.set_tts(config_tts_type)

    def set_stt_recognizer(self, recognizer_type):
        self.stt_type = recognizer_type
        self.stt_engine = SttSuper.create_recognizer(recognizer_type)

    def set_tts(self, tts_type):
        self.tts_type = tts_type
        self.tts_engine = TtsSuper.create_tts(tts_type)
