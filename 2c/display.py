import pygame
from person_data_base import PersonDataBase


class Display:
    def __init__(self, width: int, height: int):
        self.grid_dimensions = (7, 3)
        self.data_base = None
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Who Am AI?')
        self.feedback = 'Wacht tot het spel begint...'
        self.background = pygame.image.load('assets/background/bg1.PNG')
        self.font = pygame.font.Font('assets/fonts/arial.ttf', 28)

    def set_feedback(self, feedback: str):
        self.feedback = feedback

    def set_data_base(self, data_base):
        for p in data_base.persons:
            p.load_photo()
        data_base.self_person.load_photo()
        self.data_base = data_base

    def render_image_grid(self):
        width = self.width
        height = self.height * 0.7
        horizontal_spacing = 0.025 * width
        vertical_spacing = 0.06 * height
        horizontal_person_size = (width - (self.grid_dimensions[0] + 1) * horizontal_spacing) / self.grid_dimensions[0]
        vertical_person_size = (height - (self.grid_dimensions[1] + 1) * vertical_spacing) / self.grid_dimensions[1]

        for p in self.data_base.persons:
            if not p.is_shown:
                continue
            x, y = p.position
            rect = pygame.Rect(horizontal_spacing + (x * (horizontal_spacing + horizontal_person_size)),
                               vertical_spacing + (y * (vertical_spacing + vertical_person_size)),
                               horizontal_person_size,
                               vertical_person_size)
            photo = pygame.transform.scale(p.photo, (rect.width, rect.height))
            self.display.blit(source=photo, dest=rect)
            text = self.font.render(p.name, True, (0, 0, 0))
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
        photo = pygame.transform.scale(self.data_base.self_person.photo, (width, height))
        self.display.blit(source=photo, dest=rect)

        text = self.font.render(self.data_base.self_person.name, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.centerx = horizontal + width / 2
        text_rect.centery = vertical + height + 20
        self.display.blit(source=text, dest=text_rect)

    def render_feedback(self):
        lines = self.feedback.splitlines()
        for i, l in enumerate(lines):
            text = self.font.render(l, True, (0, 0, 0))
            rect = text.get_rect()
            rect.centerx = self.width * 0.33
            rect.centery = self.height * 0.8 + 40 * i
            self.display.blit(text, rect)

    def render_background(self):
        self.display.fill(color=(200, 100, 200))
        bg = pygame.transform.scale(self.background, (self.width, self.height))
        self.display.blit(source=bg, dest=pygame.Rect(0, 0, self.width, self.height))

    def render(self):
        self.render_background()
        if self.data_base:
            self.render_image_grid()
            self.render_self()
        self.render_feedback()
        pygame.display.update()


# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------

def add_remove_faces(data_base: PersonDataBase):
    input('enter to remove..')
    data_base.make_person_invisible('Paul')
    input('enter to put back')
    data_base.make_person_visible('Paul')
    input('enter to stop')


def main():
    pygame.init()
    clock = pygame.time.Clock()
    data_base, _ = PersonDataBase.generate_two_random_databases_with_different_self()
    display = Display(width=1400, height=1000)
    display.set_data_base(data_base)
    # t = threading.Thread(target=add_remove_faces, args={data_base})
    # t.start()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

        display.render()
        clock.tick(24)


if __name__ == '__main__':
    exit(main())


