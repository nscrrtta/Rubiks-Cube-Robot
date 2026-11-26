from shapely.geometry import Point, Polygon
from GUI.constants import *


Point3D = tuple[float, float, float]
Point2D = tuple[float, float]


class Cubie:

    def __init__(self, center: Point3D, indices: list[int]):
        # 6 facelets make up the 6 sides of this cubie
        # (Some facelets are inward facing)
        self.facelets = [Facelet(i) for i in indices]

        x, y, z = center
        d = 0.5

        # 8 corners of this cubie in 3D space
        self.points_3D = [
            (x-d, y-d, z-d), (x-d, y+d, z-d), (x+d, y+d, z-d), (x+d, y-d, z-d),
            (x-d, y-d, z+d), (x-d, y+d, z+d), (x+d, y+d, z+d), (x+d, y-d, z+d)
        ]

        # What indices of self.points_3D define each face of this cubie
        self.face_indices = [
            (0, 3, 7, 4), # U face
            (2, 3, 7, 6), # R face
            (4, 5, 6, 7), # F face
            (1, 2, 6, 5), # D face
            (0, 1, 5, 4), # L face
            (0, 1, 2, 3)  # B face
        ]

        for i, indices in enumerate(self.face_indices):
            self.facelets[i].update([self.points_3D[i] for i in indices])

    def rotate(self, rotation_matrix: list[float]):
        """Rotate the 8 corners of this cubie, then update each facelet."""
        for i in range(8):
            self.points_3D[i] = self._rotate_point(self.points_3D[i], rotation_matrix)
        for i, indices in enumerate(self.face_indices):
            self.facelets[i].update([self.points_3D[i] for i in indices])

    def _rotate_point(self, point: Point3D, rotation_matrix: list[float]) -> Point3D:
        """Rotate a point in 3D space about an axis defined by a rotation matrix."""
        x, y, z = point; a, b, c, d, e, f, g, h, i = rotation_matrix
        return x*a + y*b + z*c, x*d + y*e + z*f, x*g + y*h + z*i


class Facelet:

    def __init__(self, index: int):
        # Index of 1D array this facelet represents {0...53}
        # -1 if this facelet is inward facing
        self.index = index
        self.set_colour(index // 9)

    def update(self, points_3D: list[Point3D]):
        self.points_3D = points_3D

        # Convert points in 3D space to 2D space for drawing
        self.points_2D: list[Point2D] = [
            (x * CUBIE_SIZE + ORIGIN_X, y * CUBIE_SIZE + ORIGIN_Y)
            for x, y, _ in points_3D
        ]

        # For click detection
        self.polygon = Polygon(self.points_2D)

        # For drawing / click detection
        self.min_z_value = min(p[2] for p in points_3D)

    def set_colour(self, colour_index: int):
        self.colour_index = colour_index # {0...5}
        self.colour = RGB_VALUES[colour_index]

    def clicked(self, point: Point) -> bool:
        return point.within(self.polygon)
