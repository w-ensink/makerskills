

import speech_recognition as sr


class SpeechToText:
    def __init__(self):
        pass

    def get_user_input(self):
        microphone = sr.Microphone()
        print(f'microphone names: {microphone.list_microphone_names()}')
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
            return self.get_user_input()
        except sr.UnknownValueError:
            print('couldnt understand that')
            return self.get_user_input()

    def get_user_confirmation(self):
        answer = self.get_user_input()
        while answer != 'ja' and answer != 'nee':
            print(f'{answer} is niet ja of nee')
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