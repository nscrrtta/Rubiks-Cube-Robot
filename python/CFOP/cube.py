from Kociemba.enums import Corner as Co, Edge as Ed, Facelet as Fc
from CFOP.constants import *


Corner = tuple[int, int, int]
Edge = tuple[int, int]


class Cube:

    def __init__(self, colours: list[int], faces: dict[str, str], moves: list[str]):
        self.colours = colours.copy()
        self.faces = faces.copy()
        self.moves = moves.copy()

    def spawn_child(self) -> 'Cube':
        return Cube(self.colours, self.faces, self.moves)

    def edge_solved(self, edge: int) -> bool:
        return self._current_edges()[edge] == self._solved_edges()[edge]

    def corner_solved(self, corner: int) -> bool:
        return self._current_corners()[corner] == self._solved_corners()[corner]

    def find_edge(self, edge: int) -> int:
        e1 = self._solved_edges()[edge]
        for i, e2 in self._current_edges().items():
            if set(e1) == set(e2):
                return i

    def find_corner(self, corner: int) -> int:
        c1 = self._solved_corners()[corner]
        for i, c2 in self._current_corners().items():
            if set(c1) == set(c2):
                return i

    def _current_edges(self) -> dict[int, Edge]:
        return {
            # Top layer
            Ed.UR: (self.colours[Fc.U6], self.colours[Fc.R2]),
            Ed.UF: (self.colours[Fc.U8], self.colours[Fc.F2]),
            Ed.UL: (self.colours[Fc.U4], self.colours[Fc.L2]),
            Ed.UB: (self.colours[Fc.U2], self.colours[Fc.B2]),

            # Middle layer
            Ed.FR: (self.colours[Fc.F6], self.colours[Fc.R4]),
            Ed.FL: (self.colours[Fc.F4], self.colours[Fc.L6]),
            Ed.BL: (self.colours[Fc.B6], self.colours[Fc.L4]),
            Ed.BR: (self.colours[Fc.B4], self.colours[Fc.R6]),

            # Bottom layer
            Ed.DR: (self.colours[Fc.D6], self.colours[Fc.R8]),
            Ed.DF: (self.colours[Fc.D2], self.colours[Fc.F8]),
            Ed.DL: (self.colours[Fc.D4], self.colours[Fc.L8]),
            Ed.DB: (self.colours[Fc.D8], self.colours[Fc.B8])
        }

    def _current_corners(self) -> dict[int, Corner]:
        return {
            # Top layer
            Co.URF: (self.colours[Fc.U9], self.colours[Fc.R1], self.colours[Fc.F3]),
            Co.UFL: (self.colours[Fc.U7], self.colours[Fc.F1], self.colours[Fc.L3]),
            Co.ULB: (self.colours[Fc.U1], self.colours[Fc.L1], self.colours[Fc.B3]),
            Co.UBR: (self.colours[Fc.U3], self.colours[Fc.B1], self.colours[Fc.R3]),

            # Bottom layer
            Co.DFR: (self.colours[Fc.D3], self.colours[Fc.F9], self.colours[Fc.R7]),
            Co.DLF: (self.colours[Fc.D1], self.colours[Fc.L9], self.colours[Fc.F7]),
            Co.DBL: (self.colours[Fc.D7], self.colours[Fc.B9], self.colours[Fc.L7]),
            Co.DRB: (self.colours[Fc.D9], self.colours[Fc.R9], self.colours[Fc.B7])
        }

    def _solved_edges(self) -> dict[int, Edge]:
        return {
            # Top layer
            Ed.UR: (self.colours[Fc.U5], self.colours[Fc.R5]),
            Ed.UF: (self.colours[Fc.U5], self.colours[Fc.F5]),
            Ed.UL: (self.colours[Fc.U5], self.colours[Fc.L5]),
            Ed.UB: (self.colours[Fc.U5], self.colours[Fc.B5]),

            # Middle layer
            Ed.FR: (self.colours[Fc.F5], self.colours[Fc.R5]),
            Ed.FL: (self.colours[Fc.F5], self.colours[Fc.L5]),
            Ed.BL: (self.colours[Fc.B5], self.colours[Fc.L5]),
            Ed.BR: (self.colours[Fc.B5], self.colours[Fc.R5]),

            # Bottom layer
            Ed.DR: (self.colours[Fc.D5], self.colours[Fc.R5]),
            Ed.DF: (self.colours[Fc.D5], self.colours[Fc.F5]),
            Ed.DL: (self.colours[Fc.D5], self.colours[Fc.L5]),
            Ed.DB: (self.colours[Fc.D5], self.colours[Fc.B5])
        }

    def _solved_corners(self) -> dict[int, Corner]:
        return {
            # Top layer
            Co.URF: (self.colours[Fc.U5], self.colours[Fc.R5], self.colours[Fc.F5]),
            Co.UFL: (self.colours[Fc.U5], self.colours[Fc.F5], self.colours[Fc.L5]),
            Co.ULB: (self.colours[Fc.U5], self.colours[Fc.L5], self.colours[Fc.B5]),
            Co.UBR: (self.colours[Fc.U5], self.colours[Fc.B5], self.colours[Fc.R5]),

            # Bottom layer
            Co.DFR: (self.colours[Fc.D5], self.colours[Fc.F5], self.colours[Fc.R5]),
            Co.DLF: (self.colours[Fc.D5], self.colours[Fc.L5], self.colours[Fc.F5]),
            Co.DBL: (self.colours[Fc.D5], self.colours[Fc.B5], self.colours[Fc.L5]),
            Co.DRB: (self.colours[Fc.D5], self.colours[Fc.R5], self.colours[Fc.B5])
        }

    def rotate_x_axis(self, n: int = 1):
        for move in [f'R{n}', f'M{4-n}', f'L{4-n}']:
            self.make_move(move, save=False)

    def rotate_y_axis(self, n: int = 1):
        for move in [f'U{n}', f'E{4-n}', f'D{4-n}']:
            self.make_move(move, save=False)

    def rotate_z_axis(self, n: int = 1):
        for move in [f'F{n}', f'S{n}', f'B{4-n}']:
            self.make_move(move, save=False)

    def make_move(self, move: str, save: bool = True):
        face, n = move[0], int(move[1])
        moves = self._swap_colours(face, n)

        # Slice moves
        if face == 'M':
            moves = f'L{4-n}', f'R{n}'
        elif face == 'E':
            moves = f'D{4-n}', f'U{n}'
        elif face == 'S':
            moves = f'F{4-n}', f'B{n}'

        # Wide moves
        elif face == 'u':
            self._swap_colours('E', 4-n)
        elif face == 'r':
            self._swap_colours('M', 4-n)
        elif face == 'b':
            self._swap_colours('S', 4-n)
        elif face == 'd':
            self._swap_colours('E', n)
        elif face == 'l':
            self._swap_colours('M', n)
        elif face == 'f':
            self._swap_colours('S', n)

        if save:
            for m in moves:
                self.moves.append(self.faces[m[0]] + m[1])

    def _swap_colours(self, face: str, n: int) -> tuple[str]:
        for swap in FACELET_SWAPS[face.upper()]:
            a, b, c, d = s1 = swap
            w, x, y, z = s1[-n:] + s1[:-n] # Shift elements in s1 right n places

            self.colours[a], self.colours[b], self.colours[c], self.colours[d] = \
            self.colours[w], self.colours[x], self.colours[y], self.colours[z]

        if face in FACE_SWAPS:
            a, b, c, d = s1 = FACE_SWAPS[face]
            w, x, y, z = s1[-n:] + s1[:-n] # Shift elements in s1 right n places

            self.faces[a], self.faces[b], self.faces[c], self.faces[d] = \
            self.faces[w], self.faces[x], self.faces[y], self.faces[z]

        if face.isupper():
            return f'{face}{n}',
        return f'{OPPOSITES[face.upper()]}{n}',
