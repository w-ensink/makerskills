
import json
import pygame
import unittest
import random


class Person:
    def __init__(self, name, file_name, position, load_photo=False):
        self.name = name
        self.position = position
        self.file_name = file_name
        self.is_shown = True
        self.photo = None
        if load_photo:
            self.load_photo()

    def load_photo(self):
        self.photo = pygame.image.load(self.file_name)

    def to_string(self):
        pos = f'{self.position[0]}&{self.position[1]}'
        show = str(self.is_shown)
        return f'{self.name}${self.file_name}${pos}${self.is_shown}'

    @staticmethod
    def from_string(string: str):
        items = string.split('$')
        name = items[0]
        file_name = items[1]
        posx, posy = items[2].split('&')
        show = items[3] == 'True'
        p = Person(name, file_name, (int(posx), int(posy)))
        p.is_shown = show
        return p


# --------------------------------------------------------------------------------------------------------------

class PersonDataBase:
    def __init__(self):
        self.persons = []
        self.self_person = None

        with open('assets/names.json') as f:
            self.names = json.loads(f.read())

    def load_self_person(self, file_name):
        self.self_person = Person(name=self.names[file_name], file_name=f'assets/faces/{file_name}', position=(-1, -1))

    def load_file_names(self, file_names: [str]):
        self.persons.clear()
        for x in range(7):
            for y in range(3):
                index = x * 3 + y
                fn = file_names[index]
                name = self.names[fn]
                self.persons.append(Person(name=name, file_name=f'assets/faces/{fn}', position=(x, y)))

    def load_photos(self):
        for p in self.persons:
            p.load_photo()
        self.self_person.load_photo()

    def make_person_invisible(self, person_name):
        for p in self.persons:
            if p.name == person_name:
                p.is_shown = False

    def make_person_visible(self, person_name):
        for p in self.persons:
            if p.name == person_name:
                p.is_shown = True

    @staticmethod
    def generate_random_data_base():
        db = PersonDataBase()
        file_names = [f'm_{x * 3 + y + 1}.png' for x in range(7) for y in range(3)]
        db.load_file_names(file_names)
        db.load_self_person(file_names[4])
        return db

    def to_string(self):
        persons = '#'.join(p.to_string() for p in self.persons)
        return f'{self.self_person.to_string()}|{persons}'

    @staticmethod
    def from_string(string):
        this, persons = string.split('|')
        db = PersonDataBase()
        db.self_person = Person.from_string(this)
        db.persons = [Person.from_string(s) for s in persons.split('#')]
        return db

    @staticmethod
    def get_random_file_names():
        available_file_names = []
        available_file_names.extend([f'm_{i + 1}.png' for i in range(24)])
        available_file_names.extend([f'f_{i + 1}.png' for i in range(24)])
        random.shuffle(available_file_names)
        return available_file_names[:21]

    @staticmethod
    def generate_two_random_databases_with_different_self():
        file_names = PersonDataBase.get_random_file_names()
        self_1 = random.choice(file_names)
        self_2 = random.choice(file_names)
        while self_1 == self_2:
            self_2 = random.choice(file_names)
        db1 = PersonDataBase()
        db2 = PersonDataBase()
        db1.load_file_names(file_names)
        db1.load_self_person(self_1)
        db2.load_self_person(self_2)
        db2.load_file_names(file_names)
        return db1, db2


# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------


class PersonSerialisationTest(unittest.TestCase):
    def test_serialise(self):
        p = Person('Paul', 'paul.png', (0, 1))
        string = p.to_string()
        p2 = Person.from_string(string)
        self.assertEqual(p.name, p2.name)
        self.assertEqual(p.file_name, p2.file_name)
        self.assertEqual(p.is_shown, p2.is_shown)
        self.assertEqual(p.position, p2.position)


class PersonDataBaseSerialisationTest(unittest.TestCase):
    def test_seperate_serialisation(self):
        o = PersonDataBase.generate_random_data_base()
        string = o.to_string()
        o2 = PersonDataBase.from_string(string)

        self.assertEqual(o.self_person.name, o2.self_person.name)
        self.assertEqual(o.self_person.file_name, o2.self_person.file_name)

        for p1, p2 in zip(o.persons, o2.persons):
            self.assertEqual(p1.name, p2.name)
            self.assertEqual(p1.file_name, p2.file_name)


if __name__ == '__main__':
    unittest.main()