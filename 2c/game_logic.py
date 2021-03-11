

import unittest
from person_data_base import PersonDataBase


class InvalidPlayerAmountException(BaseException):
    pass


# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------


class GameLogic:
    # this player class represents any player on the server side.
    # so the sub class of this will be responsible for client communication
    # or if it's local only, it will just be connected to the display & input directly
    class Player:
        # should provide a question that gets asked to the other player
        def provide_question(self) -> str:
            pass

        # should provide the answer to the given question (only 'ja' or 'nee')
        def provide_answer(self, question: str) -> str:
            pass

        # called when this player received an answer from the other player
        def answer_received(self, answer: str):
            pass

        # called at the start of the game, to provide avatar information
        def start_game(self, serialized_person_data_base: str):
            pass

        # called when this player lost the game
        def handle_lost_game(self):
            pass

        # called when this player won the game
        def handle_won_game(self):
            pass

    # ---------------------------------------------------------------------------

    def __init__(self):
        self.players = []
        self.active_player: GameLogic.Player = None
        self.inactive_player: GameLogic.Player = None
        self.keep_running = True

    def setup(self):
        if len(self.players) != 2:
            raise InvalidPlayerAmountException()

        self.active_player = self.players[0]
        self.inactive_player = self.players[1]

        db1, db2 = PersonDataBase.generate_two_random_databases_with_different_self()
        self.active_player.start_game(db1.to_string())
        self.inactive_player.start_game(db2.to_string())

    def add_player(self, player):
        self.players.append(player)

    def get_active_player(self):
        return self.active_player

    def get_inactive_player(self):
        return self.inactive_player

    def run(self):
        self.setup()

        while self.step() and self.keep_running:
            pass

    # returns true if the game should continue, false if it needs to stop
    def step(self) -> bool:
        question = self.active_player.provide_question()
        answer = self.inactive_player.provide_answer(question)
        print(f'vraag: {question}, antwoord: {answer}')

        if question.lower().startswith('jij bent') or question.lower().startswith('je bent') and answer == 'ja':
            self.active_player.handle_won_game()
            self.inactive_player.handle_lost_game()
            return False
        else:
            self.active_player.answer_received(answer)

        self.active_player, self.inactive_player = self.inactive_player, self.active_player
        return True


# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------

class MockPlayer(GameLogic.Player):
    def __init__(self):
        self.num_provided_questions = 0
        self.num_provided_answers = 0
        self.last_asked_question = ''
        self.answer = ''
        self.question = ''
        self.last_received_answer = ''
        self.game_started = False
        self.won_game = None

    def provide_question(self):
        self.num_provided_questions += 1
        return self.question

    def provide_answer(self, question):
        self.last_asked_question = question
        self.num_provided_answers += 1
        return self.answer

    def answer_received(self, answer):
        self.last_received_answer = answer

    def start_game(self, serialized_person_data_base: str):
        self.game_started = True

    def handle_lost_game(self):
        self.won_game = False

    def handle_won_game(self):
        self.won_game = True


class GameLogicTest(unittest.TestCase):
    def setUp(self) -> None:
        self.game = GameLogic()

    def tearDown(self) -> None:
        pass

    def test_start_without_players_expect_exception(self):
        self.assertRaises(InvalidPlayerAmountException, self.game.setup)

    def test_add_single_player(self):
        player = MockPlayer()
        self.game.add_player(player)
        self.assertRaises(InvalidPlayerAmountException, self.game.setup)

    def test_add_two_players(self):
        p1, p2, = MockPlayer(), MockPlayer()
        self.game.add_player(p1)
        self.game.add_player(p2)
        try:
            self.game.setup()
        except InvalidPlayerAmountException:
            self.assertTrue(False, 'exception raised, but shouldn\'t')

    def test_setup(self):
        p1, p2, = MockPlayer(), MockPlayer()
        self.game.add_player(p1)
        self.game.add_player(p2)
        self.game.setup()
        self.assertTrue(p1.game_started)
        self.assertTrue(p2.game_started)

    def test_three_steps(self):
        p1, p2, = MockPlayer(), MockPlayer()
        self.game.add_player(p1)
        self.game.add_player(p2)
        self.game.setup()

        self.assertEqual(self.game.get_active_player(), p1)
        self.assertEqual(self.game.get_inactive_player(), p2)

        # first step
        self.assertTrue(self.game.step())
        self.assertEqual(p1.num_provided_questions, 1)
        self.assertEqual(p2.num_provided_questions, 0)
        self.assertEqual(p1.num_provided_answers, 0)
        self.assertEqual(p2.num_provided_answers, 1)

        self.assertEqual(self.game.get_active_player(), p2)
        self.assertEqual(self.game.get_inactive_player(), p1)

        # second step
        p1.answer = 'answer'
        p2.question = 'question'
        self.assertEqual(p1.last_asked_question, '')
        self.assertEqual(p2.last_received_answer, '')

        self.assertTrue(self.game.step())
        self.assertEqual(p1.num_provided_questions, 1)
        self.assertEqual(p2.num_provided_questions, 1)
        self.assertEqual(p1.num_provided_answers, 1)
        self.assertEqual(p2.num_provided_answers, 1)

        self.assertEqual(p1.last_asked_question, 'question')
        self.assertEqual(p2.last_received_answer, 'answer')

    def test_final_question(self):
        p1, p2, = MockPlayer(), MockPlayer()
        self.game.add_player(p1)
        self.game.add_player(p2)
        self.game.setup()

        p1.question = 'jij bent twee'
        p2.answer = 'ja'

        self.assertFalse(self.game.step())
        self.assertTrue(p1.won_game)
        self.assertFalse(p2.won_game)


if __name__ == '__main__':
    unittest.main()
