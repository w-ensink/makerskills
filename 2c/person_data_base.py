
import json
import pygame


class Person:
    def __init__(self, name, file_name, position):
        self.name = name
        self.photo = pygame.image.load(file_name)
        self.position = position
        self.file_name = file_name
        self.is_shown = True


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
