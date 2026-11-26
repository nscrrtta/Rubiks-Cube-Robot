from Kociemba.enums import Facelet as Fc, CubieIdx as Cb
from pathlib import Path


USE_MOTORS = False

# Root directory of the project
ROOT_DIR = Path(__file__).resolve().parents[2]

# Folder containing button images
PNG_DIR = ROOT_DIR / "png"

# Size of touch screen
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 535

# Center of cube
ORIGIN_X = WINDOW_WIDTH // 2
ORIGIN_Y = WINDOW_HEIGHT // 2

# x, y coordinates of items drawn on screen
SOLVE_BUTTON_POS  = 800, 155
SCRMB_BUTTON_POS  = 803, 248
ABORT_BUTTON_POS  = 807, 332
HOME1_BUTTON_POS  = 901, 155
HOME2_BUTTON_POS  = 901, 247
GLOBE_BUTTON_POS  = 901, 326
TOGGLE_BUTTON_POS = 920,  10
MOVE_COUNTER_POS  =  55, 490
KOCIEMBA_TEXT_POS = 910,  16
CFOP_TEXT_POS     = 910,  56
COLOUR_SELECTOR_POS = [
    ( 70, 160), # White
    ( 70, 240), # Blue
    ( 70, 320), # Red
    (155, 160), # Yellow
    (155, 240), # Green
    (155, 320)  # Orange
]

COLOUR_SELECTOR_SIZE = 56
SMALL_FONT_SIZE = 22
LARGE_FONT_SIZE = 30
CUBIE_SIZE = 100

RGB_VALUES = {
    0: (255, 255, 255), # White
    1: ( 64, 183, 255), # Blue
    2: (250,  90,  90), # Red
    3: (241, 241,  60), # Yellow
    4: (105, 245, 128), # Green
    5: (250, 140,  51), # Orange
   -1: (200, 200, 200)  # Inward-facing facelet
}

# Number of steps GUI makes for one quarter face rotation.
# Increasing this number will slow down the animation
#
# Tune this value along with STEP_DELAY in motors/constants.py
# such that the animation speed and motor speed line up.
STEPS_FACE_ROTATION = 40

# Number of steps GUI makes for one quarter cube rotation.
# Increasing this number will slow down the animation
STEPS_CUBE_ROTATION = 20

# Key: center of cubie in 3D space
# Val: indices of the 6 facelets for that cubie (U, R, F, D, L, B)
d = 1.05 # Increase this number to spread out cubies. Must be >= 1
CUBIE_DICT = {
    # Top layer
    (-d, -d, -d): [Fc.U1, Fc.XX, Fc.XX, Fc.XX, Fc.L1, Fc.B3], # ULB
    ( 0, -d, -d): [Fc.U2, Fc.XX, Fc.XX, Fc.XX, Fc.XX, Fc.B2], # UB
    ( d, -d, -d): [Fc.U3, Fc.R3, Fc.XX, Fc.XX, Fc.XX, Fc.B1], # UBR
    (-d, -d,  0): [Fc.U4, Fc.XX, Fc.XX, Fc.XX, Fc.L2, Fc.XX], # UL
    ( 0, -d,  0): [Fc.U5, Fc.XX, Fc.XX, Fc.XX, Fc.XX, Fc.XX], # U
    ( d, -d,  0): [Fc.U6, Fc.R2, Fc.XX, Fc.XX, Fc.XX, Fc.XX], # UR
    (-d, -d,  d): [Fc.U7, Fc.XX, Fc.F1, Fc.XX, Fc.L3, Fc.XX], # UFL
    ( 0, -d,  d): [Fc.U8, Fc.XX, Fc.F2, Fc.XX, Fc.XX, Fc.XX], # UF
    ( d, -d,  d): [Fc.U9, Fc.R1, Fc.F3, Fc.XX, Fc.XX, Fc.XX], # URF

    # Middle layer
    (-d,  0, -d): [Fc.XX, Fc.XX, Fc.XX, Fc.XX, Fc.L4, Fc.B6], # BL
    ( 0,  0, -d): [Fc.XX, Fc.XX, Fc.XX, Fc.XX, Fc.XX, Fc.B5], # B
    ( d,  0, -d): [Fc.XX, Fc.R6, Fc.XX, Fc.XX, Fc.XX, Fc.B4], # BR
    (-d,  0,  0): [Fc.XX, Fc.XX, Fc.XX, Fc.XX, Fc.L5, Fc.XX], # L
    ( d,  0,  0): [Fc.XX, Fc.R5, Fc.XX, Fc.XX, Fc.XX, Fc.XX], # R
    (-d,  0,  d): [Fc.XX, Fc.XX, Fc.F4, Fc.XX, Fc.L6, Fc.XX], # FL
    ( 0,  0,  d): [Fc.XX, Fc.XX, Fc.F5, Fc.XX, Fc.XX, Fc.XX], # F
    ( d,  0,  d): [Fc.XX, Fc.R4, Fc.F6, Fc.XX, Fc.XX, Fc.XX], # FR

    # Bottom layer
    (-d,  d, -d): [Fc.XX, Fc.XX, Fc.XX, Fc.D7, Fc.L7, Fc.B9], # DBL
    ( 0,  d, -d): [Fc.XX, Fc.XX, Fc.XX, Fc.D8, Fc.XX, Fc.B8], # DB
    ( d,  d, -d): [Fc.XX, Fc.R9, Fc.XX, Fc.D9, Fc.XX, Fc.B7], # DRB
    (-d,  d,  0): [Fc.XX, Fc.XX, Fc.XX, Fc.D4, Fc.L8, Fc.XX], # DL
    ( 0,  d,  0): [Fc.XX, Fc.XX, Fc.XX, Fc.D5, Fc.XX, Fc.XX], # D
    ( d,  d,  0): [Fc.XX, Fc.R8, Fc.XX, Fc.D6, Fc.XX, Fc.XX], # DR
    (-d,  d,  d): [Fc.XX, Fc.XX, Fc.F7, Fc.D1, Fc.L9, Fc.XX], # DLF
    ( 0,  d,  d): [Fc.XX, Fc.XX, Fc.F8, Fc.D2, Fc.XX, Fc.XX], # DF
    ( d,  d,  d): [Fc.XX, Fc.R7, Fc.F9, Fc.D3, Fc.XX, Fc.XX]  # DFR
}

