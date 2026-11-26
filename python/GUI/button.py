from GUI.constants import PNG_DIR
import pygame


class Button:

    def __init__(self, position: tuple[int, int], name: str):
        self.position = position
        self.enabled = True

        # Button is white when enabled, grey when disabled
        self.images = {
            True: self._load_image(f'{name}_white.png'),
            False: self._load_image(f'{name}_grey.png')
        }

        # Both images are the same size, so either can be used
        self.rect = self.images[0].get_rect(topleft=position)
    
    def enabled_and_clicked(self, x: int, y: int) -> bool:
        return self.enabled and self.clicked(x, y)

    def clicked(self, x: int, y: int) -> bool:
        return self.rect.collidepoint(x, y)

    def _load_image(self, file: str) -> pygame.Surface:
        return pygame.image.load(PNG_DIR / file)
