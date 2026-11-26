from Kociemba.enums import Corner as Co, Edge as Ed, Facelet as Fc
from CFOP.constants import *
from CFOP.cube import Cube
import itertools


class F2L:

    def __init__(self, max_solves: int = MAX_SOLVE_F2L):
        self.max_solves = max_solves

    def solve_F2L(self, cubes: list[Cube]) -> list[Cube]:
        self.solved_cubes: list[Cube] = []

        for cube in cubes:
            self.solved_count = 0
            colours = [cube.colours[i] for i in (Fc.B5, Fc.L5, Fc.R5, Fc.F5)]
            for permutation in itertools.permutations(colours):
                self._solve_F2L_recursively(cube.spawn_child(), permutation)

        return self.solved_cubes

    def _solve_F2L_recursively(self, cube: Cube, colours: list[int], depth: int = 0):
        if self.solved_count >= self.max_solves:
            return
        if depth == len(colours):
            self.solved_cubes.append(cube)
            self.solved_count += 1
            return

        for cube in self._get_cubes_with_solved_pair(cube, colours[depth]):
            self._solve_F2L_recursively(cube, colours, depth + 1)

    def _get_cubes_with_solved_pair(self, cube: Cube, colour: int) -> list[Cube]:
        cubes: list[Cube] = []

        # Rotate cube so correct face is in front
        while cube.colours[Fc.F5] != colour:
            cube.rotate_y_axis()

        # If pair already solved
        if cube.corner_solved(Co.DFR) and cube.edge_solved(Ed.FR):
            return [cube]

        # Locate corner and edge
        crnr_node = cube.find_corner(Co.DFR)
        edge_node = cube.find_edge(Ed.FR)

        # Rotate cube so corner is URF or DFR
        i = (4 - crnr_node) % 4
        if i > 0: cube.rotate_y_axis(i)

        # Update corner node and edge node after rotating cube
        crnr_node = (crnr_node // 4) * 4
        edge_node = (edge_node // 4) * 4 + (edge_node + i) % 4

        if crnr_node == Co.URF:
            paths = self._get_paths_URF(cube, edge_node)
        elif crnr_node == Co.DFR:
            paths = self._get_paths_DFR(cube, edge_node)

        for path in paths:
            child = cube.spawn_child()
            for move in path:
                child.make_move(move)
            cubes.extend(self._get_cubes_with_solved_pair(child, colour))

        return cubes

    def _get_paths_URF(self, cube: Cube, edge_node: int) -> list[list[str]]:
        paths: list[list[str]] = []

        if edge_node == Ed.UF:
            # White faces up
            if cube.colours[Fc.U9] == cube.colours[Fc.D5]:

                # Front-facing colours are the same
                if cube.colours[Fc.F2] == cube.colours[Fc.F3]:
                    if not (cube.corner_solved(Co.DLF) and cube.edge_solved(Ed.FL)):
                        paths.extend([[U2, Li, U, L, Ui, F, Ui, Fi], [U2, Li, Ui, L, Ui, F, Ui, Fi]])
                    if not (cube.corner_solved(Co.DFR) and cube.edge_solved(Ed.FR)):
                        paths.extend([[U, Fi, U, F, Ui, R, Ui, Ri], [U, Fi, Ui, F, Ui, R, Ui, Ri]])
                    if not (cube.corner_solved(Co.DRB) and cube.edge_solved(Ed.BR)):
                        paths.extend([[Ri, U, R, Ui, B, Ui, Bi], [Ri, Ui, R, Ui, B, Ui, Bi]])
                    if not (cube.corner_solved(Co.DBL) and cube.edge_solved(Ed.BL)):
                        paths.extend([[Ui, Bi, U, B, Ui, L, Ui, Li], [Ui, Bi, Ui, B, Ui, L, Ui, Li]])

                # Front-facing colours are different
                else:
                    if not (cube.corner_solved(Co.DLF) and cube.edge_solved(Ed.FL)):
                        paths.append([U, Li, U2, L])
                    if not (cube.corner_solved(Co.DFR) and cube.edge_solved(Ed.FR)):
                        paths.append([Fi, U2, F])
                    if not (cube.corner_solved(Co.DRB) and cube.edge_solved(Ed.BR)):
                        paths.append([Ui, Ri, U2, R])
                    if not (cube.corner_solved(Co.DBL) and cube.edge_solved(Ed.BL)):
                        paths.append([U2, Bi, U2, B])

            # White faces right
            elif cube.colours[Fc.R1] == cube.colours[Fc.D5]:

                # Front-facing colours are different
                if cube.colours[Fc.F2] != cube.colours[Fc.F3]:
                    if not (cube.corner_solved(Co.DLF) and cube.edge_solved(Ed.FL)):
                        paths.append([U2, Li, U2, L])
                    if not (cube.corner_solved(Co.DFR) and cube.edge_solved(Ed.FR)):
                        paths.append([U, Fi, U2, F])
                    if not (cube.corner_solved(Co.DRB) and cube.edge_solved(Ed.BR)):
                        paths.append([Ri, U2, R])
                    if not (cube.corner_solved(Co.DBL) and cube.edge_solved(Ed.BL)):
                        paths.append([Ui, Bi, U2, B])

                # Front-facing colours are the same
                elif cube.colours[Fc.F2] == cube.colours[Fc.F5]:
                    paths = [[Ui, Fi, U, F]]
                elif cube.colours[Fc.F2] == cube.colours[Fc.R5]:
                    paths = [[U, Ri, U2, R]]
                elif cube.colours[Fc.F2] == cube.colours[Fc.L5]:
                    paths = [[Li, U, L]]
                elif cube.colours[Fc.F2] == cube.colours[Fc.B5]:
                    paths = [[U, Bi, U, B], [Bi, U2, B]]

            # White faces front
            elif cube.colours[Fc.F3] == cube.colours[Fc.D5]:

                first_move = [Ui] if cube.colours[Fc.U6] == cube.colours[Fc.U9] else []

                if not (cube.corner_solved(Co.DLF) and cube.edge_solved(Ed.FL)):
                    paths.append(first_move + [U2, Li, U, L])
                if not (cube.corner_solved(Co.DFR) and cube.edge_solved(Ed.FR)):
                    paths.append(first_move + [U, Fi, U, F])
                if not (cube.corner_solved(Co.DRB) and cube.edge_solved(Ed.BR)):
                    paths.append(first_move + [Ri, U, R])
                if not (cube.corner_solved(Co.DBL) and cube.edge_solved(Ed.BL)):
                    paths.append(first_move + [Ui, Bi, U, B])

        elif edge_node == Ed.UR:
            # White faces up
            if cube.colours[Fc.U9] == cube.colours[Fc.D5]:

                # Right-facing colours are the same
                if cube.colours[Fc.R2] == cube.colours[Fc.R1]:
                    if not (cube.corner_solved(Co.DLF) and cube.edge_solved(Ed.FL)):
                        paths.extend([[F, Ui, Fi, U, Li, U, L], [F, U, Fi, U, Li, U, L]])
                    if not (cube.corner_solved(Co.DFR) and cube.edge_solved(Ed.FR)):
                        paths.extend([[Ui, R, Ui, Ri, U, Fi, U, F], [Ui, R, U, Ri, U, Fi, U, F]])
                    if not (cube.corner_solved(Co.DRB) and cube.edge_solved(Ed.BR)):
                        paths.extend([[U2, B, Ui, Bi, U, Ri, U, R], [U2, B, U, Bi, U, Ri, U, R]])
                    if not (cube.corner_solved(Co.DBL) and cube.edge_solved(Ed.BL)):
                        paths.extend([[U, L, Ui, Li, U, Bi, U, B], [U, L, U, Li, U, Bi, U, B]])

                # Right-facing colours are different
                else:
                    if not (cube.corner_solved(Co.DLF) and cube.edge_solved(Ed.FL)):
                        paths.append([U, F, U2, Fi])
                    if not (cube.corner_solved(Co.DFR) and cube.edge_solved(Ed.FR)):
                        paths.append([R, U2, Ri])
                    if not (cube.corner_solved(Co.DRB) and cube.edge_solved(Ed.BR)):
                        paths.append([Ui, B, U2, Bi])
                    if not (cube.corner_solved(Co.DBL) and cube.edge_solved(Ed.BL)):
                        paths.append([U2, L, U2, Li])

            # White faces right
            elif cube.colours[Fc.R1] == cube.colours[Fc.D5]:

                first_move = [U] if cube.colours[Fc.U6] == cube.colours[Fc.U9] else []

                if not (cube.corner_solved(Co.DLF) and cube.edge_solved(Ed.FL)):
                    paths.append(first_move + [F, Ui, Fi])
                if not (cube.corner_solved(Co.DFR) and cube.edge_solved(Ed.FR)):
                    paths.append(first_move + [Ui, R, Ui, Ri])
                if not (cube.corner_solved(Co.DRB) and cube.edge_solved(Ed.BR)):
                    paths.append(first_move + [U2, B, Ui, Bi])
                if not (cube.corner_solved(Co.DBL) and cube.edge_solved(Ed.BL)):
                    paths.append(first_move + [U, L, Ui, Li])

            # White faces front
            elif cube.colours[Fc.F3] == cube.colours[Fc.D5]:

                # Right-facing colours are different
                if cube.colours[Fc.R2] != cube.colours[Fc.R1]:
                    if not (cube.corner_solved(Co.DLF) and cube.edge_solved(Ed.FL)):
                        paths.append([F, U2, Fi])
                    if not (cube.corner_solved(Co.DFR) and cube.edge_solved(Ed.FR)):
                        paths.append([Ui, R, U2, Ri])
                    if not (cube.corner_solved(Co.DRB) and cube.edge_solved(Ed.BR)):
                        paths.append([U2, B, U2, Bi])
                    if not (cube.corner_solved(Co.DBL) and cube.edge_solved(Ed.BL)):
                        paths.append([U, L, U2, Li])

                # Right-facing colours are the same -> solve pair
                elif cube.colours[Fc.R2] == cube.colours[Fc.F5]:
                    paths = [[U2, F, Ui, Fi]]
                elif cube.colours[Fc.R2] == cube.colours[Fc.R5]:
                    paths = [[U, R, Ui, Ri]]
                elif cube.colours[Fc.R2] == cube.colours[Fc.L5]:
                    paths = [[Ui, L, Ui, Li], [L, U2, Li]]
                elif cube.colours[Fc.R2] == cube.colours[Fc.B5]:
                    paths = [[B, Ui, Bi]]

        elif edge_node == Ed.UB:
            # White faces up
            if cube.colours[Fc.U9] == cube.colours[Fc.D5]:

                # Front-facing and up-facing colours are the same
                if cube.colours[Fc.U2] == cube.colours[Fc.F3]:
                    if not (cube.corner_solved(Co.DLF) and cube.edge_solved(Ed.FL)):
                        paths.append([U, Li, U, L])
                    if not (cube.corner_solved(Co.DFR) and cube.edge_solved(Ed.FR)):
                        paths.append([Fi, U, F])
                    if not (cube.corner_solved(Co.DRB) and cube.edge_solved(Ed.BR)):
                        paths.append([Ui, Ri, U, R])
                    if not (cube.corner_solved(Co.DBL) and cube.edge_solved(Ed.BL)):
                        paths.append([U2, Bi, U, B])

                # Front-facing and up-facing colours are different -> solve pair
                elif cube.colours[Fc.B2] == cube.colours[Fc.F5]:
                    paths = [[U2, F, U2, Fi, U, F, Ui, Fi]]
                elif cube.colours[Fc.B2] == cube.colours[Fc.R5]:
                    paths = [[U, R, U2, Ri, U, R, Ui, Ri]]
                elif cube.colours[Fc.B2] == cube.colours[Fc.L5]:
                    paths = [[Ui, L, U2, Li, U, L, Ui, Li]]
                elif cube.colours[Fc.B2] == cube.colours[Fc.B5]:
                    paths = [[B, U2, Bi, U, B, Ui, Bi]]

            # White faces right
            elif cube.colours[Fc.R1] == cube.colours[Fc.D5]:

                # Top-facing colours are the same
                if cube.colours[Fc.U2] == cube.colours[Fc.U9]:
                    if not (cube.corner_solved(Co.DLF) and cube.edge_solved(Ed.FL)):
                        paths.append([U2, Li, U2, L])
                    if not (cube.corner_solved(Co.DFR) and cube.edge_solved(Ed.FR)):
                        paths.append([U, Fi, U2, F])
                    if not (cube.corner_solved(Co.DRB) and cube.edge_solved(Ed.BR)):
                        paths.append([Ri, U2, R])
                    if not (cube.corner_solved(Co.DBL) and cube.edge_solved(Ed.BL)):
                        paths.append([Ui, Bi, U2, B])

                # Top-facing colours are different -> solve pair
                elif cube.colours[Fc.F3] == cube.colours[Fc.F5]:
                    paths = [[R, U, Ri]]
                elif cube.colours[Fc.F3] == cube.colours[Fc.R5]:
                    paths = [[Ui, B, U, Bi]]
                elif cube.colours[Fc.F3] == cube.colours[Fc.L5]:
                    paths = [[U, F, U, Fi]]
                elif cube.colours[Fc.F3] == cube.colours[Fc.B5]:
                    paths = [[U2, L, U, Li]]

            # White faces front
            elif cube.colours[Fc.F3] == cube.colours[Fc.D5]:

                u_move = U if cube.colours[Fc.U2] == cube.colours[Fc.U9] else Ui

                if not (cube.corner_solved(Co.DLF) and cube.edge_solved(Ed.FL)):
                    paths.append([F, u_move, Fi])
                if not (cube.corner_solved(Co.DFR) and cube.edge_solved(Ed.FR)):
                    paths.append([Ui, R, u_move, Ri])
                if not (cube.corner_solved(Co.DRB) and cube.edge_solved(Ed.BR)):
                    paths.append([U2, B, u_move, Bi])
                if not (cube.corner_solved(Co.DBL) and cube.edge_solved(Ed.BL)):
                    paths.append([Ui, L, u_move, Li])

        elif edge_node == Ed.UL:
            # White faces up
            if cube.colours[Fc.U9] == cube.colours[Fc.D5]:

                # Front-facing and up-facing colours are different
                if cube.colours[Fc.U4] != cube.colours[Fc.F3]:
                    if not (cube.corner_solved(Co.DLF) and cube.edge_solved(Ed.FL)):
                        paths.append([U, F, Ui, Fi])
                    if not (cube.corner_solved(Co.DFR) and cube.edge_solved(Ed.FR)):
                        paths.append([R, Ui, Ri])
                    if not (cube.corner_solved(Co.DRB) and cube.edge_solved(Ed.BR)):
                        paths.append([Ui, B, Ui, Bi])
                    if not (cube.corner_solved(Co.DBL) and cube.edge_solved(Ed.BL)):
                        paths.append([U2, L, Ui, Li])

                # Front-facing and up-facing colours are the same -> solve pair
                elif cube.colours[Fc.L2] == cube.colours[Fc.F5]:
                    paths = [[Ui, Fi, U2, F, Ui, Fi, U, F]]
                elif cube.colours[Fc.L2] == cube.colours[Fc.R5]:
                    paths = [[U2, Ri, U2, R, Ui, Ri, U, R]]
                elif cube.colours[Fc.L2] == cube.colours[Fc.L5]:
                    paths = [[Li, U2, L, Ui, Li, U, L]]
                elif cube.colours[Fc.L2] == cube.colours[Fc.B5]:
                    paths = [[U, Bi, U2, B, Ui, Bi, U, B]]

            # White faces right
            elif cube.colours[Fc.R1] == cube.colours[Fc.D5]:

                u_move = Ui if cube.colours[Fc.U4] == cube.colours[Fc.U9] else U

                if not (cube.corner_solved(Co.DLF) and cube.edge_solved(Ed.FL)):
                    paths.append([U2, Li, u_move, L])
                if not (cube.corner_solved(Co.DFR) and cube.edge_solved(Ed.FR)):
                    paths.append([U, Fi, u_move, F])
                if not (cube.corner_solved(Co.DRB) and cube.edge_solved(Ed.BR)):
                    paths.append([Ri, u_move, R])
                if not (cube.corner_solved(Co.DBL) and cube.edge_solved(Ed.BL)):
                    paths.append([U, Bi, u_move, B])

            # White faces front
            elif cube.colours[Fc.F3] == cube.colours[Fc.D5]:

                # Top-facing colours are the same
                if cube.colours[Fc.U4] == cube.colours[Fc.U9]:
                    if not (cube.corner_solved(Co.DLF) and cube.edge_solved(Ed.FL)):
                        paths.append([F, U2, Fi])
                    if not (cube.corner_solved(Co.DFR) and cube.edge_solved(Ed.FR)):
                        paths.append([Ui, R, U2, Ri])
                    if not (cube.corner_solved(Co.DRB) and cube.edge_solved(Ed.BR)):
                        paths.append([U2, B, U2, Bi])
                    if not (cube.corner_solved(Co.DBL) and cube.edge_solved(Ed.BL)):
                        paths.append([U, L, U2, Li])

                # Top-facing colours are different -> solve pair
                elif cube.colours[Fc.U9] == cube.colours[Fc.F5]:
                    paths = [[Fi, Ui, F]]
                elif cube.colours[Fc.U9] == cube.colours[Fc.R5]:
                    paths = [[Ui, Ri, Ui, R]]
                elif cube.colours[Fc.U9] == cube.colours[Fc.L5]:
                    paths = [[U, Li, Ui, L]]
                elif cube.colours[Fc.U9] == cube.colours[Fc.B5]:
                    paths = [[U2, Bi, Ui, B]]

        elif edge_node == Ed.FL:
            # White faces up
            if cube.colours[Fc.U9] == cube.colours[Fc.D5]:
                # Front-facing colours are the same
                if cube.colours[Fc.F3] == cube.colours[Fc.F4]:
                    paths = [[L, Fi, Li, F]]
                # Front-facing colours are different
                else: paths = [[U, F, Ui, Fi], [U, Li, U, L]]

            # White faces right
            elif cube.colours[Fc.R1] == cube.colours[Fc.D5]:
                # Front-facing colours are the same
                if cube.colours[Fc.F3] == cube.colours[Fc.F4]:
                    paths = [[Ui, Li, U, L]]
                # Front-facing colours are different
                else: paths = [[F, U2, Fi]]

            # White faces front
            elif cube.colours[Fc.F3] == cube.colours[Fc.D5]:
                # Top-facing and front-facing colours are the same
                if cube.colours[Fc.U9] == cube.colours[Fc.F4]:
                    paths = [[F, U, Fi]]
                # Top-facing and front-facing colours are different
                else: paths = [[Li, Ui, L]]

        elif edge_node == Ed.FR:
            # White faces up
            if cube.colours[Fc.U9] == cube.colours[Fc.D5]:
                # Front-facing colours are the same
                if cube.colours[Fc.F3] == cube.colours[Fc.F6]:
                    paths = [[R, Ui, Ri], [Fi, U, F]]
                # Front-facing colours are different
                else: paths = [[U, Ri, F, R, Fi], [Ui, F, Ri, Fi, R]]

            # White faces right
            elif cube.colours[Fc.R1] == cube.colours[Fc.D5]:
                # Front-facing colours are the same
                if cube.colours[Fc.F3] == cube.colours[Fc.F6]:
                    paths = [[U, R, U, Ri], [U, Fi, U, F]]
                # Front-facing colours are different
                else: paths = [[U, Fi, Ui, F]]

            # White faces front
            elif cube.colours[Fc.F3] == cube.colours[Fc.D5]:
                # Right-facing colours are the same
                if cube.colours[Fc.R1] == cube.colours[Fc.R4]:
                    paths = [[Ui, Fi, Ui, F]]
                # Right-facing colours are different
                else: paths = [[Ui, R, U, Ri]]

        elif edge_node == Ed.BR:
            # White faces up
            if cube.colours[Fc.U9] == cube.colours[Fc.D5]:
                # Right-facing colours are the same
                if cube.colours[Fc.R1] == cube.colours[Fc.R6]:
                    paths = [[Bi, R, B, Ri]]
                # Right-facing colours are different
                else: paths = [[Ui, Ri, U, R]]

            # White faces right
            elif cube.colours[Fc.R1] == cube.colours[Fc.D5]:
                # Front-facing and right-facing colours are the same
                if cube.colours[Fc.F3] == cube.colours[Fc.R6]:
                    paths = [[B, U, Bi]]
                # Front-facing and right-facing colours are different
                else: paths = [[Ri, Ui, R]]

            # White faces front
            elif cube.colours[Fc.F3] == cube.colours[Fc.D5]:
                # Right-facing colours are the same
                if cube.colours[Fc.R1] == cube.colours[Fc.R6]:
                    paths = [[U, B, Ui, Bi]]
                # Right-facing colours are different
                else: paths = [[Ri, U2, R]]

        elif edge_node == Ed.BL:
            # White faces up
            if cube.colours[Fc.U9] == cube.colours[Fc.D5]:
                # Front-facing and back-facing colours are the same
                if cube.colours[Fc.F3] == cube.colours[Fc.B6]:
                    paths = [[U2, L, Ui, Li], [U2, Bi, U, B]]
                # Front-facing and back-facing colours are different
                else: paths = [[U, B, Li, Bi, L], [Ui, Li, B, L, Bi]]

            # White faces right
            elif cube.colours[Fc.R1] == cube.colours[Fc.D5]:
                # Front-facing and back-facing colours are the same
                if cube.colours[Fc.F3] == cube.colours[Fc.B6]:
                    paths = [[Ui, L, U, Li]]
                # Front-facing and back-facing colours are different
                else: paths = [[Bi, U, B]]

            # White faces front
            elif cube.colours[Fc.F3] == cube.colours[Fc.D5]:
                # Right-facing and left-facing colours are the same
                if cube.colours[Fc.R1] == cube.colours[Fc.L4]:
                    paths = [[U, Bi, Ui, B]]
                # Right-facing and left-facing colours are different
                else: paths = [[L, Ui, Li]]

        return paths

    def _get_paths_DFR(self, cube: Cube, edge_node: int) -> list[list[str]]:
        paths: list[list[str]] = []

        if edge_node == Ed.UF:
            # White faces down
            if cube.colours[Fc.D3] == cube.colours[Fc.D5]:
                # Front-facing colours are the same
                if cube.colours[Fc.F9] == cube.colours[Fc.F2]:
                    paths = [[U, R, Ui, Ri], [U, R, U, Ri]]
                # Front-facing colours are different
                else: paths = [[Fi, U2, F]]

            # White faces right
            elif cube.colours[Fc.R7] == cube.colours[Fc.D5]:
                # Front-facing colours are the same
                if cube.colours[Fc.F9] == cube.colours[Fc.F2]:
                    paths = [[U, Fi, U, F], [Ui, R, U, Ri]]
                # Front-facing colours are different -> solve pair
                elif cube.colours[Fc.F2] == cube.colours[Fc.L5]:
                    paths = [[R, Li, U, L, Ri]]
                # Right-facing colours are different -> don't solve pair
                else: paths = [[R, U, Ri]]

            # White faces front
            elif cube.colours[Fc.F9] == cube.colours[Fc.D5]:
                # Right-facing and front-facing colours are the same
                if cube.colours[Fc.R7] == cube.colours[Fc.F2]:
                    paths = [[Fi, Ui, F]]
                # Right-facing and front-facing colours are different
                else: paths = [[Ui]]

        elif edge_node == Ed.UR:
            # White faces down
            if cube.colours[Fc.D3] == cube.colours[Fc.D5]:
                # Right-facing colours are the same
                if cube.colours[Fc.R7] == cube.colours[Fc.R2]:
                    paths = [[Ui, Fi, U, F], [Ui, Fi, Ui, F]]
                # Right-facing colours are different
                else: paths = [[R, U2, Ri]]

            # White faces right
            elif cube.colours[Fc.R7] == cube.colours[Fc.D5]:
                # Front-facing and top-facing colours are the same
                if cube.colours[Fc.F9] == cube.colours[Fc.U6]:
                    paths = [[U]]
                # Front-facing and top-facing colours are different
                else: paths = [[R, U, Ri]]

            # White faces front
            elif cube.colours[Fc.F9] == cube.colours[Fc.D5]:
                # Right-facing colours are the same
                if cube.colours[Fc.R7] == cube.colours[Fc.R2]:
                    paths = [[Ui, R, Ui, Ri], [U, Fi, Ui, F]]
                # Right-facing colours are different -> solve pair
                elif cube.colours[Fc.R2] == cube.colours[Fc.B5]:
                    paths = [[Fi, B, Ui, Bi, F]]
                # Right-facing colours are different -> don't solve pair
                else: paths = [[Fi, Ui, F]]

        elif edge_node == Ed.UB:
            # White faces down
            if cube.colours[Fc.D3] == cube.colours[Fc.D5]:
                # Front-facing and top-facing colours are the same
                if cube.colours[Fc.U2] == cube.colours[Fc.F9]:
                    paths = [[Fi, U, F], [Fi, Ui, F]]
                # Front-facing and top-facing colours are different
                else: paths = [[Ui, R, U, Ri]]

            # White faces right
            elif cube.colours[Fc.R7] == cube.colours[Fc.D5]:
                # Front-facing and top-facing colours are the same
                if cube.colours[Fc.U2] == cube.colours[Fc.F9]:
                    paths = [[U2]]
                # Front-facing and top-facing colours are different
                else: paths = [[R, U2, Ri], [U, R, U, Ri]]

            # White faces front
            elif cube.colours[Fc.F9] == cube.colours[Fc.D5]:
                # Right-facing and top-facing colours are the same
                if cube.colours[Fc.U2] == cube.colours[Fc.R7]:
                    paths = [[U]]
                # Right-facing and top-facing colours are different
                else: paths = [[R, Ui, Ri]]

        elif edge_node == Ed.UL:
            # White faces down
            if cube.colours[Fc.D3] == cube.colours[Fc.D5]:
                # Front-facing and left-facing colours are the same
                if cube.colours[Fc.F9] == cube.colours[Fc.L2]:
                    paths = [[R, Ui, Ri], [R, U, Ri]]
                # Front-facing and left-facing colours are different
                else: paths = [[U, Fi, Ui, F]]

            # White faces right
            elif cube.colours[Fc.R7] == cube.colours[Fc.D5]:
                # Front-facing and left-facing colours are the same
                if cube.colours[Fc.F9] == cube.colours[Fc.L2]:
                    paths = [[Fi, U, F]]
                # Front-facing and left-facing colours are different
                else: paths = [[Ui]]

            # White faces front
            elif cube.colours[Fc.F9] == cube.colours[Fc.D5]:
                # Right-facing and left-facing colours are the same
                if cube.colours[Fc.R7] == cube.colours[Fc.L2]:
                    paths = [[Fi, U2, F], [Ui, Fi, Ui, F]]
                # Right-facing and left-facing colours are different
                else: paths = [[U2]]

        elif edge_node == Ed.FL:
            # White faces down
            if cube.colours[Fc.D3] == cube.colours[Fc.D5]:
                # Front-facing colours are the same
                if cube.colours[Fc.F4] == cube.colours[Fc.F9]:
                    paths = [[Fi, U, F2, U, Fi], [F, U, Fi, R, U, Ri], [Li, U, L, Fi, Ui, F]]
                # Front-facing colours are different
                else: paths = [[Li, R, Ui, Ri, L]]

            # White faces right
            elif cube.colours[Fc.R7] == cube.colours[Fc.D5]:
                # Front-facing colours are the same
                if cube.colours[Fc.F4] == cube.colours[Fc.F9]:
                    paths = [[Li, Ui, L]]
                # Front-facing colours are different
                else: paths = [[F, U, Fi, Ui]]

            # White faces front
            elif cube.colours[Fc.F9] == cube.colours[Fc.D5]:
                # Right-facing and left-facing colours are the same
                if cube.colours[Fc.R7] == cube.colours[Fc.L6]:
                    paths = [[F, Ui, Fi]]
                # Right-facing and left-facing colours are different
                else: paths = [[Li, U2, L]]

        elif edge_node == Ed.FR:
            # White faces down
            if cube.colours[Fc.D3] == cube.colours[Fc.D5]:
                # Front-facing colours are different
                if cube.colours[Fc.F6] != cube.colours[Fc.F9]:
                    paths = [[R, Ui, Ri], [Fi, U, F]]
                # Front-facing colours are the same and pair not already solved
                elif cube.colours[Fc.F6] != cube.colours[Fc.F5]:
                    paths = [[R, U, Ri], [Fi, Ui, F]]

            # White faces right
            elif cube.colours[Fc.R7] == cube.colours[Fc.D5]:
                # Front-facing colours are the same
                if cube.colours[Fc.F6] == cube.colours[Fc.F9]:
                    paths = [[R, Ui, Ri, Fi, U, F]]
                # Front-facing colours are different
                else: paths = [[R, Ui, Ri]]

            # White faces front
            elif cube.colours[Fc.F9] == cube.colours[Fc.D5]:
                # Right-facing colours are the same
                if cube.colours[Fc.R4] == cube.colours[Fc.R7]:
                    paths = [[Fi, U, F, R, Ui, Ri]]
                # Right-facing colours are different
                else: paths = [[Fi, U, F]]

        elif edge_node == Ed.BR:
            # White faces down
            if cube.colours[Fc.D3] == cube.colours[Fc.D5]:
                # Right-facing colours are the same
                if cube.colours[Fc.R6] == cube.colours[Fc.R7]:
                    paths = [[B, Ui, Bi, R, U, Ri]]
                # Right-facing colours are different
                else: paths = [[Fi, B, U, Bi, F]]

            # White faces right
            elif cube.colours[Fc.R7] == cube.colours[Fc.D5]:
                # Front-facing and right-facing colours are the same
                if cube.colours[Fc.F9] == cube.colours[Fc.R6]:
                    paths = [[R, U, R2, U, R], [Fi, Ui, F]]
                # Front-facing and right-facing colours are different
                else: paths = [[Ri, U, R2, U, Ri], [B, U, Bi, R, U, Ri]]

            # White faces front
            elif cube.colours[Fc.F9] == cube.colours[Fc.D5]:
                # Right-facing colours are the same
                if cube.colours[Fc.R6] == cube.colours[Fc.R7]:
                    paths = [[B, U, Bi]]
                # Right-facing colours are different
                else: paths = [[Ri, U, R, Ui], [B, Ui, Bi, Fi, U2, F]]

        elif edge_node == Ed.BL:
            # White faces down
            if cube.colours[Fc.D3] == cube.colours[Fc.D5]:
                # Front-facing and left-facing colours are the same
                if cube.colours[Fc.F9] == cube.colours[Fc.L4]:
                    paths = [[L, R, U, Ri, Li]]
                # Front-facing and left-facing colours are different
                else: paths = [[L, U, Li, Fi, Ui, F], [Bi, Ui, B, R, U, Ri]]

            # White faces right
            elif cube.colours[Fc.R7] == cube.colours[Fc.D5]:
                # Front-facing and left-facing colours are the same
                if cube.colours[Fc.F9] == cube.colours[Fc.L4]:
                    paths = [[R, U, Ri, L, U2, Li], [Bi, U2, B, Fi, U, F]]
                # Front-facing and left-facing colours are different
                else: paths = [[L, Ui, Li]]

            # White faces front
            elif cube.colours[Fc.F9] == cube.colours[Fc.D5]:
                # Down-facing and left-facing colours are the same
                if cube.colours[Fc.D3] == cube.colours[Fc.L4]:
                    paths = [[L, U2, Li]]
                # Down-facing and left-facing colours are different
                else: paths = [[Bi, U, B]]

        return paths
