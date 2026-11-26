from Kociemba.enums import Edge as Ed, Facelet as Fc


M = 'M1';    M2 = 'M2';    Mi = 'M3'
E = 'E1';    E2 = 'E2';    Ei = 'E3'
S = 'S1';    S2 = 'S2';    Si = 'S3'

U = 'U1';    U2 = 'U2';    Ui = 'U3'
R = 'R1';    R2 = 'R2';    Ri = 'R3'
F = 'F1';    F2 = 'F2';    Fi = 'F3'
D = 'D1';    D2 = 'D2';    Di = 'D3'
L = 'L1';    L2 = 'L2';    Li = 'L3'
B = 'B1';    B2 = 'B2';    Bi = 'B3'

u = 'u1';    u2 = 'u2';    ui = 'u3'
r = 'r1';    r2 = 'r2';    ri = 'r3'
f = 'f1';    f2 = 'f2';    fi = 'f3'
d = 'd1';    d2 = 'd2';    di = 'd3'
l = 'l1';    l2 = 'l2';    li = 'l3'
b = 'b1';    b2 = 'b2';    bi = 'b3'


# Faces that are swapped for slice moves
FACE_SWAPS = {
    'M': ['U', 'F', 'D', 'B'],
    'E': ['F', 'R', 'B', 'L'],
    'S': ['U', 'R', 'D', 'L']
}

# Facelet indices that are swapped for each move
FACELET_SWAPS = {
    'M': [[Fc.B8, Fc.U2, Fc.F2, Fc.D2], [Fc.B5, Fc.U5, Fc.F5, Fc.D5], [Fc.B2, Fc.U8, Fc.F8, Fc.D8]],
    'E': [[Fc.B4, Fc.L4, Fc.F4, Fc.R4], [Fc.B5, Fc.L5, Fc.F5, Fc.R5], [Fc.B6, Fc.L6, Fc.F6, Fc.R6]],
    'S': [[Fc.L8, Fc.U4, Fc.R2, Fc.D6], [Fc.L5, Fc.U5, Fc.R5, Fc.D5], [Fc.L2, Fc.U6, Fc.R8, Fc.D4]],
    'U': [[Fc.B3, Fc.R3, Fc.F3, Fc.L3], [Fc.B2, Fc.R2, Fc.F2, Fc.L2], [Fc.B1, Fc.R1, Fc.F1, Fc.L1], [Fc.U1, Fc.U3, Fc.U9, Fc.U7], [Fc.U2, Fc.U6, Fc.U8, Fc.U4]],
    'R': [[Fc.B1, Fc.D9, Fc.F9, Fc.U9], [Fc.B4, Fc.D6, Fc.F6, Fc.U6], [Fc.B7, Fc.D3, Fc.F3, Fc.U3], [Fc.R1, Fc.R3, Fc.R9, Fc.R7], [Fc.R2, Fc.R6, Fc.R8, Fc.R4]],
    'F': [[Fc.L9, Fc.U7, Fc.R1, Fc.D3], [Fc.L6, Fc.U8, Fc.R4, Fc.D2], [Fc.L3, Fc.U9, Fc.R7, Fc.D1], [Fc.F1, Fc.F3, Fc.F9, Fc.F7], [Fc.F2, Fc.F6, Fc.F8, Fc.F4]],
    'D': [[Fc.B7, Fc.L7, Fc.F7, Fc.R7], [Fc.B8, Fc.L8, Fc.F8, Fc.R8], [Fc.B9, Fc.L9, Fc.F9, Fc.R9], [Fc.D1, Fc.D3, Fc.D9, Fc.D7], [Fc.D2, Fc.D6, Fc.D8, Fc.D4]],
    'L': [[Fc.B9, Fc.U1, Fc.F1, Fc.D1], [Fc.B6, Fc.U4, Fc.F4, Fc.D4], [Fc.B3, Fc.U7, Fc.F7, Fc.D7], [Fc.L1, Fc.L3, Fc.L9, Fc.L7], [Fc.L2, Fc.L6, Fc.L8, Fc.L4]],
    'B': [[Fc.L1, Fc.D7, Fc.R9, Fc.U3], [Fc.L4, Fc.D8, Fc.R6, Fc.U2], [Fc.L7, Fc.D9, Fc.R3, Fc.U1], [Fc.B1, Fc.B3, Fc.B9, Fc.B7], [Fc.B2, Fc.B6, Fc.B8, Fc.B4]]
}

# Moves that link two edges
EDGE_LINKS = {
    Ed.UR: {Ed.UF: U, Ed.UL: U2, Ed.UB: Ui, Ed.BR: R, Ed.DR: R2, Ed.FR: Ri},
    Ed.UF: {Ed.UL: U, Ed.UB: U2, Ed.UR: Ui, Ed.FR: F, Ed.DF: F2, Ed.FL: Fi},
    Ed.UL: {Ed.UB: U, Ed.UR: U2, Ed.UF: Ui, Ed.FL: L, Ed.DL: L2, Ed.BL: Li},
    Ed.UB: {Ed.UR: U, Ed.UF: U2, Ed.UL: Ui, Ed.BL: B, Ed.DB: B2, Ed.BR: Bi},

    Ed.FR: {Ed.DF: F, Ed.FL: F2, Ed.UF: Fi, Ed.UR: R, Ed.BR: R2, Ed.DR: Ri},
    Ed.FL: {Ed.UF: F, Ed.FR: F2, Ed.DF: Fi, Ed.DL: L, Ed.BL: L2, Ed.UL: Li},
    Ed.BL: {Ed.DB: B, Ed.BR: B2, Ed.UB: Bi, Ed.UL: L, Ed.FL: L2, Ed.DL: Li},
    Ed.BR: {Ed.UB: B, Ed.BL: B2, Ed.DB: Bi, Ed.DR: R, Ed.FR: R2, Ed.UR: Ri},

    Ed.DR: {Ed.DB: D, Ed.DL: D2, Ed.DF: Di, Ed.FR: R, Ed.UR: R2, Ed.BR: Ri},
    Ed.DF: {Ed.DR: D, Ed.DB: D2, Ed.DL: Di, Ed.FL: F, Ed.UF: F2, Ed.FR: Fi},
    Ed.DL: {Ed.DF: D, Ed.DR: D2, Ed.DB: Di, Ed.BL: L, Ed.UL: L2, Ed.FL: Li},
    Ed.DB: {Ed.DL: D, Ed.DF: D2, Ed.DR: Di, Ed.BR: B, Ed.UB: B2, Ed.BL: Bi}
}

# Cube faces that are opposite to each other
OPPOSITES = {'U':'D', 'D':'U', 'L':'R', 'R':'L', 'F':'B', 'B':'F'}

# Moves that are used to replace a U move
SEQUENCE = [L, R, F2, B2, Li, Ri]


"""
Tune these variables to adjust speed vs number of moves.

Higher values:
  - Explore more options
  - Code will take longer
  - Solution will have fewer moves

Lower values:
  - Explore fewer options
  - Code will be faster
  - Solution will have more moves
"""

# Max number of cubes to solve cross
MAX_SOLVE_CROSS = 200

# How many cubes with cross solved to continue solving
# First number: How many cubes should not have U moves
# Second number: How many cubes should have U moves
NUM_CUBES_CROSS = 7, 3

# Max number of cubes to solve F2L (per cube with cross solved)
MAX_SOLVE_F2L = 50

# How many cubes with F2L solved to continue solving
NUM_CUBES_F2L = 100
