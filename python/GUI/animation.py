from CFOP.constants import OPPOSITES

from GUI.constants import *
from GUI.renderer import Renderer
from GUI.cube import Cube, Vector
from GUI.cubie import Cubie

import math
if USE_MOTORS:
    import zmq


class Animation:

    def __init__(self, cube: Cube, renderer: Renderer):
        self.cube = cube
        self.renderer = renderer

        # Moves that are made (one per while loop iteration)
        self.moves: list[str] = []
        self.motors_enabled = False

        # For sending messages to motors.py
        self.context = self.socket = None
        if USE_MOTORS:
            self.context = zmq.Context()
            self.socket = self.context.socket(zmq.PAIR)
            self.socket.setsockopt(zmq.LINGER, 0)
            self.socket.setsockopt(zmq.SNDTIMEO, 1000)
            self.socket.bind('tcp://localhost:5555')

    def _send_msg_to_motors(self, msg: dict):
        if self.socket is None:
            return
        try:
            self.socket.send_pyobj(msg)
        except Exception as e:
            print(f'[ERROR] Could not send message to motors: {msg} | {e}')

    ### Moves ###

    def make_next_move(self):
        if not self.motors_enabled:
            self._send_msg_to_motors({'pin_state': 0})
            self.motors_enabled = True

        move1, move2 = self.moves.pop(), 'X0'
        # Check if the next move can be done at the same time
        if self.moves and self.moves[-1][0] == OPPOSITES[move1[0]]:
            move2 = self.moves.pop()
        moves = move1[0], int(move1[1]), move2[0], int(move2[1])
        self._send_msg_to_motors({'moves': moves})
        self._animate_face_rotations(*moves)

    def abort(self):
        self.moves.clear()

    def disable_motors(self):
        self._send_msg_to_motors({'pin_state': 1})
        self.motors_enabled = False

    def close(self):
        self._send_msg_to_motors({'quit': True})
        if self.socket is not None:
            self.socket.close()
        if self.context is not None:
            self.context.term()

    ### Cube rotations ###

    def rotate_swipe(self, x1: int, y1: int, x2: int, y2: int):
        """Rotate the cube 90° for a swipe from (x1, y1) to (x2, y2)."""
        dx = x2 - x1
        dy = y2 - y1

        # Swipe must be at least 25 px long
        hypotenuse = math.sqrt(dx*dx + dy*dy)
        if hypotenuse < 25:
            return

        # Slope determines axis of rotation
        slope = dy / dx if dx != 0 else math.inf
        theta = math.pi / 2

        # Vertical swipe
        if abs(slope) > 4.0:
            if dy > 0: theta *= -1
            self._animate_cube_rotation(theta, (1.0, 0.0, 0.0), 2)

        # Horizontal swipe
        elif abs(slope) < 0.3:
            if dx > 0: theta *= -1
            self._animate_cube_rotation(theta, self.cube.y_axis)

        # Diagonal swipe bottom left to top right / top right to bottom left
        elif slope < 0:
            if dx < 0: theta *= -1
            self._animate_cube_rotation(theta, self.cube.x_axis)

        # Diagonal swipe top left to bottom right / bottom right to top left
        elif slope > 0:
            if dx < 0: theta *= -1
            self._animate_cube_rotation(theta, self.cube.z_axis)

    def rotate_drag(self, x1: int, y1: int, x2: int, y2: int):
        """Rotate the cube freely for a drag from (x1, y1) to (x2, y2)."""

        def pos_to_sphere(x: int, y: int) -> Vector:
            x = (x - ORIGIN_X) / 500
            y = (y - ORIGIN_Y) / 500
            z = math.sqrt(1.0 - (x*x + y*y))
            return x, y, z

        prev_point = pos_to_sphere(x1, y1)
        curr_point = pos_to_sphere(x2, y2)

        axis = self.cube.get_cross_product(prev_point, curr_point)
        m = math.sqrt(sum(i*i for i in axis))

        if m <= 0.001:
            return

        axis = (axis[0] / m, axis[1] / m, axis[2] / m)
        angle = m * 2.0 # Sensitivity factor
        self.cube.rotate_cube(angle, axis)

        self.cube.sort_facelets()
        self.renderer.draw()

    def rotate_to_URF(self):
        rotation_matrix = self.cube.get_URF_rotation_matrix()
        theta, axis = self.cube.extract_theta_axis(rotation_matrix)
        if theta: self._animate_cube_rotation(theta, axis)

    def return_to_DLB(self):
        rotation_matrix = self.cube.get_DLB_rotation_matrix()
        theta, axis = self.cube.extract_theta_axis(rotation_matrix)
        if theta: self._animate_cube_rotation(theta, axis)

    ### Animation loops ###

    def _animate_face_rotations(self, f1: str, n1: int, f2: str, n2: int):
        """Rotate face 1 (f1) n1 times, rotate face 2 (f2) n2 times."""

        def get_num_steps(turns: int) -> int:
            if turns % 2:
                return STEPS_FACE_ROTATION
            return STEPS_FACE_ROTATION * turns

        def get_theta(face: str, turns: int) -> float:
            theta = (math.pi/2) / STEPS_FACE_ROTATION
            if face in 'DLB':
                theta *= -1
            if turns == 3:
                theta *= -1
            return theta

        def get_axis(face: str) -> Vector:
            if face in 'RL':
                return self.cube.x_vector
            if face in 'UD':
                return self.cube.y_vector
            if face in 'FB':
                return self.cube.z_vector
            return (0.0, 0.0, 0.0)

        def get_cubies(face: str) -> list[Cubie]:
            if face not in 'URFDLB':
                return []
            return self.cube.cubies_dict[face]

        # Move 1 values
        axis_i   = get_axis(f1)
        cubies_i = get_cubies(f1)
        steps_i  = get_num_steps(n1)
        theta_i  = get_theta(f1, n1)

        # Move 2 values
        axis_j   = get_axis(f2)
        cubies_j = get_cubies(f2)
        steps_j  = get_num_steps(n2)
        theta_j  = get_theta(f2, n2)

        # While loop for animation
        while steps_i or steps_j:
            if steps_i:
                steps_i -= 1
                self.cube.rotate_cubies(cubies_i, theta_i, axis_i)
            if steps_j:
                steps_j -= 1
                self.cube.rotate_cubies(cubies_j, theta_j, axis_j)
            self.cube.sort_facelets()
            self.renderer.draw()

        self.cube.swap_cubies(f1, n1)
        self.cube.swap_cubies(f2, n2)
        self.cube.update_cubies()

    def _animate_cube_rotation(self, theta: float, axis: Vector, n: int = 1):
        for _ in range(STEPS_CUBE_ROTATION * n):
            self.cube.rotate_cube(theta / STEPS_CUBE_ROTATION, axis)
            self.cube.sort_facelets()
            self.renderer.draw()
