from Kociemba.constants import *


class Cube:

    def __init__(
            self,
            cp: list[int] = [i for i in range(8)],  # Corner permutations
            co: list[int] = [0 for _ in range(8)],  # Corner orientations
            ep: list[int] = [i for i in range(12)], # Edge permutations
            eo: list[int] = [0 for _ in range(12)]  # Edge orientations
        ):
        self.cp = cp[:]
        self.co = co[:]
        self.ep = ep[:]
        self.eo = eo[:]

    def __eq__(self, other: object) -> bool:
        cube: Cube = other
        return (self.cp == cube.cp
            and self.co == cube.co
            and self.ep == cube.ep
            and self.eo == cube.eo
        )

    def spawn_child(self) -> 'Cube':
        return Cube(self.cp, self.co, self.ep, self.eo)

    def multiply_corners(self, other: 'Cube'):
        """
        Multiply this cube with another cube, restricted to the corners.
        Does not change other cube.
        """
        cube: Cube = other
        permutation_c = [0] * 8
        orientation_c = [0] * 8

        for i in range(8):
            orientation_a = self.co[cube.cp[i]]
            orientation_b = cube.co[i]

            # Two regular cubes
            if orientation_a < 3 and orientation_b < 3:
                orientation = orientation_a + orientation_b
                if orientation >= 3:
                    orientation -= 3

            # Cube b is in a mirrored state
            elif orientation_a < 3 <= orientation_b:
                orientation = orientation_a + orientation_b
                # The composition is also in a mirrored state
                if orientation >= 6:
                    orientation -= 3

            # Cube a is in a mirrored state
            elif orientation_a >= 3 > orientation_b:
                orientation = orientation_a - orientation_b
                # The composition is also in a mirrored state
                if orientation < 3:
                    orientation += 3

            # Both cubes are in mirrored states
            elif orientation_a >= 3 and orientation_b >= 3:
                orientation = orientation_a - orientation_b
                # The composition is a regular cube
                if orientation < 0:
                    orientation += 3

            permutation_c[i] = self.cp[cube.cp[i]]
            orientation_c[i] = orientation

        self.cp = permutation_c
        self.co = orientation_c

    def multiply_edges(self, other: 'Cube'):
        """
        Multiply this cube with another cube, restricted to the edges.
        Does not change other cube.
        """
        cube: Cube = other
        permutation_e = [0] * 12
        orientation_e = [0] * 12

        for i in range(12):
            permutation_e[i] = self.ep[cube.ep[i]]
            orientation_e[i] = (cube.eo[i] + self.eo[cube.ep[i]]) % 2

        self.ep = permutation_e
        self.eo = orientation_e

    def multiply(self, b: 'Cube'):
        self.multiply_corners(b)
        self.multiply_edges(b)

    def get_twist(self) -> int:
        """Get the twist of the 8 corners. 0 <= twist < 2187 in phase 1, twist = 0 in phase 2"""
        ret = 0
        for i in range(7):
            ret = 3 * ret + self.co[i]
        return ret

    def get_flip(self) -> int:
        """Get the flip of the 12 edges. 0 <= flip < 2048 in phase 1, flip = 0 in phase 2"""
        ret = 0
        for i in range(11):
            ret = 2 * ret + self.eo[i]
        return ret

    def get_slice(self) -> int:
        """
        Get the location of the UD-slice edges FR, FL, BL and BR ignoring their permutation.
        0 <= slice < 495 in phase 1, slice = 0 in phase 2.
        """
        a = j = 0
        # Compute the index a < (12 choose 4)
        for i in range(11, -1, -1):
            if self.ep[i] >= 8:
                a += self._n_choose_k(11 - i, j + 1)
                j += 1
        return a

    def get_slice_sorted(self) -> int:
        """
        Get the permutation and location of the UD-slice edges FR, FL, BL and BR.
        0 <= slice_sorted < 11880 in phase 1,
        0 <= slice_sorted < 24 in phase 2,
        slice_sorted = 0 for solved cube.
        """
        a = j = 0
        edge4 = [0] * 4

        # First compute the index a < (12 choose 4) and the permutation array perm.
        for i in range(11, -1, -1):
            if self.ep[i] >= 8:
                a += self._n_choose_k(11 - i, j + 1)
                edge4[3 - j] = self.ep[i]
                j += 1

        # Then compute the index b < 4! for the permutation in edge4
        b = 0
        for i in range(3, 0, -1):
            j = 0
            while edge4[i] != i + 8:
                self._rotate_left(edge4, 0, i)
                j += 1
            b = (i + 1) * b + j

        return 24 * a + b

    def get_u_edges(self) -> int:
        """
        Get the permutation and location of edges UR, UF, UL and UB.
        0 <= u_edges < 11880 in phase 1,
        0 <= u_edges < 1680 in phase 2,
        u_edges = 1656 for solved cube.
        """
        a = j = 0

        edge4 = [0] * 4
        ep_mod = self.ep[:]

        for _ in range(4):
            self._rotate_right(ep_mod, 0, 11)

        # First compute the index a < (12 choose 4) and the permutation array perm.
        for i in range(11, -1, -1):
            if ep_mod[i] <= 3:
                a += self._n_choose_k(11 - i, j + 1)
                edge4[3 - j] = ep_mod[i]
                j += 1

        # Then compute the index b < 4! for the permutation in edge4
        b = 0
        for i in range(3, 0, -1):
            j = 0
            while edge4[i] != i:
                self._rotate_left(edge4, 0, i)
                j += 1
            b = (i + 1) * b + j

        return 24 * a + b

    def get_d_edges(self) -> int:
        """
        Get the permutation and location of the edges DR, DF, DL and DB.
        0 <= d_edges < 11880 in phase 1,
        0 <= d_edges < 1680 in phase 2,
        d_edges = 0 for solved cube.
        """
        a = j = 0

        edge4 = [0] * 4
        ep_mod = self.ep[:]

        for _ in range(4):
            self._rotate_right(ep_mod, 0, 11)

        # First compute the index a < (12 choose 4) and the permutation array perm.
        for i in range(11, -1, -1):
            if 4 <= ep_mod[i] <= 7:
                a += self._n_choose_k(11 - i, j + 1)
                edge4[3 - j] = ep_mod[i]
                j += 1

        # Then compute the index b < 4! for the permutation in edge4
        b = 0
        for i in range(3, 0, -1):
            j = 0
            while edge4[i] != i + 4:
                self._rotate_left(edge4, 0, i)
                j += 1
            b = (i + 1) * b + j

        return 24 * a + b

    def get_ud_edges(self) -> int:
        """
        Get the permutation of the 8 U and D edges.
        ud_edges undefined in phase 1,
        0 <= ud_edges < 40320 in phase 2,
        ud_edges = 0 for solved cube.
        """
        perm = self.ep[:8]
        a = 0

        for i in range(7, 0, -1):
            j = 0
            while perm[i] != i:
                self._rotate_left(perm, 0, i)
                j += 1
            a = (i + 1) * a + j

        return a

    def get_corners(self) -> int:
        """
        Get the permutation of the 8 corners.
        0 <= corners < 40320 defined but unused in phase 1,
        0 <= corners < 40320 in phase 2,
        corners = 0 for solved cube.
        """
        perm = self.cp[:]
        a = 0

        for i in range(7, 0, -1):
            j = 0
            while perm[i] != i:
                self._rotate_left(perm, 0, i)
                j += 1
            a = (i + 1) * a + j

        return a

    def _rotate_right(self, arr: list[int], left: int, right: int):
        """Rotate array arr right between left and right. Right is included"""
        temp = arr[right]
        for i in range(right, left, -1):
            arr[i] = arr[i - 1]
        arr[left] = temp

    def _rotate_left(self, arr: list[int], left: int, right: int):
        """Rotate array arr left between left and right. Right is included"""
        temp = arr[left]
        for i in range(left, right):
            arr[i] = arr[i + 1]
        arr[right] = temp

    def _n_choose_k(self, n: int, k: int) -> int:
        """Binomial coefficient [n choose k]"""
        if n < k:
            return 0
        if k > n // 2:
            k = n - k
        s, i, j = 1, n, 1
        while i != n - k:
            s *= i
            s //= j
            i -= 1
            j += 1
        return s
