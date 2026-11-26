import pygame


class Text:

    white = (255, 255, 255)
    grey  = (135, 135, 135)

    def __init__(self, text: str, font: pygame.font.Font, **rect_kwargs):
        self.font = font
        self.rect_kwargs = rect_kwargs

        self.text = None
        self.enabled = True
        
        self.set_text(text)

    def set_text(self, text: str):
        if text == self.text:
            return
        self.text = text

        # Text is white when enabled, grey when disabled
        self.surfaces = {
            True: self.font.render(self.text, True, self.white),
            False: self.font.render(self.text, True, self.grey)
        }
        self.rect = self.surfaces[0].get_rect(**self.rect_kwargs)
