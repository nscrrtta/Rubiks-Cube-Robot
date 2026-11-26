from GUI.constants import CUBIE_DICT, FACE_INDICES, CORNER_INDICES, EDGE_INDICES
from GUI.cubie import Cubie, Facelet

from shapely.geometry import Point
import math


Vector = tuple[float, float, float]

# Flattened 3x3 matrix
Matrix = tuple[float, float, float, float, float, float, float, float, float]


class Cube:

    def __init__(self):
        # Keep track of x,y,z coordinate system within cube
        # Faces rotate around these axes
        self.x_vector: Vector = (1.0, 0.0, 0.0)
        self.y_vector: Vector = (0.0,-1.0, 0.0)
        self.z_vector: Vector = (0.0, 0.0, 1.0)

        # 26 cubies (6-sided sub-cubes, some sides are inward facing)
        self.cubies = [Cubie(key, val) for key, val in CUBIE_DICT.items()]
        self.update_cubies()

        # Polygons that are drawn / clicked
        self.facelets: list[Facelet] = []
        for cubie in self.cubies:
            self.facelets.extend(cubie.facelets)

        # Rotate so looking at URF corner
        a, b = -math.pi/4, -math.asin(math.sqrt(1/3))
        self.rotate_cube(a, (0.0, 1.0, 0.0))
        self.rotate_cube(b, (1.0, 0.0, 0.0))

        # Remember the current state of axis vectors
        self.x_axis = self.x_vector
        self.y_axis = self.y_vector
        self.z_axis = self.z_vector

        self.sort_facelets()

    def update_cubies(self):
        """Define which cubies belong to each face."""
        self.cubies_dict = {
            key: [self.cubies[i] for i in val]
            for key, val in FACE_INDICES.items()
        }

    def swap_cubies(self, face: str, n: int):
        """After a move is made, rotate cubie objects within a face."""
        if face not in 'URFDLB':
            return
        for s1 in [CORNER_INDICES[face], EDGE_INDICES[face]]:
            a, b, c, d = s1
            w, x, y, z = s1[-n:] + s1[:-n] # Shift elements in s1 right n places

            self.cubies[a], self.cubies[b], self.cubies[c], self.cubies[d] = \
            self.cubies[w], self.cubies[x], self.cubies[y], self.cubies[z]

    def rotate_cubies(self, cubies: list[Cubie], theta: float, axis: Vector):
        """Rotate list of cubies about an axis by some angle theta."""
        rotation_matrix = self.get_rotation_matrix(theta, axis)
        for cubie in cubies:
            cubie.rotate(rotation_matrix)

    def rotate_cube(self, theta: float, axis: Vector):
        """Rotate entire cube about an axis by some angle theta."""
        rotation_matrix = self.get_rotation_matrix(theta, axis)
        for cubie in self.cubies:
            cubie.rotate(rotation_matrix)

        # Update internal coordinate system
        self.x_vector = self.rotate_point(self.x_vector, rotation_matrix)
        self.y_vector = self.rotate_point(self.y_vector, rotation_matrix)
        self.z_vector = self.rotate_point(self.z_vector, rotation_matrix)

    def update_facelet_indices(self) -> list[int]:
        """
        Determine which facelets belong to each face and update their indices accordingly.
        Ex: facelets on U face have indices 0...8
        """
        facelets: list[Facelet] = []
        axes = [self.y_vector, self.x_vector, self.z_vector] * 2

        # Caches
        normals: list[Vector | None] = [None] * 54
        indices = [0] * 54

        for cubies, axis in zip(self.cubies_dict.values(), axes):
            for cubie in cubies:
                for facelet in cubie.facelets:
                    # Inward-facing facelet
                    if facelet.index == -1:
                        continue
                    # Already visited this facelet
                    if indices[facelet.index]:
                        continue

                    # If not yet calculated normal of this facelet
                    normal = normals[facelet.index]
                    if normal is None:
                        normal = self.get_normal(facelet.points_3D)
                        normals[facelet.index] = normal

                    dot = self.get_dot_product(normal, axis)

                    if abs(round(dot)) == 1:
                        indices[facelet.index] = 1
                        facelets.append(facelet)
                        break

        colours = []
        for i, facelet in enumerate(facelets):
            colours.append(facelet.colour_index)
            facelet.index = i
        return colours

    def sort_facelets(self):
        """Sort facelets by min z value. Required for drawing / click detection."""
        self.facelets.sort(key=lambda f: f.min_z_value)

    def get_clicked_facelet(self, x: int, y: int) -> Facelet | None:
        point = Point(x, y)
        for i in range(len(self.facelets) - 1, -1, -1):
            facelet = self.facelets[i]
            if facelet.index >= 0 and facelet.clicked(point):
                return facelet
        return None

    ### Math related methods ###

    def get_URF_rotation_matrix(self) -> Matrix:
        """Return rotation matrix that rotates cube to URF orientation."""

        # Align x_vector with x_axis and y_vector with y_axis
        z_curr = self.get_cross_product(self.x_vector, self.y_vector)
        z_dest = self.get_cross_product(self.x_axis, self.y_axis)

        curr_matrix: Matrix = (*self.x_vector, *self.y_vector, *z_curr)

        # Use zip() to create transpose of matrix
        dest_matrix: Matrix = tuple(n for v in zip(self.x_axis, self.y_axis, z_dest) for n in v)

        return self.multiply_3x3_matrices(dest_matrix, curr_matrix)

    def get_DLB_rotation_matrix(self) -> Matrix:
        """Return rotation matrix that rotates cube to DLB orientation."""

        # Get rotation matrix that rotates cube to URF orientation
        r1 = self.get_URF_rotation_matrix()

        # Get rotation matrix that rotates cube 180 degrees about x-axis
        r2 = self.get_rotation_matrix(math.pi, (1.0, 0.0, 0.0))
        
        # Multiply the two matrices together
        return self.multiply_3x3_matrices(r2, r1)

    def get_rotation_matrix(self, theta: float, axis: Vector) -> Matrix:
        """Return values of rotation matrix defined by an angle and axis of rotation."""
        ux, uy, uz = axis

        sin_t = math.sin(theta)
        cos_t = math.cos(theta)
        one_minus_cos_t = 1 - cos_t

        return (
            ux*ux*one_minus_cos_t + cos_t,
            ux*uy*one_minus_cos_t - uz*sin_t,
            ux*uz*one_minus_cos_t + uy*sin_t,

            uy*ux*one_minus_cos_t + uz*sin_t,
            uy*uy*one_minus_cos_t + cos_t,
            uy*uz*one_minus_cos_t - ux*sin_t,

            uz*ux*one_minus_cos_t - uy*sin_t,
            uz*uy*one_minus_cos_t + ux*sin_t,
            uz*uz*one_minus_cos_t + cos_t
        )

    def rotate_point(self, point: Vector, rotation_matrix: Matrix) -> Vector:
        """Rotate a point in 3D space about an axis defined by a rotation matrix."""
        x, y, z = point; a, b, c, d, e, f, g, h, i = rotation_matrix
        return x*a + y*b + z*c, x*d + y*e + z*f, x*g + y*h + z*i

    def get_normal(self, points: list[Vector]) -> Vector:
        """Return normal vector of plane defined by 4 points in 3D space."""
        p1, p2, p3, _ = points
        v1 = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
        v2 = (p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2])
        return self.get_cross_product(v1, v2)

    def get_dot_product(self, v1: Vector, v2: Vector) -> float:
        """Return dot product of two 1x3 vectors."""
        return sum(v1[i] * v2[i] for i in range(3))

    def get_cross_product(self, v1: Vector, v2: Vector) -> Vector:
        """Return cross product of two 1x3 vectors."""
        ax, ay, az = v1; bx, by, bz = v2
        return ay*bz - az*by, az*bx - ax*bz, ax*by - ay*bx

    def multiply_3x3_matrices(self, m1: Matrix, m2: Matrix) -> Matrix:
        """Multiply two 3x3 matrices stored as 1D arrays."""
        return tuple(
            sum(m1[i*3 + k] * m2[k*3 + j] for k in range(3))
            for i in range(3) for j in range(3)
        )

    def extract_theta_axis(self, rotation_matrix: Matrix) -> tuple[float, Vector]:
        """Extract angle and axis from a rotation matrix."""
        diagonal = [rotation_matrix[i] for i in [0, 4, 8]]

        trace = sum(diagonal)
        x = (trace - 1) / 2
        x = min(max(x, -1), 1)
        angle = math.acos(x)
        threshold = 0.025

        # 0° rotation
        if angle < threshold:
            return 0.0, (1.0, 0.0, 0.0)

        # 180° rotation
        if abs(angle - math.pi) < threshold:
            i = diagonal.index(max(diagonal)) # {0,1,2}
            m = math.sqrt(2 * (diagonal[i] + 1))
            x, y, z = (m / 2 if j == i else rotation_matrix[i*3+j] / m for j in range(3))
            return angle, (x, y, z)

        # Normal rotations
        a = 2 * math.sin(angle)
        axis = (
            (rotation_matrix[7] - rotation_matrix[5]) / a,
            (rotation_matrix[2] - rotation_matrix[6]) / a,
            (rotation_matrix[3] - rotation_matrix[1]) / a
        )
        return angle, axis
