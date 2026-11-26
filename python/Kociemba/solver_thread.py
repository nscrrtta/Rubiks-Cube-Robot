from Kociemba.coord import CoordCube
from Kociemba.symmetries import syms
from Kociemba.tables import tables
from Kociemba.constants import *
from Kociemba.enums import Move
from Kociemba.cube import Cube
import threading as thr
import time


class SolverThread(thr.Thread):

    def __init__(
            self,
            cube: Cube,
            index: int,
            timeout: int,
            max_length: int,
            solutions: list[list[str]],
            terminated: thr.Event,
            shortest_length: list[int]
        ):
        thr.Thread.__init__(self)
        self.cb_cube = cube
        self.rot = index % 2
        self.inv = index // 2
        self.timeout = timeout
        self.max_length = max_length

        # These variables are shared by the six threads, initialized in solve function
        self.solutions = solutions
        self.terminated = terminated
        self.shortest_length = shortest_length

        self.start_time = time.monotonic()
        self.lock = thr.Lock()
        self.corner_save = 0

    def _search_phase1(self, flip: int, twist: int, slice_sorted: int, dist: int, remaining: int):
        if self.terminated.is_set():
            return
        if remaining == 0:
            self._phase1_solved(slice_sorted)
            return

        # Phase 1 not solved...

        for m in Move:
            # dist = 0 means that we are already in the subgroup H.
            # If there are less than 5 moves left this forces all remaining moves to be phase 2 moves.
            # So we can forbid these at the end of phase 1 and generate these moves in phase 2.
            if dist == 0 and remaining < 5 and m in PHASE2_MOVES:
                continue

            if len(self.phase1_moves) > 0:
                diff = self.phase1_moves[-1] // 3 - m // 3
                # Successive moves: on same face or on same axis with wrong order
                if diff in [0, 3]:
                    continue

            flip_new = tables.move_flip[N_MOVE * flip + m]
            twist_new = tables.move_twist[N_MOVE * twist + m]
            slice_sorted_new = tables.move_slice_sorted[N_MOVE * slice_sorted + m]

            flip_slice = N_FLIP * (slice_sorted_new // 24) + flip_new
            class_idx = tables.fs_class_idx[flip_slice]
            sym = tables.fs_sym[flip_slice]
            dist_new_mod3 = tables.get_flipslice_twist_depth3(
                N_TWIST * class_idx + tables.conj_twist[(twist_new << 2) + sym]
            )
            dist_new = tables.distance[3 * dist + dist_new_mod3]

            # Impossible to reach subgroup H in (remaining - 1) moves
            if dist_new >= remaining:
                continue

            self.phase1_moves.append(m)
            self._search_phase1(flip_new, twist_new, slice_sorted_new, dist_new, remaining - 1)
            self.phase1_moves.pop()

    def _phase1_solved(self, slice_sorted: int):
        if time.monotonic() > self.start_time + self.timeout and self.solutions:
            self.terminated.set()

        if self.phase1_moves and self.phase1_moves[-1] in [Move.R3, Move.F3, Move.L3]:
            # Apply R2, F2, L2 or B2 on last phase1 solution
            m = self.phase1_moves[-1]
            corners = tables.move_corners[N_MOVE * self.corner_save + m - 1]
        else:
            corners = self.co_cube.corners
            # Get current corner configuration
            for m in self.phase1_moves:
                corners = tables.move_corners[N_MOVE * corners + m]
            self.corner_save = corners

        # New solution must be shorter / do not use phase 2 solutions with length > 12
        limit = min(self.shortest_length[0] - len(self.phase1_moves), 13)
        if tables.pruning_phase2_corner_slice[24 * corners + slice_sorted] >= limit:
            return

        u_edges = self.co_cube.u_edges
        d_edges = self.co_cube.d_edges

        for m in self.phase1_moves:
            u_edges = tables.move_u_edges[N_MOVE * u_edges + m]
            d_edges = tables.move_d_edges[N_MOVE * d_edges + m]

        ud_edges = tables.phase2_edge_merge[24 * u_edges + d_edges % 24]

        dist2 = tables.get_depth_phase2(corners, ud_edges)

        # Do not use more than phase2_limit - 1 moves in phase 2
        for remaining in range(dist2, limit):
            self.phase2_moves = []
            self._search_phase2(corners, ud_edges, slice_sorted, dist2, remaining)

    def _search_phase2(self, corners: int, ud_edges: int, slice_sorted: int, dist: int, remaining: int):
        if self.terminated.is_set():
            return
        if remaining == 0 and slice_sorted == 0:
            self._phase2_solved()
            return

        # Phase 2 not solved...

        for m in Move:
            if m in PHASE1_MOVES:
                continue

            if self.phase2_moves:
                diff = self.phase2_moves[-1] // 3 - m // 3
                # Successive moves: on same face or on same axis with wrong order
                if diff in [0, 3]:
                    continue
            elif self.phase1_moves:
                diff = self.phase1_moves[-1] // 3 - m // 3
                # Successive moves: on same face or on same axis with wrong order
                if diff in [0, 3]:
                    continue

            corners_new = tables.move_corners[N_MOVE * corners + m]
            ud_edges_new = tables.move_ud_edges[N_MOVE * ud_edges + m]
            slice_sorted_new = tables.move_slice_sorted[N_MOVE * slice_sorted + m]

            sym = tables.co_sym[corners_new]
            class_idx = tables.co_class_idx[corners_new]
            dist_new_mod3 = tables.get_corners_ud_edges_depth3(
                40320 * class_idx + tables.conj_ud_edges[(ud_edges_new << 2) + sym]
            )
            dist_new = tables.distance[3 * dist + dist_new_mod3]

            # Impossible to reach solved cube in (remaining - 1) moves
            depth = tables.pruning_phase2_corner_slice[24 * corners_new + slice_sorted_new]
            if max(dist_new, depth) >= remaining:
                continue

            self.phase2_moves.append(m)
            self._search_phase2(corners_new, ud_edges_new, slice_sorted_new, dist_new, remaining - 1)
            self.phase2_moves.pop()

    def _phase2_solved(self):
        self.lock.acquire()
        moves = self.phase1_moves + self.phase2_moves

        if len(self.solutions) == 0 or len(moves) < len(self.solutions[-1]):
            # We solved the inverse cube
            if self.inv == 1:
                # R1->R3, R2->R2, R3->R1, etc
                moves = [Move((m // 3) * 3 + (2 - m % 3)) for m in moves[::-1]]

            moves = [Move(syms.move_array[m][38 * self.rot]).name for m in moves]
            self.shortest_length[0] = len(moves)
            self.solutions.append(moves)

        # We have reached the target number of solutions
        if self.shortest_length[0] <= self.max_length:
            self.terminated.set()

        self.lock.release()

    def _invert_cube(self, cube: Cube) -> Cube:
        inverted = Cube()

        for e in range(12):
            inverted.ep[cube.ep[e]] = e
        for e in range(12):
            inverted.eo[e] = cube.eo[inverted.ep[e]]

        for c in range(8):
            inverted.cp[cube.cp[c]] = c
        for c in range(8):
            ori = cube.co[inverted.cp[c]]
            if 0 < ori < 3: ori = 3-ori
            inverted.co[c] = ori

        return inverted

    def run(self):
        if self.rot == 0: # No rotation
            cb = self.cb_cube.spawn_child()
        elif self.rot == 1:  # Conjugation by 90° rotation about FB axis
            cb = syms.symmetry_cubes[36].spawn_child()
            cb.multiply(self.cb_cube)
            cb.multiply(syms.symmetry_cubes[38])

        if self.inv == 1: # Invert cube
            cb = self._invert_cube(cb)

        self.co_cube = CoordCube(cb) # The rotated/inverted cube in coordinate representation

        dist = tables.get_depth_phase1(
            self.co_cube.flip,
            self.co_cube.twist,
            self.co_cube.slice_sorted // N_PERM_4
        )

        for remaining in range(dist, 20): # Iterative deepening, solution has at least dist moves
            self.phase1_moves = []
            self._search_phase1(
                self.co_cube.flip,
                self.co_cube.twist,
                self.co_cube.slice_sorted,
                dist, remaining
            )
