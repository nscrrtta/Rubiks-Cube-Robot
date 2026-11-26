from Kociemba.constants import *
import array as ar
import os


class Tables:

    def __init__(self):
        self.all_tables_loaded = True

        # Coord
        self.phase2_edge_merge = self._load_table('phase2_edge_merge', N_U_EDGES_PHASE2 * N_PERM_4)

        # Moves
        self.move_flip = self._load_table('move_flip', N_FLIP * N_MOVE)
        self.move_twist = self._load_table('move_twist', N_TWIST * N_MOVE)
        self.move_corners = self._load_table('move_corners', N_CORNERS * N_MOVE)
        self.move_ud_edges = self._load_table('move_ud_edges', N_UD_EDGES * N_MOVE)
        self.move_u_edges = self._load_table('move_u_edges', N_SLICE_SORTED * N_MOVE)
        self.move_d_edges = self._load_table('move_d_edges', N_SLICE_SORTED * N_MOVE)
        self.move_slice_sorted = self._load_table('move_slice_sorted', N_SLICE_SORTED * N_MOVE)

        # Pruning
        self.pruning_phase2_corner_slice = self._load_table('pruning_phase2_corner_slice', N_CORNERS * N_PERM_4, 'b')
        self.pruning_phase1 = self._load_table('pruning_phase1', (N_FLIPSLICE_CLASS * N_TWIST) // 16 + 1, 'L')
        self.pruning_phase2 = self._load_table('pruning_phase2', (N_CORNERS_CLASS * N_UD_EDGES) // 16, 'L')
        self.distance = self._create_distance_array()

        # Symmetries
        self.conj_ud_edges = self._load_table('conj_ud_edges', N_UD_EDGES * N_SYM_CV2)
        self.conj_twist = self._load_table('conj_twist', N_TWIST * N_SYM_CV2)

        self.fs_class_idx = self._load_table('fs_class_idx', N_FLIP * N_SLICE, 'L')
        self.fs_rep = self._load_table('fs_rep', N_FLIPSLICE_CLASS, 'L')
        self.fs_sym = self._load_table('fs_sym', N_FLIP * N_SLICE, 'B')

        self.co_class_idx = self._load_table('co_class_idx', N_CORNERS)
        self.co_rep = self._load_table('co_rep', N_CORNERS_CLASS)
        self.co_sym = self._load_table('co_sym', N_CORNERS, 'B')

    def _load_table(self, file_name: str, byte_size: int, type_code: str = 'H') -> ar.array:
        arr = ar.array(type_code)
        try:
            with open(os.path.join(FOLDER, file_name), 'rb') as f:
                arr.fromfile(f, byte_size)
                return arr
        except (FileNotFoundError, EOFError) as e:
            print(f'[ERROR] Could not load table: {file_name} | {e}')
            self.all_tables_loaded = False
        return arr

    def _create_distance_array(self) -> list[int]:
        distance = [0] * 60
        for i in range(20):
            for j in range(3):
                val = (i // 3) * 3 + j
                if i % 3 == 2 and j == 0:
                    val += 3
                elif i % 3 == 0 and j == 2:
                    val -= 3
                distance[3 * i + j] = val
        return distance

    def get_flipslice_twist_depth3(self, x: int) -> int:
        y = self.pruning_phase1[x // 16]
        y >>= (x % 16) * 2
        return y & 3

    def get_corners_ud_edges_depth3(self, x: int) -> int:
        y = self.pruning_phase2[x // 16]
        y >>= (x % 16) * 2
        return y & 3

    def get_depth_phase1(self, flip: int, twist: int, slice_: int) -> int:
        """Compute the distance to the cube subgroup H where flip = slice = twist = 0"""
        flipslice = N_FLIP * slice_ + flip
        sym = self.fs_sym[flipslice]
        class_idx = self.fs_class_idx[flipslice]

        x = N_TWIST * class_idx + self.conj_twist[(twist << 2) + sym]
        depth_mod3 = self.get_flipslice_twist_depth3(x)

        depth = 0
        while (flip, slice_, twist) != (0, 0, 0): # While not solved
            if depth_mod3 == 0:
                depth_mod3 = 3
            for i in range(N_MOVE):
                flip1 = self.move_flip[N_MOVE * flip + i]
                twist1 = self.move_twist[N_MOVE * twist + i]
                slice1 = self.move_slice_sorted[N_MOVE * slice_ * N_PERM_4 + i] // N_PERM_4

                flipslice1 = N_FLIP * slice1 + flip1
                sym = self.fs_sym[flipslice1]
                class_idx1 = self.fs_class_idx[flipslice1]

                x = N_TWIST * class_idx1 + self.conj_twist[(twist1 << 2) + sym]
                if self.get_flipslice_twist_depth3(x) == depth_mod3 - 1:
                    twist = twist1
                    slice_ = slice1
                    flip = flip1
                    depth_mod3 -= 1
                    depth += 1
                    break

        return depth

    def get_depth_phase2(self, corners: int, ud_edges: int) -> int:
        """
        Get distance to subgroup where only the UD-slice edges may be permuted in their slice.
        (Only 24 / 2 = 12 possible ways due to overall even parity).
        This is a lower bound for the number of moves to solve phase 2.
        """
        sym = self.co_sym[corners]
        class_idx = self.co_class_idx[corners]

        x = N_UD_EDGES * class_idx + self.conj_ud_edges[(ud_edges << 2) + sym]
        depth_mod3 = self.get_corners_ud_edges_depth3(x)

        # Unfilled entry
        if depth_mod3 == 3:
            return 11

        depth = 0
        while (corners, ud_edges) != (0, 0): # While not solved
            if depth_mod3 == 0:
                depth_mod3 = 3
            # Only iterate phase 2 moves
            for i in PHASE2_MOVES:
                corners1 = self.move_corners[N_MOVE * corners + i]
                ud_edges1 = self.move_ud_edges[N_MOVE * ud_edges + i]

                sym = self.co_sym[corners1]
                class_idx1 = self.co_class_idx[corners1]

                x = N_UD_EDGES * class_idx1 + self.conj_ud_edges[(ud_edges1 << 2) + sym]
                if self.get_corners_ud_edges_depth3(x) == depth_mod3 - 1:
                    corners = corners1
                    ud_edges = ud_edges1
                    depth_mod3 -= 1
                    depth += 1
                    break

        return depth


tables = Tables()
