from CFOP.move_manager import MoveManager
from CFOP.constants import *
from CFOP.cube import Cube


class EdgeSolver:

    @staticmethod
    def find_paths(
            cube: Cube,
            find_one: bool,
            start_node: int,
            final_node: int,
            move_limit: int,
            prohibited: set[str],
        ) -> list[tuple[str, ...]]:

        current_moves: list[str] = []
        visited_nodes = set()
        paths = set()

        def search(curr_node: int):
            if len(current_moves) > move_limit:
                return
            if find_one and paths:
                return

            if curr_node == final_node:
                moves = tuple(MoveManager.reduce_moves(current_moves))
                if moves in paths:
                    return

                # Check if these moves solve edge
                child = cube.spawn_child()
                for move in moves:
                    child.make_move(move)
                if child.edge_solved(final_node):
                    paths.add(moves)
                return

            for node, move in EDGE_LINKS[curr_node].items():
                if node in visited_nodes or move in prohibited:
                    continue
                
                current_moves.append(move)
                visited_nodes.add(node)
                search(node)
                current_moves.pop()
                visited_nodes.remove(node)

        search(start_node)
        return sorted(paths, key=lambda moves: len(moves))
