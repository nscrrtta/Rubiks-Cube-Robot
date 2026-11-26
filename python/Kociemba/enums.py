from enum import IntEnum


"""
                Up (0)
                |  0  1  2 |
                |  3  4  5 |
                |  6  7  8 |

Left (4)        Front (2)       Right (1)       Back (5)
| 36 37 38 |    | 18 19 20 |    |  9 10 11 |    | 45 46 47 |
| 39 40 41 |    | 21 22 23 |    | 12 13 14 |    | 48 49 50 |
| 42 43 44 |    | 24 25 26 |    | 15 16 17 |    | 51 52 53 |

                Down (3)
                | 27 28 29 |
                | 30 31 32 |
                | 33 34 35 |
"""
class Facelet(IntEnum):
    U1 = 0; U2 = 1; U3 = 2
    U4 = 3; U5 = 4; U6 = 5
    U7 = 6; U8 = 7; U9 = 8

    R1 = 9;  R2 = 10; R3 = 11
    R4 = 12; R5 = 13; R6 = 14
    R7 = 15; R8 = 16; R9 = 17

    F1 = 18; F2 = 19; F3 = 20
    F4 = 21; F5 = 22; F6 = 23
    F7 = 24; F8 = 25; F9 = 26

    D1 = 27; D2 = 28; D3 = 29
    D4 = 30; D5 = 31; D6 = 32
    D7 = 33; D8 = 34; D9 = 35

    L1 = 36; L2 = 37; L3 = 38
    L4 = 39; L5 = 40; L6 = 41
    L7 = 42; L8 = 43; L9 = 44

    B1 = 45; B2 = 46; B3 = 47
    B4 = 48; B5 = 49; B6 = 50
    B7 = 51; B8 = 52; B9 = 53

    XX = -1 # Inward-facing facelet


class Color(IntEnum):
    U = 0
    R = 1
    F = 2
    D = 3
    L = 4
    B = 5


class Corner(IntEnum):
    URF = 0
    UFL = 1
    ULB = 2
    UBR = 3
    DFR = 4
    DLF = 5
    DBL = 6
    DRB = 7


class Edge(IntEnum):
    UR = 0
    UF = 1
    UL = 2
    UB = 3
    DR = 4
    DF = 5
    DL = 6
    DB = 7
    FR = 8
    FL = 9
    BL = 10
    BR = 11


class Move(IntEnum):
    U1 = 0
    U2 = 1
    U3 = 2
    R1 = 3
    R2 = 4
    R3 = 5
    F1 = 6
    F2 = 7
    F3 = 8
    D1 = 9
    D2 = 10
    D3 = 11
    L1 = 12
    L2 = 13
    L3 = 14


class CubieIdx(IntEnum):
    ULB = 0
    UB  = 1
    UBR = 2
    UL  = 3
    U   = 4
    UR  = 5
    UFL = 6
    UF  = 7
    URF = 8
    BL  = 9
    B   = 10
    BR  = 11
    L   = 12
    R   = 13
    FL  = 14
    F   = 15
    FR  = 16
    DBL = 17
    DB  = 18
    DRB = 19
    DL  = 20
    D   = 21
    DR  = 22
    DLF = 23
    DF  = 24
    DFR = 25
