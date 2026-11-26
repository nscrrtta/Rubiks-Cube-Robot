from Kociemba.constants import *
from Kociemba.cube import Cube


class Symmetries:

    def __init__(self):
        self._create_symmetry_cubes()
        self._create_inversion_array()
        self._create_move_array()

    def _create_symmetry_cubes(self):
        basic_symmetry_cubes = [
            Cube(ROT_120_CP, ROT_120_CO, ROT_120_EP, ROT_120_EO),
            Cube(ROT_90_CP,  ROT_90_CO,  ROT_90_EP,  ROT_90_EO ),
            Cube(ROT_180_CP, ROT_180_CO, ROT_180_EP, ROT_180_EO),
            Cube(REFLECT_CP, REFLECT_CO, REFLECT_EP, REFLECT_EO),
        ]

        # 48 cubes will represent the 48 cube symmetries
        self.symmetry_cubes: list[Cube] = []
        cube = Cube()

        for i in range(48):
            self.symmetry_cubes.append(cube.spawn_child())
            cube.multiply(basic_symmetry_cubes[3])
            if (i + 1) %  2 == 0:
                cube.multiply(basic_symmetry_cubes[2])
            if (i + 1) %  4 == 0:
                cube.multiply(basic_symmetry_cubes[1])
            if (i + 1) % 16 == 0:
                cube.multiply(basic_symmetry_cubes[0])

    def _create_inversion_array(self):
        self.inversion_cubes: list[Cube] = []
        self.inversion_array = [0] * N_SYM

        for i in range(N_SYM):
            for j in range(N_SYM):
                cube = self.symmetry_cubes[i].spawn_child()
                cube.multiply_corners(self.symmetry_cubes[j])

                if all(cube.cp[i] == i for i in range(3)):
                    self.inversion_array[i] = j
                    break

        for i in self.inversion_array:
            self.inversion_cubes.append(self.symmetry_cubes[i])

    def _create_move_array(self):
        basic_move_cubes = [
            Cube(U_CP, U_CO, U_EP, U_EO),
            Cube(R_CP, R_CO, R_EP, R_EO),
            Cube(F_CP, F_CO, F_EP, F_EO),
            Cube(D_CP, D_CO, D_EP, D_EO),
            Cube(L_CP, L_CO, L_EP, L_EO)
        ]

        # These cubes represent all 18 cube moves
        self.move_cubes: list[Cube] = []
        self.move_array = [[0 for _ in range(N_SYM)] for _ in range(N_MOVE)]

        for i in range(5):
            cube = Cube()
            for _ in range(3):
                cube.multiply(basic_move_cubes[i])
                self.move_cubes.append(cube.spawn_child())

        for i in range(N_SYM):
            for j in range(N_MOVE):
                cube = self.symmetry_cubes[i].spawn_child()
                cube.multiply(self.move_cubes[j])
                cube.multiply(self.inversion_cubes[i])

                for k in range(N_MOVE):
                    if cube == self.move_cubes[k]:
                        self.move_array[j][i] = k
                        break


syms = Symmetries()
