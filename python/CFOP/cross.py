from Kociemba.enums import Edge as Ed, Facelet as Fc
from CFOP.edge_solver import EdgeSolver
from CFOP.constants import *
from CFOP.cube import Cube
import itertools


class Cross:

    def __init__(self, max_solves: int = MAX_SOLVE_CROSS):
        self.max_solves = max_solves

    def solve_cross(self, cube: Cube) -> list[Cube]:
        self.solved_cubes: list[Cube] = []
        self.solved_count = 0

        colours = [cube.colours[i] for i in (Fc.B5, Fc.L5, Fc.R5, Fc.F5)]
        for permutation in itertools.permutations(colours):
            self._solve_cross_recursively(cube.spawn_child(), permutation)

        return self.solved_cubes

    def _solve_cross_recursively(self, cube: Cube, colours: list[int], depth: int = 0):
        if self.solved_count >= self.max_solves:
            return
        if depth == len(colours):
            self.solved_cubes.append(cube)
            self.solved_count += 1
            return

        for cube in self._get_cubes_with_solved_edge(cube, colours[depth]):
            self._solve_cross_recursively(cube, colours, depth + 1)

    def _get_cubes_with_solved_edge(self, cube: Cube, colour: int) -> list[Cube]:
        cubes: list[Cube] = []

        # Rotate cube so correct face is in front
        while cube.colours[Fc.F5] != colour:
            cube.rotate_y_axis()

        # If edge already solved
        if cube.edge_solved(Ed.UF):
            return [cube]

        # Locate edge
        start = cube.find_edge(Ed.UF)

        paths = self._get_paths_that_keep_cross(cube, start) \
             or self._get_paths_that_undo_cross(cube, start)

        for path in paths:
            child = cube.spawn_child()
            for move in path:
                child.make_move(move)
            cubes.append(child)

        return cubes

    def _get_paths_that_keep_cross(self, cube: Cube, start: int) -> list[tuple[str, ...]]:
        prohibited = set()

        if cube.edge_solved(Ed.UR):
            prohibited |= {R, R2, Ri}
        if cube.edge_solved(Ed.UB):
            prohibited |= {B, B2, Bi}
        if cube.edge_solved(Ed.UL):
            prohibited |= {L, L2, Li}
        if prohibited:
            prohibited |= {U, U2, Ui}

        return self._find_paths(cube, start, 3, prohibited) \
            or self._find_paths(cube, start, 4, prohibited)

    def _get_paths_that_undo_cross(self, cube: Cube, start: int) -> list[tuple[str, ...]]:
        # These paths undo the cross to solve an edge then fix the cross
        if start == Ed.UF:
            return [(Fi, L, D, Li, F2), (F, Ri, Di, R, F2), (Fi, U, Li, Ui), (F, Ui, R, U)]
        elif start == Ed.UB:
            return [(B2, Di, R, Fi, Ri), (B2, D, Li, F, L)]
        elif start == Ed.FL:
            return [(L, D, Li, F2), (U, Li, Ui)]
        elif start == Ed.FR:
            return [(Ri, Di, R, F2), (Ui, R, U)]
        elif start == Ed.BR and cube.colours[Fc.B4] == cube.colours[Fc.U5]:
            return [(R, Di, Ri, F2), (R, Di, F2, Ri), (Ui, Ri, U)]
        elif start == Ed.BR and cube.colours[Fc.R6] == cube.colours[Fc.U5]:
            return [(R2, Fi, R2), (Bi, D2, F2, B)]
        elif start == Ed.BL and cube.colours[Fc.B6] == cube.colours[Fc.U5]:
            return [(Li, D, L, F2), (Li, D, F2, L), (U, L, Ui)]
        elif start == Ed.BL and cube.colours[Fc.L4] == cube.colours[Fc.U5]:
            return [(L2, F, L2), (B, D2, F2, Bi)]
        elif start == Ed.DF:
            return [(D, R, Fi, Ri), (Di, Li, F, L)]
        elif start == Ed.DR:
            return [(R, Fi, Ri)]
        elif start == Ed.DB:
            return [(Di, R, Fi, Ri), (D, Li, F, L)]
        elif start == Ed.DL:
            return [(Li, F, L)]

    def _find_paths(self, cube: Cube, start: int, limit: int, prohibited: set[str]) -> list[tuple[str, ...]]:
        return EdgeSolver.find_paths(
            cube=cube,
            find_one=False,
            start_node=start,
            final_node=Ed.UF,
            move_limit=limit,
            prohibited=prohibited,
        )
