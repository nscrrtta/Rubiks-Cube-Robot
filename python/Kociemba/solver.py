from collections import Counter
from Kociemba.solver_thread import SolverThread
from Kociemba.constants import *
from Kociemba.cube import Cube
import threading as thr
import time


class Solver:

    def solve(self, colours: list[int], max_length: int = 22, timeout: int = 3) -> list[str]:
        t = time.time()

        colours = self._rotate_x_axis(colours)
        colours = self._translate_colours(colours)
        cube = self._list_to_cube(colours)

        # These mutable variables are modified by all threads
        solutions: list[list[str]] = []
        terminated = thr.Event()
        terminated.clear()

        threads: list[thr.Thread] = []
        for i in range(4):
            thread = SolverThread(cube, i, timeout, max_length, solutions, terminated, [999])
            threads.append(thread)
            thread.start()

        # Wait until all threads have finished
        for thread in threads:
            thread.join()

        moves = solutions[-1] if solutions else []
        moves = self._translate_moves(moves)

        print(f'{len(moves)} moves in {round(time.time()-t, 2)} seconds')
        for i in range(0, len(moves), 10): print(moves[i : i + 10])
        print()

        return moves[::-1]

    def solvable(self, colours: list[int]) -> bool:
        counts = Counter(colours)
        if any(counts[i] != 9 for i in range(6)):
            return False

        colours = self._translate_colours(colours)
        cube = self._list_to_cube(colours)

        if set(cube.ep) != set(range(12)):
            return False

        if sum(cube.eo) % 2 != 0:
            return False

        if set(cube.cp) != set(range(8)):
            return False

        if sum(cube.co) % 3 != 0:
            return False

        edge_parity = 0
        for i in range(11, 0, -1):
            for j in range(i - 1, -1, -1):
                if cube.ep[j] > cube.ep[i]:
                    edge_parity += 1

        corner_parity = 0
        for i in range(7, 0, -1):
            for j in range(i - 1, -1, -1):
                if cube.cp[j] > cube.cp[i]:
                    corner_parity += 1

        return (edge_parity % 2) == (corner_parity % 2)

    def _rotate_x_axis(self, colours: list[int]) -> list[int]:
        """
        Kociemba 5-face solver excludes B moves.
        Rotate cube about x axis so U face becomes B face.
        """
        indices = [
            Fc.F1, Fc.F2, Fc.F3, Fc.F4, Fc.F5, Fc.F6, Fc.F7, Fc.F8, Fc.F9,
            Fc.R7, Fc.R4, Fc.R1, Fc.R8, Fc.R5, Fc.R2, Fc.R9, Fc.R6, Fc.R3,
            Fc.D1, Fc.D2, Fc.D3, Fc.D4, Fc.D5, Fc.D6, Fc.D7, Fc.D8, Fc.D9,
            Fc.B9, Fc.B8, Fc.B7, Fc.B6, Fc.B5, Fc.B4, Fc.B3, Fc.B2, Fc.B1,
            Fc.L3, Fc.L6, Fc.L9, Fc.L2, Fc.L5, Fc.L8, Fc.L1, Fc.L4, Fc.L7,
            Fc.U9, Fc.U8, Fc.U7, Fc.U6, Fc.U5, Fc.U4, Fc.U3, Fc.U2, Fc.U1
        ]
        return [colours[i] for i in indices]

    def _translate_colours(self, colours: list[int]) -> list[int]:
        # Define colour of each face by looking at centers
        colour_dict = {
            colours[Fc.U5]: Cl.U,
            colours[Fc.R5]: Cl.R,
            colours[Fc.F5]: Cl.F,
            colours[Fc.D5]: Cl.D,
            colours[Fc.L5]: Cl.L,
            colours[Fc.B5]: Cl.B

        }
        return [colour_dict[s].value for s in colours]

    def _translate_moves(self, moves: list[str]) -> list[str]:
        """
        Because the cube was rotated prior to being solved,
        some moves need to be translated.

        L and R moves stay the same, F, U, D moves change
        (There shouldn't be any B moves).
        """
        translations = {'L':'L', 'R':'R', 'U':'F', 'F':'D', 'D':'B'}
        return [translations[m[0]] + m[1] for m in moves]

    def _list_to_cube(self, colours: list[int]) -> Cube:
        cube = Cube()

        # Invalidate corner and edge permutation
        cube.cp = [-1] * 8
        cube.ep = [-1] * 12

        for i, facelet in enumerate(CORNER_FACELETS):
            # Facelets of corner at position i
            corner = [colours[f] for f in facelet]

            for j, vals in enumerate(CORNER_COLORS):
                if vals[0] not in corner:
                    continue

                k = corner.index(vals[0])
                col1 = corner[(k + 1) % 3]
                col2 = corner[(k + 2) % 3]

                if col1 == vals[1] and col2 == vals[2]:
                    # Corner j is in corner position i
                    cube.cp[i] = j
                    cube.co[i] = k
                    break

        for i, facelets in enumerate(EDGE_FACELETS):
            # Facelets of edge at position i
            edge = [colours[f] for f in facelets]

            for j, vals in enumerate(EDGE_COLORS):
                if vals[0] not in edge:
                    continue

                k = edge.index(vals[0])
                col1 = edge[(k + 1) % 2]

                if col1 == vals[1]:
                    # Edge j is in edge position i
                    cube.ep[i] = j
                    cube.eo[i] = k
                    break

        return cube
