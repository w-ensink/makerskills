from client import ServerConnection
from speech_to_text_input import SpeechToText
import threading
from display import Display
import pygame
from person_data_base import PersonDataBase
from utility import limit_words_per_line
from osc_message_sender import SoundManager, ScoreManager

PORT = 50_000
IP_ADDRESS = '84.104.226.204'


# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------


class State:
    def get_recognition_error_feedback(self):
        pass

    def get_default_feedback(self):
        pass

    def get_confirmation_error(self):
        pass

    def get_confirmation_message(self):
        pass

    def get_final_feedback(self):
        pass

    def get_feedback_after_decline(self):
        pass


class AnsweringQuestionState(State):
    def __init__(self, question: str):
        self.question = question
        self.answer = ''

    def get_default_feedback(self):
        return f'{self.question}?\n' \
               f'Wat is jouw antwoord?.'

    def get_confirmation_message(self):
        return f'De vraag was:\n' \
               f'"{self.question}?"\n' \
               f'Jouw antwoord is: "{self.answer}".\n' \
               f'Wil je dit versturen? (ja/nee)'

    def get_feedback_after_decline(self):
        return f'Je antwoord is niet verstuurd, spreek opnieuw in.\n' \
               f'De vraag was:\n"{self.question}?"'

    def get_confirmation_error(self):
        return f'Dat was geen "ja" of "nee".\n' \
               f'De vraag was:\n' \
               f'"{self.question}?"\n' \
               f'Jouw antwoord is: "{self.answer}".\n' \
               f'Wil je dit versturen? (ja/nee)'

    def get_recognition_error_feedback(self):
        return f'Dat kon ik niet verstaan.\n' \
               f'Probeer opnieuw je antwoord in te spreken.\n' \
               f'De vraag was:\n' \
               f'"{self.question}?"'

    def get_final_feedback(self):
        return 'Je antwoord is verzonden.'


class EliminatingFacesState(State):
    def __init__(self, question, answer):
        self.question, self.answer = question, answer
        self.persons_to_remove = ''

    def get_default_feedback(self):
        return f'Je vraag was: "{self.question}?"\n' \
               f'Het antwoord is: "{self.answer}"\n' \
               f'Welke personen wil je weghalen?'

    def get_confirmation_message(self):
        if self.persons_to_remove == '':
            return f'Ik heb geen gezichten weggehaald, is dat wat je wilde? (ja/nee)\n' \
                   f'Vraag: "{self.question}?"\n' \
                   f'Antwoord: "{self.answer}"'
        return f'{limit_words_per_line(self.persons_to_remove, 8)}\n' \
               f'Waren dit alle gezichten die je weg wil hebben? (ja/nee)\n' \
               f'Vraag: "{self.question}?"\n' \
               f'Anwoord: "{self.answer}"'

    def get_feedback_after_decline(self):
        return f'Oke, welke personen vallen nog meer weg?\n' \
               f'Vraag: "{self.question}?"\n' \
               f'Anwoord: "{self.answer}"'

    def get_confirmation_error(self):
        if self.persons_to_remove == '':
            return f'Dat was geen "ja" of "nee", probeer het opnieuw.\n' \
                   f'Ik heb geen gezichten weggehaald, is dat wat je wilde? (ja/nee)\n' \
                   f'Vraag: "{self.question}?"\n' \
                   f'Antwoord: "{self.answer}"'
        return f'Dat was geen "ja" of "nee", probeer het opnieuw\n' \
               f'Wil je nog meer personen weghalen? (ja/nee)\n'\
               f'Vraag: "{self.question}?"\n' \
               f'Anwoord: "{self.answer}"'

    def get_recognition_error_feedback(self):
        return f'Dat kon ik niet verstaan.\n' \
               f'Welke gezichten wil je weg hebben?\n' \
               f'Vraag: "{self.question}?"\n' \
               f'Anwoord: "{self.answer}"'

    def get_final_feedback(self):
        return f'Oke, dan is het nu weer wachten op de volgende vraag.'


class AskingQuestionState(State):
    def __init__(self):
        self.question = ''

    def get_default_feedback(self):
        return 'Spreek je vraag in.'

    def get_confirmation_message(self):
        return f'Ik hoorde: "{self.question}?"\n' \
               f'Wil je dit versturen? (ja/nee)'

    def get_feedback_after_decline(self):
        return 'Je vraag is niet verstuurd.\n' \
               'Spreek opnieuw je vraag in.'

    def get_confirmation_error(self):
        return f'Dat is geen "ja" of "nee", probeer het opnieuw.\n' \
               f'Je vraag is:\n' \
               f'"{self.question}"?\n' \
               f'Wil je dit versturen?'

    def get_recognition_error_feedback(self):
        return 'Dat kon ik niet verstaan.'

    def get_final_feedback(self):
        return 'Je vraag is verzonden.\n' \
               'Nu is het wachten op het antwoord.'


