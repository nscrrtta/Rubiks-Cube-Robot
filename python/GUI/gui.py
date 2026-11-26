from Kociemba.solver import Solver as KociembaSolver
from Kociemba.tables import tables

from CFOP.solver import Solver as CFOPSolver
from CFOP.constants import *

from GUI.constants import *
from GUI.animation import Animation
from GUI.renderer import Renderer
from GUI.selector import Selector
from GUI.button import Button
from GUI.cubie import Facelet
from GUI.cube import Cube
from GUI.text import Text

import pygame
import random
import time


class GUI:

    def __init__(self, window: pygame.Surface):
        # 3D cube for drawing
        self.cube = Cube()

        # Colour selectors
        self.colour_selectors = [Selector(i) for i in range(6)]
        self.selected_colour = self.colour_selectors[0]
        self.selected_colour.selected = True

        # Buttons
        self.toggle_btn = Button(TOGGLE_BUTTON_POS, 'toggle')
        self.solve_btn = Button(SOLVE_BUTTON_POS, 'solve')
        self.scrmb_btn = Button(SCRMB_BUTTON_POS, 'scrmb')
        self.abort_btn = Button(ABORT_BUTTON_POS, 'abort')
        self.globe_btn = Button(GLOBE_BUTTON_POS, 'globe')
        self.URF_btn = Button(HOME1_BUTTON_POS, 'home1')
        self.DLB_btn = Button(HOME2_BUTTON_POS, 'home2')

        # Text
        small_font = pygame.font.SysFont('Arial', SMALL_FONT_SIZE)
        large_font = pygame.font.SysFont('Arial', LARGE_FONT_SIZE)

        self.koci_text = Text('Kociemba', small_font, topright=KOCIEMBA_TEXT_POS)
        self.cfop_text = Text('CFOP', small_font, topright=CFOP_TEXT_POS)
        self.move_text = Text('', large_font, center=MOVE_COUNTER_POS)

        self.abort_btn.enabled = False
        self.globe_btn.enabled = False
        self.cfop_text.enabled = False

        buttons = [
            self.toggle_btn,
            self.solve_btn,
            self.scrmb_btn,
            self.abort_btn,
            self.globe_btn,
            self.URF_btn,
            self.DLB_btn
        ]
        text = [self.koci_text, self.cfop_text, self.move_text]

        # Draws everything in these lists
        self.renderer = Renderer(window, self.cube.facelets, self.colour_selectors, buttons, text)

        # Animates the cube and sends moves to motors
        self.animation = Animation(self.cube, self.renderer)

        # Colours of cube represented as a 1D array
        self.colours = [i//9 for i in range(54)]

        # For detecting taps, swipes and drags
        self.last_touch_pos: tuple[int, int] | None = None
        self.last_touch_time = 0.0

        # For checking if cube is solvable / solving cube
        self.koci_solver = KociembaSolver()
        self.cfop_solver = CFOPSolver()

        # Increments when cube is being solved
        self.move_counter = 0

        if not tables.all_tables_loaded:
            self._toggle_algorithm()
        self.renderer.draw()

    ### Input ###

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._mouse_down(*event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self._mouse_up(*event.pos)
        elif event.type == pygame.MOUSEMOTION:
            self._mouse_motion(*event.pos)

    def _mouse_down(self, x: int, y: int):
        self.last_touch_time = time.time()

        if self.solve_btn.enabled_and_clicked(x, y):
            self._solve()
        elif self.scrmb_btn.enabled_and_clicked(x, y):
            self._scramble()
        elif self.abort_btn.enabled_and_clicked(x, y):
            self.animation.abort()
        elif self.URF_btn.enabled_and_clicked(x, y):
            self.animation.rotate_to_URF()
        elif self.DLB_btn.enabled_and_clicked(x, y):
            self.animation.return_to_DLB()
        elif self.globe_btn.clicked(x, y):
            self.globe_btn.enabled = not self.globe_btn.enabled
            self.renderer.draw()
        elif self.toggle_btn.clicked(x, y):
            self._toggle_algorithm()
            self.renderer.draw()
        elif selector := self._get_clicked_selector(x, y):
            self._set_selected_colour(selector)
        elif not self.abort_btn.enabled and self._inside_circle(x, y):
            self.last_touch_pos = (x, y)

    def _mouse_up(self, x: int, y: int):
        if self.abort_btn.enabled or self.last_touch_pos is None:
            return

        dt = time.time() - self.last_touch_time
        last_pos = self.last_touch_pos
        
        if dt <= 0.2 and (facelet := self._get_clicked_facelet(x, y)) is not None:
            self._set_facelet_colour(facelet)
            if self.toggle_btn.enabled:
                solvable = self.koci_solver.solvable(self.colours)
            else:
                solvable = self.cfop_solver.solvable(self.colours)
            self.solve_btn.enabled = self.scrmb_btn.enabled = solvable
            self.renderer.draw()

        elif dt <= 0.7 and not self.globe_btn.enabled:
            if self._mouse_inside_circle(x, y):
                self.animation.rotate_swipe(*last_pos, x, y)

        self.last_touch_pos = None

    def _mouse_motion(self, x: int, y: int):
        if self.abort_btn.enabled or not self.globe_btn.enabled:
            return
        if not self._mouse_inside_circle(x, y):
            return

        self.animation.rotate_drag(*self.last_touch_pos, x, y)
        self.last_touch_pos = (x, y)

    def _mouse_inside_circle(self, x: int, y: int) -> bool:
        if self.last_touch_pos is None:
            return False
        return self._inside_circle(x, y) \
            and self._inside_circle(*self.last_touch_pos)

    def _inside_circle(self, x: int, y: int) -> bool:
        return (x - ORIGIN_X) ** 2 + (y - ORIGIN_Y) ** 2 <= 300 ** 2

    ### Button actions ###

    def _solve(self):
        self._enable_buttons(False)
        self.move_text.set_text('')
        self.move_counter = 0

        moves: list[str] = []
        if self.toggle_btn.enabled:
            moves = self.koci_solver.solve(self.colours)
        if not moves:
            moves = self.cfop_solver.solve(self.colours)
        self.animation.moves = moves

    def _scramble(self):
        self._enable_buttons(False)
        self.move_text.set_text('')
        self.move_counter = -1

        moves: list[str] = []
        faces = [f for f in 'FBLRD']

        for _ in range(20):
            face = random.choice(faces)
            turn = random.choice(['1', '2', '3'])
            moves.append(face + turn)

            # Don't repeat the same face
            faces = [f for f in 'FBLRD' if f != face]

        print(f'Scramble: {moves}')
        self.animation.moves = moves[::-1]

    def _get_clicked_selector(self, x: int, y: int) -> Selector | None:
        for selector in self.colour_selectors:
            if selector.clicked(x, y):
                return selector
        return None

    def _set_selected_colour(self, selector: Selector):
        self.selected_colour.selected = False
        self.selected_colour = selector
        selector.selected = True
        self.renderer.draw()

    def _get_clicked_facelet(self, x: int, y: int) -> Facelet | None:
        if self.last_touch_pos is None:
            return None
        facelet1 = self.cube.get_clicked_facelet(*self.last_touch_pos)
        facelet2 = self.cube.get_clicked_facelet(x, y)
        if facelet1 is None or facelet2 is None or facelet1.index != facelet2.index:
            return None
        return facelet1

    def _set_facelet_colour(self, facelet: Facelet):
        self.colours[facelet.index] = self.selected_colour.index
        facelet.set_colour(self.selected_colour.index)

    def _enable_buttons(self, enabled: bool):
        for button in [self.solve_btn, self.scrmb_btn, self.URF_btn, self.DLB_btn]:
            button.enabled = enabled
        self.abort_btn.enabled = not enabled
        self.renderer.draw()

    def _toggle_algorithm(self):
        if tables.all_tables_loaded:
            self.toggle_btn.enabled = not self.toggle_btn.enabled
        else:
            self.toggle_btn.enabled = False
        self.cfop_text.enabled = not self.toggle_btn.enabled
        self.koci_text.enabled = self.toggle_btn.enabled

    ### Moves ###

    def update(self):
        if self.animation.moves:
            self.animation.make_next_move()
            if self.move_counter >= 0:
                self.move_counter += 1
                self.move_text.set_text(f'{self.move_counter}')
    
        # After completing last move
        elif self.abort_btn.enabled:
            self.colours = self.cube.update_facelet_indices()
            self.animation.disable_motors()
            self._enable_buttons(True)
