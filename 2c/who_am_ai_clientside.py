from client import ServerConnection
from speech_to_text_input import SpeechToText

PORT = 50_000
IP_ADDRESS = '84.104.226.204'
ADDRESS = (IP_ADDRESS, PORT)


class Player:
    def __init__(self):
        self.server_connection = ServerConnection(ADDRESS)
        self.speech_to_text = SpeechToText()

    def start(self):
        message = self.server_connection.wait_for_message()
        if message.startswith('START'):
            print('start game')

        if message.startswith('QUESTION'):
            print('stel een vraag')
            question = self.speech_to_text.get_user_input()
            print(f'hoorde: "{question}", wil je dit versturen? (ja/nee)')
            while not self.speech_to_text.get_user_conformation():
                question = self.speech_to_text.get_user_input()
                print('het bericht is niet verstuurd, stel opnieuw een vraag')
            print(f'"{question}" is verstuurd, nu is het wachten op een antwoord...')
            self.server_connection.send_message(question)

        elif message.startswith('ANSWER'):
            question_to_answer = message[6:]
            print(f'vraag: "{question_to_answer}"')
            print('zeg iets om te antwoorden')
            answer = self.speech_to_text.get_user_input()
            print(f'hoorde: "{answer}"')
            print('wil je dat versturen? (ja/nee)')
            while not self.speech_to_text.get_user_conformation():
                answer = self.speech_to_text.get_user_input()
                print(f'het bericht is niet verstuurd, spreek opnieuw een vraag in')
            print(f'"{answer}" is verstuurd')
            self.server_connection.send_message(answer)


if __name__ == '__main__':
    player = Player()
    while True:
        player.start()