# Important that order for each face matches Facelet enum in Kociemba.enums
FACE_INDICES = {
    'U': [Cb.ULB, Cb.UB, Cb.UBR, Cb.UL, Cb.U, Cb.UR, Cb.UFL, Cb.UF, Cb.URF],
    'R': [Cb.URF, Cb.UR, Cb.UBR, Cb.FR, Cb.R, Cb.BR, Cb.DFR, Cb.DR, Cb.DRB],
    'F': [Cb.UFL, Cb.UF, Cb.URF, Cb.FL, Cb.F, Cb.FR, Cb.DLF, Cb.DF, Cb.DFR],
    'D': [Cb.DLF, Cb.DF, Cb.DFR, Cb.DL, Cb.D, Cb.DR, Cb.DBL, Cb.DB, Cb.DRB],
    'L': [Cb.ULB, Cb.UL, Cb.UFL, Cb.BL, Cb.L, Cb.FL, Cb.DBL, Cb.DL, Cb.DLF],
    'B': [Cb.UBR, Cb.UB, Cb.ULB, Cb.BR, Cb.B, Cb.BL, Cb.DRB, Cb.DB, Cb.DBL]
}

# Important that order follows a clockwise rotation
# relative to the direction each face turns
CORNER_INDICES = {
    'U': [Cb.ULB, Cb.UBR, Cb.URF, Cb.UFL],
    'R': [Cb.URF, Cb.UBR, Cb.DRB, Cb.DFR],
    'F': [Cb.UFL, Cb.URF, Cb.DFR, Cb.DLF],
    'D': [Cb.DFR, Cb.DRB, Cb.DBL, Cb.DLF],
    'L': [Cb.ULB, Cb.UFL, Cb.DLF, Cb.DBL],
    'B': [Cb.UBR, Cb.ULB, Cb.DBL, Cb.DRB]
}
EDGE_INDICES = {
    'U': [Cb.UB, Cb.UR, Cb.UF, Cb.UL],
    'R': [Cb.UR, Cb.BR, Cb.DR, Cb.FR],
    'F': [Cb.UF, Cb.FR, Cb.DF, Cb.FL],
    'D': [Cb.DF, Cb.DR, Cb.DB, Cb.DL],
    'L': [Cb.UL, Cb.FL, Cb.DL, Cb.BL],
    'B': [Cb.UB, Cb.BL, Cb.DB, Cb.BR]
}
