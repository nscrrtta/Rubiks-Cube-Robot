from Kociemba.constants import *
from Kociemba.tables import tables
from Kociemba.cube import Cube


class CoordCube:
    """
    Represent a cube on the coordinate level.

    In phase 1, a state is uniquely determined by the three coordinates:
    flip, twist and slice = slice_sorted // 24.

    In phase 2, a state is uniquely determined by the three coordinates:
    corners, ud_edges and slice_sorted % 24.
    """
    def __init__(self, cube: Cube):
        self.flip = cube.get_flip()
        self.twist = cube.get_twist()
        self.u_edges = cube.get_u_edges()
        self.d_edges = cube.get_d_edges()
        self.corners = cube.get_corners()
        self.slice_sorted = cube.get_slice_sorted()

        self.ud_edges = -1 # Invalid
        if self.slice_sorted < N_PERM_4: # Phase 2 cube
            self.ud_edges = cube.get_ud_edges()

        # Symmetry reduced flipslice coordinate used in phase 1
        self.flipslice_class_idx = tables.fs_class_idx[N_FLIP * (self.slice_sorted // N_PERM_4) + self.flip]
        self.flipslice_sym = tables.fs_sym[N_FLIP * (self.slice_sorted // N_PERM_4) + self.flip]
        self.flipslice_rep = tables.fs_rep[self.flipslice_class_idx]

        # Symmetry reduced corner permutation coordinate used in phase 2
        self.corner_class_idx = tables.co_class_idx[self.corners]
        self.corner_rep = tables.co_rep[self.corner_class_idx]
        self.corner_sym = tables.co_sym[self.corners]
