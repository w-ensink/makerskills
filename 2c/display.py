import pygame


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

        for x in range(self.grid_dimensions[0]):
            for y in range(self.grid_dimensions[1]):
                number = x * self.grid_dimensions[1] + y + 1
                self.persons.append(Person(name='joep',
                                           file_path=f'game/assets/male/m_{number}.PNG',
                                           position=(x, y)))

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
            text = font.render('Peter', True, (0, 255, 0))
            text_rect = text.get_rect()
            text_rect.centerx = horizontal_spacing + (x * (horizontal_spacing + horizontal_person_size)) + 0.5 * horizontal_person_size
            text_rect.centery = vertical_spacing + (y * (vertical_spacing + vertical_person_size)) + vertical_person_size + 0.5 * vertical_spacing
            self.display.blit(source=text, dest=text_rect)

    def render(self):
        self.display.fill(color=(200, 100, 200))
        self.render_image_grid()
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
