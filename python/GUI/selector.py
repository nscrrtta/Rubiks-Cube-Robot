from GUI.constants import COLOUR_SELECTOR_POS, COLOUR_SELECTOR_SIZE, RGB_VALUES
import pygame


class Selector:

    def __init__(self, index: int):
        self.index = index
        self.selected = False
        self.colour = RGB_VALUES[index]

        self.inner_rect = self._get_rect(0)
        self.outer_rect = self._get_rect(6)

    def clicked(self, x: int, y: int) -> bool:
        return self.inner_rect.collidepoint(x, y)

    def _get_rect(self, offset: int) -> pygame.Rect:
        x, y = COLOUR_SELECTOR_POS[self.index]
        return pygame.Rect(
            x - offset,
            y - offset,
            COLOUR_SELECTOR_SIZE + 2 * offset,
            COLOUR_SELECTOR_SIZE + 2 * offset
        )
