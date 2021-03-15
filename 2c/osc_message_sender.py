from pythonosc.udp_client import SimpleUDPClient
from person_data_base import PersonDataBase
import json


class OSCMessageSender:
    def __init__(self, port):
        self.client = SimpleUDPClient("127.0.0.1", port)

    def send_message(self, address, messages):
        self.client.send_message(address, messages)


def middle_square_method(r, g, b):
    return (((r * g * b) ** 2.0) / 10_000.0) % 10_000.0


class SoundManager:
    def __init__(self):
        self.sender = OSCMessageSender(port=6000)
        with open('game/face_values.json') as f:
            self.colors = json.loads(f.read())

        with open('assets/names.json') as f:
            self.names = json.loads(f.read())

    def send_data_base(self, data_base: PersonDataBase):
        data = []
        active_persons = [p.name for p in data_base.persons if p.is_shown]
        for fn, name in self.names.items():
            if name in active_persons:
                rgb = self.colors[fn]
                data.append(middle_square_method(rgb[0], rgb[1], rgb[2]))

        self.sender.send_message('/persons', data)


if __name__ == '__main__':
    sm = SoundManager()
    db = PersonDataBase.generate_random_data_base()
    sm.send_data_base(db)
