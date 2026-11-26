from Kociemba.enums import Facelet as Fc

from CFOP.constants import *
from CFOP.move_manager import MoveManager
from CFOP.edge_solver import EdgeSolver
from CFOP.cube import Cube, Corner
from CFOP.cross import Cross
from CFOP.f2l import F2L
from CFOP.oll import OLL
from CFOP.pll import PLL

from collections import Counter
import time


class Solver:

    def __init__(self):
        self.cross = Cross()
        self.f2l = F2L()
        self.oll = OLL()
        self.pll = PLL()

    def solve(self, colours: list[int]) -> list[str]:
        t = time.time()

        faces = {f: f for f in 'URFDLB'}
        cubes = self.cross.solve_cross(Cube(colours, faces, []))
        cubes = self._get_best_cubes(cubes, *NUM_CUBES_CROSS)

        # Rotate cubes upside down
        for cube in cubes:
            cube.rotate_z_axis(2)

        cubes = self.f2l.solve_F2L(cubes)
        cubes = self._get_best_cubes(cubes, NUM_CUBES_F2L)

        self.oll.solve_OLL(cubes)
        self.pll.solve_PLL(cubes)

        moves = self._get_best_cubes(cubes, 1)[0].moves

        print(f'{len(moves)} moves in {round(time.time()-t, 2)} seconds')
        for i in range(0, len(moves), 10):
            print(moves[i : i + 10])
        print()

        return moves[::-1]

    def _get_best_cubes(self, cubes: list[Cube], n: int, m: int = 0) -> list[Cube]:
        """
        Return a list of m+n cubes.
        m cubes have U moves, n cubes have no U moves.
        """
        if m == 0:
            return self._sort_and_dedupe(cubes, n)

        # Split cubes into two lists
        cubes_u: list[Cube] = [] # Cubes with U moves
        cubes_x: list[Cube] = [] # Cubes without U moves

        for cube in cubes:
            u = any(moves[0] == 'U' for moves in cube.moves)
            cubes_u.append(cube) if u else cubes_x.append(cube)

        # Return m cubes with U moves, n cubes without U moves
        return self._sort_and_dedupe(cubes_u, m) \
             + self._sort_and_dedupe(cubes_x, n)

    def _sort_and_dedupe(self, cubes: list[Cube], n: int) -> list[Cube]:
        for cube in cubes:
            cube.moves = MoveManager.replace_u_moves(cube.moves)
            cube.moves = MoveManager.reduce_moves(cube.moves)

        # Sort by number of moves
        cubes = sorted(cubes, key=lambda cube: len(cube.moves))

        # Remove duplicates (cubes with the same moves)
        seen = set()
        deduped_cubes = []

        for cube in cubes:
            moves = tuple(cube.moves)
            if moves not in seen:
                seen.add(moves)
                deduped_cubes.append(cube)
            if len(deduped_cubes) == n:
                break

        return deduped_cubes

    ### Methods for checking if cube is solvable ###

    def solvable(self, colours: list[int]) -> bool:
        cube = Cube(colours, {f: f for f in 'URFDLB'}, [])

        return self._count_colours(cube) \
           and self._corners_valid(cube) \
           and self._edges_valid(cube) \
           and self._even_swaps() \

    def _count_colours(self, cube: Cube) -> bool:
        counts = Counter(cube.colours)
        return all(counts[i] == 9 for i in range(6))

    def _corners_valid(self, cube: Cube) -> bool:
        self.c_dict = {}
        for i in range(8):
            j = cube.find_corner(i)
            if j is None:
                return False

            a = cube._solved_corners()[i]
            b = cube._current_corners()[j]
            if not self._can_rotate_to(a, b):
                return False

            self.c_dict[i] = j
        return self._sum_corners(cube) % 3 == 0

    def _can_rotate_to(self, a: Corner, b: Corner) -> bool:
        for _ in range(3):
            if a == b:
                return True
            a = (a[1], a[2], a[0])
        return False

    def _sum_corners(self, cube: Cube) -> int:
        sum_corners = 0
        colours = [cube.colours[Fc.U5], cube.colours[Fc.D5]]
        for _ in range(4):
            if cube.colours[Fc.R1] in colours:
                sum_corners += 1
            if cube.colours[Fc.F3] in colours:
                sum_corners += 2
            if cube.colours[Fc.F9] in colours:
                sum_corners += 1
            if cube.colours[Fc.R7] in colours:
                sum_corners += 2
            cube.rotate_y_axis()
        return sum_corners

    def _edges_valid(self, cube: Cube) -> bool:
        self.e_dict = {}
        flips = 0
        for i in range(12):
            j = cube.find_edge(i)
            if j is None:
                return False
            flips += self._path_exists(cube, j, i)
            self.e_dict[i] = j
        return flips % 2 == 0

    def _path_exists(self, cube: Cube, start: int, final: int) -> int:
        return len(EdgeSolver.find_paths(
            cube=cube,
            find_one=True,
            start_node=start,
            final_node=final,
            move_limit=2,
            prohibited={F, Fi, B, Bi}
        ))

    def _even_swaps(self) -> bool:
        swaps = self._count_swaps(self.e_dict) \
              + self._count_swaps(self.c_dict)
        return swaps % 2 == 0

    def _count_swaps(self, d: dict) -> int:
        for i, j in d.items():
            if i == j:
                continue
            d[i], d[j] = d[j], d[i]
            return 1 + self._count_swaps(d)
        return 0
