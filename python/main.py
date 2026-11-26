from GUI.constants import WINDOW_WIDTH, WINDOW_HEIGHT
from GUI.gui import GUI
import pygame


pygame.init()
pygame.display.set_caption('Rubik\'s Cube Robot by Nick Sciarretta')

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

gui = GUI(window)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            gui.handle_event(event)

    gui.update()
    clock.tick(60)

gui.animation.close()
pygame.quit()