class WhoAmAIClient(threading.Thread, SpeechToText.FeedbackListener):
    def __init__(self, input_provider, server_connection: ServerConnection, display: Display):
        super().__init__()
        self.server_connection = server_connection
        self.input_provider = input_provider
        self.data_base = None
        self.display = display
        self.keep_running = True
        self.sound_manager = SoundManager()
        self.input_provider.add_feedback_listener(self)
        self.score_manager = ScoreManager()
        self.feedback_state = None
        self.last_asked_question = ''

    # from SpeechToText.FeedbackListener
    def speech_server_error(self):
        self.display.set_feedback(self.feedback_state.get_recognition_error_feedback())
        self.sound_manager.trigger_not_understand_sound()

    # from SpeechToText.FeedbackListener
    def speech_could_not_be_recognized(self):
        self.display.set_feedback(self.feedback_state.get_recognition_error_feedback())
        self.sound_manager.trigger_not_understand_sound()

    def speech_not_confirmation_type(self):
        self.display.set_feedback(self.feedback_state.get_confirmation_error())
        self.sound_manager.trigger_not_understand_sound()

    def stop(self):
        self.keep_running = False

    def run(self):
        while self.keep_running:
            self.handle_next_message()
        self.server_connection.close()

    def handle_start_game(self, message):
        self.data_base = PersonDataBase.from_string(message)
        self.display.set_data_base(self.data_base)
        self.display.set_feedback('Wacht op de andere speler')
        score_data = self.score_manager.get_score(self.data_base)
        self.sound_manager.send_data(score_data)
        self.sound_manager.trigger_start_sound()

    def handle_persons_to_remove(self):
        persons_to_remove = self.input_provider.get_user_input()
        self.sound_manager.trigger_neutral_sound()
        to_remove_names = []
        for p in self.data_base.persons:
            if p.name in persons_to_remove.split(' '):
                self.data_base.make_person_invisible(p.name)
                to_remove_names.append(p.name)
        return ', '.join(to_remove_names)

    def remove_all_desired_faces(self):
        self.feedback_state.persons_to_remove = self.handle_persons_to_remove()
        self.display.set_feedback(self.feedback_state.get_confirmation_message())
        self.sound_manager.trigger_neutral_sound()
        while not self.input_provider.get_user_confirmation():
            self.display.set_feedback(self.feedback_state.get_feedback_after_decline())
            self.feedback_state.persons_to_remove = self.handle_persons_to_remove()
            self.display.set_feedback(self.feedback_state.get_confirmation_message())
            self.sound_manager.trigger_neutral_sound()

    def handle_answer_received(self, answer):
        self.feedback_state = EliminatingFacesState(answer=answer,
                                                    question=self.last_asked_question)
        self.sound_manager.trigger_receive_sound()
        self.display.set_feedback(self.feedback_state.get_default_feedback())
        self.remove_all_desired_faces()
        self.display.set_feedback(self.feedback_state.get_final_feedback())
        score_data = self.score_manager.get_score(self.data_base)
        message = 'OK' + '|'.join([str(i) for i in score_data])
        print(f'sent: {message}')
        self.server_connection.send_message(message)
        self.sound_manager.trigger_send_sound()

    def handle_ask_question(self):
        self.feedback_state = AskingQuestionState()
        self.display.set_feedback(self.feedback_state.get_default_feedback())
        self.sound_manager.trigger_neutral_sound()
        self.feedback_state.question = self.input_provider.get_user_input()
        self.display.set_feedback(self.feedback_state.get_confirmation_message())

        while not self.input_provider.get_user_confirmation():
            self.display.set_feedback(self.feedback_state.get_feedback_after_decline())
            self.feedback_state.question = self.input_provider.get_user_input()
            self.display.set_feedback(self.feedback_state.get_confirmation_message())
            self.sound_manager.trigger_neutral_sound()

        self.display.set_feedback(self.feedback_state.get_final_feedback())
        self.server_connection.send_message(self.feedback_state.question)
        self.last_asked_question = self.feedback_state.question
        self.sound_manager.trigger_send_sound()

    def handle_answer_question(self, question):
        self.feedback_state = AnsweringQuestionState(question)
        self.sound_manager.trigger_receive_sound()
        self.display.set_feedback(self.feedback_state.get_default_feedback())
        self.feedback_state.answer = self.input_provider.get_user_input()
        self.sound_manager.trigger_neutral_sound()
        self.display.set_feedback(self.feedback_state.get_confirmation_message())

        while not self.input_provider.get_user_confirmation():
            self.display.set_feedback(self.feedback_state.get_feedback_after_decline())
            self.feedback_state.answer = self.input_provider.get_user_input()
            self.display.set_feedback(self.feedback_state.get_confirmation_message())
            self.sound_manager.trigger_neutral_sound()

        self.display.set_feedback(self.feedback_state.get_final_feedback())
        self.server_connection.send_message(self.feedback_state.answer)
        self.sound_manager.trigger_send_sound()

    def handle_next_message(self):
        message = self.server_connection.wait_for_message()
        if message.startswith('START'):
            self.handle_start_game(message[5:])

        if message.startswith('QUESTION'):
            print(f'received: {message}')
            if len(message) > len('QUESTION'):
                score_data = [int(i) for i in message[8:].split('|')]
                self.sound_manager.send_data(score_data)
            self.feedback_state = AskingQuestionState()
            self.handle_ask_question()

        if message.startswith('ANSWER'):
            question = message[6:]
            self.handle_answer_question(question)

        if message.startswith('RESPONSE'):
            self.handle_answer_received(message[8:])

        if message.startswith('WIN'):
            self.display.set_feedback('Je hebt gewonnen!')
            self.sound_manager.trigger_win_sound()
            self.stop()

        if message.startswith('LOSE'):
            self.display.set_feedback('Je hebt verloren, loser.')
            self.sound_manager.trigger_lose_sound()
            self.stop()


# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------

def main():
    pygame.init()
    clock = pygame.time.Clock()
    display = Display(width=1400, height=1000)
    server_connection = ServerConnection((IP_ADDRESS, PORT))
    input_provider = SpeechToText()
    who_am_ai_client = WhoAmAIClient(input_provider, server_connection, display)
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
