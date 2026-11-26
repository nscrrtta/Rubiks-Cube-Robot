from GUI.selector import Selector
from GUI.cubie import Facelet
from GUI.button import Button
from GUI.text import Text

import pygame


class Renderer:

    def __init__(
            self,
            window: pygame.Surface,
            facelets: list[Facelet],
            selectors: list[Selector],
            buttons: list[Button],
            texts: list[Text]
        ):
        self.window = window
        self.facelets = facelets
        self.selectors = selectors
        self.buttons = buttons
        self.texts = texts

    def draw(self):
        self.window.fill((50, 50, 50))

        for text in self.texts:
            self._draw_text(text)

        for button in self.buttons:
            self._draw_button(button)

        for selector in self.selectors:
            self._draw_selector(selector)

        for facelet in self.facelets:
            self._draw_facelet(facelet)

        pygame.display.update()

    def _draw_text(self, text: Text):
        self.window.blit(text.surfaces[text.enabled], text.rect)

    def _draw_button(self, button: Button):
        self.window.blit(button.images[button.enabled], button.position)

    def _draw_selector(self, selector: Selector):
        colour = selector.colour
        pygame.draw.rect(self.window, colour, selector.inner_rect, 0, 5)
        if selector.selected:
            pygame.draw.rect(self.window, colour, selector.outer_rect, 2, 10)

    def _draw_facelet(self, facelet: Facelet):
        pygame.draw.polygon(self.window, facelet.colour, facelet.points_2D)
        pygame.draw.polygon(self.window, (50, 50, 50), facelet.points_2D, width=2)
