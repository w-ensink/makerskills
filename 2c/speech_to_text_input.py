

import speech_recognition as sr
# TODO: FeedbackListener class die aangeroepen wordt wanneer input niet begrepen wordt

class SpeechToText:
    class FeedbackListener:
        def speech_could_not_be_recognized(self):
            pass

        def speech_server_error(self):
            pass

        def speech_not_confirmation_type(self):
            pass

    def __init__(self):
        self.feedback_listeners = []

    def add_feedback_listener(self, listener):
        self.feedback_listeners.append(listener)

    def get_user_input(self):
        microphone = sr.Microphone()
        recognizer = sr.Recognizer()
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.6)
            audio = recognizer.listen(source)

        print('sending data to google')
        try:
            response = recognizer.recognize_google(audio, language='nl-NL')
            return response
        except sr.RequestError:
            print('failed request')
            for l in self.feedback_listeners:
                l.speech_server_error()
            return self.get_user_input()
        except sr.UnknownValueError:
            print('couldnt understand that')
            for l in self.feedback_listeners:
                l.speech_could_not_be_recognized()
            return self.get_user_input()

    def get_user_confirmation(self):
        answer = self.get_user_input()
        while answer != 'ja' and answer != 'nee':
            print(f'{answer} is niet ja of nee')
            for l in self.feedback_listeners:
                l.speech_not_confirmation_type()
            answer = self.get_user_input()
        return answer == 'ja'


if __name__ == '__main__':
    speech_text = SpeechToText()

    while True:
        print('zeg iets...')
        ans = speech_text.get_user_input()
        print(f'heard: {ans}')
        if ans == 'stop':
            print('weet je het zeker?')
            if speech_text.get_user_confirmation():
                break