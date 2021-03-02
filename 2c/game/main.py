# Importing the library
import pygame
import pygame.freetype

# Initializing Pygame 
pygame.init()

# game name
pygame.display.set_caption('Who Am AI?')

# Initializing surface 
starting_position = 20
width = 1400
height = 1000

# set variables
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 128)

# number of rows and collums for the images
cols = 7
rows = 3

# rectangle dimensions
rect_width = 1360 / cols - 50
rect_height = 500 / rows + 10

# creating the surface
surface = pygame.display.set_mode((width, height))

background = pygame.image.load(r'D:\hku\jaar2\makerskills\2c\assets\bg.PNG')
background = pygame.transform.scale(background, (1400, 1000))
surface.blit(background, (0, 5))


# Initialing Color
color = (255, 0, 0)

# Drawing image rectangle
pygame.draw.rect(surface, color, pygame.Rect(starting_position,
                                             starting_position,
                                             width - (starting_position * 2),
                                             height / 1.5), 2)

# drawing text rectangle
pygame.draw.rect(surface, (0, 0, 255), pygame.Rect(starting_position,
                                                   700,
                                                   width / 1.5,
                                                   height / 4), 2)

# drawing display for the picture that your opponent has to guess
dit_ben_jij = pygame.Rect((1100, 700), (rect_width * 1.5, rect_height * 1.5))
pygame.display.update(pygame.draw.rect(surface, color, dit_ben_jij))


# drawing mini rectangles
def array_mini_rect():
    grid = []
    for x in range(cols):
        for y in range(rows):
            grid.append(pygame.Rect(starting_position + 25 + x * (1360 / cols),
                                    starting_position + 8 + y * (height / 1.5) / rows,
                                    rect_width,
                                    rect_height))
    return grid


def draw_grid(grid):
    for r in grid:
        pygame.draw.rect(surface, color, r)


draw_grid(array_mini_rect())

# loading AI images over the mini rectangles
image = pygame.image.load(r'D:\hku\jaar2\makerskills\2c\assets\pic_1.PNG')
image = pygame.transform.scale(image, (144, 176))
surface.blit(image, (starting_position + 25, starting_position + 8))

font = pygame.font.Font('freesansbold.ttf', 32)
font1 = pygame.font.Font('freesansbold.ttf', 24)

# create a text surface object,
# on which text is drawn on it.
text = font.render('1', True, black)
question = font1.render('hallo wutru', True, white)

# create a rectangular object for the
# text surface object
textRect = text.get_rect()
questionRect = text.get_rect()

# set the center of the rectangular object.
textRect.center = (starting_position + 25 + rect_width / 2, height / 4.35)
questionRect.center = (starting_position + 30, 750)

# infinite loop
while True:

    # copying the text surface object
    # to the display surface object
    # at the center coordinate.
    surface.blit(text, textRect)
    surface.blit(question, questionRect)

    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    for event in pygame.event.get():

        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT:
            # deactivates the pygame library
            pygame.quit()

            # quit the program.
            quit()

        # Draws the surface object to the screen.
        pygame.display.update()

pygame.display.flip()

x = input()
