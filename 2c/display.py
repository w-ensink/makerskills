import pygame
import json
import random


def load_random_persons():
    num_men = 10
    num_women = 11
    persons = []
    with open('game/names.json') as f:
        names = json.loads(f.read())

    for x in range(7):
        for y in range(3):
            if random.randint(0, 1):
                persons.append(Person(name=names[f'm_{x * 3 + y + 1}.png'],
                                      file_path=f'game/assets/male/m_{x * 3 + y + 1}.png',
                                      position=(x, y)))
            else:
                persons.append(Person(name=names[f'f_{x * 3 + y + 1}.png'],
                                      file_path=f'game/assets/female/f_{x * 3 + y + 1}.png',
                                      position=(x, y)))
    return persons


class Person:
    def __init__(self, name, file_path, position: (int, int)):
        self.name = name
        self.photo = pygame.image.load(file_path)
        self.position = position


class Display:
    def __init__(self, width, height):
        self.grid_dimensions = (7, 3)
        self.persons = []
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Who Am AI?')
        self.feedback = 'ben jij piemel?'
        self.self_person = Person('Piemel', 'game/assets/male/m_4.PNG', (-1, -1))
        self.background = pygame.image.load('game/assets/background/bg.PNG')

    def set_feedback(self, feedback):
        self.feedback = feedback

    def load_person_grid(self, names):
        assert len(names) == 21
        with open('game/names.json') as f:
            corresponsing_names = json.loads(f.read())

        for x in range(self.grid_dimensions[0]):
            for y in range(self.grid_dimensions[1]):
                number = x * self.grid_dimensions[1] + y
                file_name = names[number]
                gender = 'male' if file_name.startswith('m') else 'female'
                path = f'game/assets/{gender}/{file_name}'
                self.persons.append(Person(name=corresponsing_names[names[number]],
                                           file_path=path,
                                           position=(x, y)))

    def load_self_person(self, name):
        with open('game/names.json') as f:
            corresponsing_names = json.loads(f.read())

        gender = 'male' if name.startswith('m') else 'female'
        path = f'game/assets/{gender}/{name}'
        self.self_person = Person(name=corresponsing_names[name], file_path=path, position=(-1, -1))

    def render_image_grid(self):
        width = self.width
        height = self.height * 0.7
        horizontal_spacing = 0.025 * width
        vertical_spacing = 0.06 * height
        horizontal_person_size = (width - (self.grid_dimensions[0] + 1) * horizontal_spacing) / self.grid_dimensions[0]
        vertical_person_size = (height - (self.grid_dimensions[1] + 1) * vertical_spacing) / self.grid_dimensions[1]

        for p in self.persons:
            x, y = p.position
            rect = pygame.Rect(horizontal_spacing + (x * (horizontal_spacing + horizontal_person_size)),
                               vertical_spacing + (y * (vertical_spacing + vertical_person_size)),
                               horizontal_person_size,
                               vertical_person_size)
            photo = pygame.transform.scale(p.photo, (rect.width, rect.height))
            self.display.blit(source=photo, dest=rect)
            font = pygame.font.Font('game/assets/fonts/arial.ttf', 28)
            text = font.render(p.name, True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.centerx = horizontal_spacing + (
                        x * (horizontal_spacing + horizontal_person_size)) + 0.5 * horizontal_person_size
            text_rect.centery = vertical_spacing + (
                        y * (vertical_spacing + vertical_person_size)) + vertical_person_size + 0.5 * vertical_spacing
            self.display.blit(source=text, dest=text_rect)

    def render_self(self):
        horizontal = self.width * 0.7
        vertical = self.height * 0.75
        width = int(self.width * 0.15)
        height = int(self.height * 0.2)
        rect = pygame.Rect(horizontal, vertical, width, height)
        photo = pygame.transform.scale(self.self_person.photo, (width, height))
        self.display.blit(source=photo, dest=rect)

        font = pygame.font.Font('game/assets/fonts/arial.ttf', 28)
        text = font.render(self.self_person.name, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.centerx = horizontal + width / 2
        text_rect.centery = vertical + height + 20
        self.display.blit(source=text, dest=text_rect)

    def render_feedback(self):
        font = pygame.font.Font('game/assets/fonts/arial.ttf', 32)
        text = font.render(self.feedback, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.centerx = self.width * 0.33
        text_rect.centery = self.height * 0.8
        self.display.blit(source=text, dest=text_rect)

    def render(self):
        self.display.fill(color=(200, 100, 200))
        bg = pygame.transform.scale(self.background, (self.width, self.height))
        self.display.blit(source=bg, dest=pygame.Rect(0, 0, self.width, self.height))
        self.render_image_grid()
        self.render_self()
        self.render_feedback()
        pygame.display.update()


def main():
    pygame.init()
    clock = pygame.time.Clock()
    display = Display(1400, 1000)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

        display.render()
        clock.tick(60)


if __name__ == '__main__':
    exit(main())
