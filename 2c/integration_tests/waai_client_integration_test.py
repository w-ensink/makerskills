import unittest
from unittest import mock


from who_am_ai_clientside import WhoAmAIClient
from person_data_base import PersonDataBase


class WaaiClientIntegrationTest(unittest.TestCase):
    def test_start_game(self):
        with mock.patch('client.ServerConnection') as MockServerConnection, \
                mock.patch('display.Display') as MockDisplay, \
                mock.patch('speech_to_text_input.SpeechToText') as MockSpeechToText:

            data_base = PersonDataBase.generate_random_data_base()
            server_connection = MockServerConnection()
            display = MockDisplay()
            speech_text = MockSpeechToText()
            waai_client = WhoAmAIClient(server_connection=server_connection,
                                        display=display,
                                        input_provider=speech_text)

            MockServerConnection.return_value.wait_for_message.return_value = 'START' + data_base.to_string()

            waai_client.handle_next_message()

            # assert that the start message has been given and the data base has been received
            self.assertEqual(waai_client.data_base.self_person.name, data_base.self_person.name)

            # make sure a question gets asked when the question command get's received from the server
            MockServerConnection.return_value.wait_for_message.return_value = 'QUESTION'
            MockSpeechToText.return_value.get_user_input.return_value = 'ben je jaap?'
            MockSpeechToText.return_value.get_user_confirmation.return_value = True

            waai_client.handle_next_message()
            server_connection.send_message.assert_called_once_with('ben je jaap?')


if __name__ == '__main__':
    unittest.main()
