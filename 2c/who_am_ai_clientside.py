from client import ServerConnection
from speech_to_text_input import SpeechToText
import threading
from display import Display
import pygame


PORT = 50_000
IP_ADDRESS = '84.104.226.204'
ADDRESS = (IP_ADDRESS, PORT)


class WhoAmAIClient(threading.Thread):
    def __init__(self, display):
        super().__init__()
        self.server_connection = ServerConnection(ADDRESS)
        self.speech_to_text = SpeechToText()
        self.display = display
        self.keep_running = True

    def stop(self):
        self.keep_running = False

    def run(self):
        while self.keep_running:
            self.handle_next_message()
        self.server_connection.close()

    def handle_start_game(self, message):
        grid, this = message.split('&')
        grid = grid.split('|')
        self.display.load_person_grid(grid)
        self.display.load_self_person(this)

    def handle_ask_question(self):
        self.display.set_feedback('Spreek je vraag in')
        question = self.speech_to_text.get_user_input()
        self.display.set_feedback(f'Ik hoorde: "{question}", wil je dit verzenden?')
        while not self.speech_to_text.get_user_conformation():
            self.display.set_feedback('Ik heb het niet verzonden, spreek opnieuw in')
            question = self.speech_to_text.get_user_input()
            self.display.set_feedback(f'Ik hoorde: "{question}", wil je dit verzenden?')
        self.display.set_feedback('Je vraag is verzonden...')
        self.server_connection.send_message(question)
        answer = self.server_connection.wait_for_message()
        self.display.set_feedback(f'Het antwoord: "{answer}". Wacht op de volgende vraag')
        self.server_connection.send_message('OK')

    def handle_answer_question(self, question):
        self.display.set_feedback(f'Vraag: {question}? Spreek je antwoord in.')
        answer = self.speech_to_text.get_user_input()
        self.display.set_feedback(f'Ik hoorde: "{answer}", wil je dat versturen?')
        while not self.speech_to_text.get_user_conformation():
            self.display.set_feedback('Het bericht is niet verstuurd, spreek opnieuw je antwoord in.')
            answer = self.speech_to_text.get_user_input()
            self.display.set_feedback(f'Ik hoorde: "{answer}", wil je dat versturen?')
        self.display.set_feedback('Je antwoord is verstuurd.')
        self.server_connection.send_message(answer)

    def handle_next_message(self):
        message = self.server_connection.wait_for_message()
        if message.startswith('START'):
            self.handle_start_game(message[5:])

        if message.startswith('QUESTION'):
            self.handle_ask_question()

        if message.startswith('ANSWER'):
            self.handle_answer_question(message[6:])

        if message.startswith('WIN'):
            self.display.set_feedback('Je hebt gewonnen!')

        if message.startswith('LOSE'):
            self.display.set_feedback('Je hebt verloren, loser.')


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
            answer = self.server_connection.wait_for_message()
            print(f'The answer is: {answer}')
            self.server_connection.send_message('OK')

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


def main():
    pygame.init()
    clock = pygame.time.Clock()
    display = Display(1400, 1000)
    who_am_ai_client = WhoAmAIClient(display)
    who_am_ai_client.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                who_am_ai_client.stop()
                return 0

        display.render()
        clock.tick(60)


if __name__ == '__main__':
    exit(main())
