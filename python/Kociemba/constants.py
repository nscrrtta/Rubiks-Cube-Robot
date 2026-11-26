from Kociemba.enums import Color as Cl, Facelet as Fc, Move as Mv
from pathlib import Path


# Root directory of the project
ROOT_DIR = Path(__file__).resolve().parents[2]

# Folder name for generated tables
FOLDER = ROOT_DIR / "python" / "Kociemba" / "twophase-tables"

# Map the corner positions to facelet positions
CORNER_FACELETS = [
    [Fc.U9, Fc.R1, Fc.F3],
    [Fc.U7, Fc.F1, Fc.L3],
    [Fc.U1, Fc.L1, Fc.B3],
    [Fc.U3, Fc.B1, Fc.R3],
    [Fc.D3, Fc.F9, Fc.R7],
    [Fc.D1, Fc.L9, Fc.F7],
    [Fc.D7, Fc.B9, Fc.L7],
    [Fc.D9, Fc.R9, Fc.B7]
]

# Map the edge positions to facelet positions
EDGE_FACELETS = [
    [Fc.U6, Fc.R2],
    [Fc.U8, Fc.F2],
    [Fc.U4, Fc.L2],
    [Fc.U2, Fc.B2],
    [Fc.D6, Fc.R8],
    [Fc.D2, Fc.F8],
    [Fc.D4, Fc.L8],
    [Fc.D8, Fc.B8],
    [Fc.F6, Fc.R4],
    [Fc.F4, Fc.L6],
    [Fc.B6, Fc.L4],
    [Fc.B4, Fc.R6]
]

# Map the corner positions to facelet colors
CORNER_COLORS = [
    [Cl.U, Cl.R, Cl.F],
    [Cl.U, Cl.F, Cl.L],
    [Cl.U, Cl.L, Cl.B],
    [Cl.U, Cl.B, Cl.R],
    [Cl.D, Cl.F, Cl.R],
    [Cl.D, Cl.L, Cl.F],
    [Cl.D, Cl.B, Cl.L],
    [Cl.D, Cl.R, Cl.B]
]

# Map the edge positions to facelet colors
EDGE_COLORS = [
    [Cl.U, Cl.R],
    [Cl.U, Cl.F],
    [Cl.U, Cl.L],
    [Cl.U, Cl.B],
    [Cl.D, Cl.R],
    [Cl.D, Cl.F],
    [Cl.D, Cl.L],
    [Cl.D, Cl.B],
    [Cl.F, Cl.R],
    [Cl.F, Cl.L],
    [Cl.B, Cl.L],
    [Cl.B, Cl.R]
]

PHASE1_MOVES = [
    Mv.R1, Mv.R3, Mv.L1, Mv.L3, Mv.F1, Mv.F3
]

PHASE2_MOVES = [
    Mv.U1, Mv.U2, Mv.U3, Mv.R2, Mv.F2,
    Mv.D1, Mv.D2, Mv.D3, Mv.L2
]

N_MOVE = 15
N_PERM_4 = 24

# 3^7 possible corner orientations in phase 1
N_TWIST = 2187

# 2^11 possible edge orientations in phase 1
N_FLIP = 2048

# 12*11*10*9 possible positions of the FR, FL, BL, BR edges in phase 1
N_SLICE_SORTED = 11880

# Ignore the permutation of FR, FL, BL, BR in phase 1
N_SLICE = N_SLICE_SORTED // N_PERM_4

# Number of equivalence classes for combined flip+slice concerning symmetry group C2v(a1)
N_FLIPSLICE_CLASS = 255644

# Number of different positions of the edges UR, UF, UL and UB in phase 2
N_U_EDGES_PHASE2 = 1680

# 8! corner permutations in phase 2
N_CORNERS = 40320

# Number of equivalence classes concerning symmetry group C2v(a1)
N_CORNERS_CLASS = 10368

# 8! permutations of the edges in the U-face and D-face in phase 2
N_UD_EDGES = 40320

# Number of symmetries of full group Oh
N_SYM = 48

# Number of symmetries of subgroup C2v(a1)
N_SYM_CV2 = 4

### The basic six cube moves described by permutations and changes in orientation ###

# Up-move
U_CP = [3, 0, 1, 2, 4, 5, 6, 7]
U_CO = [0, 0, 0, 0, 0, 0, 0, 0]
U_EP = [3, 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11]
U_EO = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Right-move
R_CP = [4, 1, 2, 0, 7, 5, 6, 3]
R_CO = [2, 0, 0, 1, 1, 0, 0, 2]
R_EP = [8, 1, 2, 3, 11, 5, 6, 7, 4, 9, 10, 0]
R_EO = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Front-move
F_CP = [1, 5, 2, 3, 0, 4, 6, 7]
F_CO = [1, 2, 0, 0, 2, 1, 0, 0]
F_EP = [0, 9, 2, 3, 4, 8, 6, 7, 1, 5, 10, 11]
F_EO = [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0]

# Down-move
D_CP = [0, 1, 2, 3, 5, 6, 7, 4]
D_CO = [0, 0, 0, 0, 0, 0, 0, 0]
D_EP = [0, 1, 2, 3, 5, 6, 7, 4, 8, 9, 10, 11]
D_EO = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Left-move
L_CP = [0, 2, 6, 3, 4, 1, 5, 7]
L_CO = [0, 1, 2, 0, 0, 2, 1, 0]
L_EP = [0, 1, 10, 3, 4, 5, 9, 7, 8, 2, 6, 11]
L_EO = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

### Basic symmetry cubes described by permutations and changes in orientation ###

# 90° clockwise rotation around the axis through the U and D centers
ROT_90_CP = [3, 0, 1, 2, 7, 4, 5, 6]
ROT_90_CO = [0, 0, 0, 0, 0, 0, 0, 0]
ROT_90_EP = [3, 0, 1, 2, 7, 4, 5, 6, 11, 8, 9, 10]
ROT_90_EO = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]

# 120° clockwise rotation around the long diagonal URF-DBL
ROT_120_CP = [0, 4, 5, 1, 3, 7, 6, 2]
ROT_120_CO = [1, 2, 1, 2, 2, 1, 2, 1]
ROT_120_EP = [1, 8, 5, 9, 3, 11, 7, 10, 0, 4, 6, 2]
ROT_120_EO = [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1]

# 180° rotation around the axis through the F and B centers
ROT_180_CP = [5, 4, 7, 6, 1, 0, 3, 2]
ROT_180_CO = [0, 0, 0, 0, 0, 0, 0, 0]
ROT_180_EP = [6, 5, 4, 7, 2, 1, 0, 3, 9, 8, 11, 10]
ROT_180_EO = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Reflection at the plane through the U, D, F, B centers
REFLECT_CP = [1, 0, 3, 2, 5, 4, 7, 6]
REFLECT_CO = [3, 3, 3, 3, 3, 3, 3, 3]
REFLECT_EP = [2, 1, 0, 3, 6, 5, 4, 7, 9, 8, 11, 10]
REFLECT_EO = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
