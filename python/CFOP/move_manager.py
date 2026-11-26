from CFOP.constants import OPPOSITES, SEQUENCE


class MoveManager:

    @staticmethod
    def reduce_moves(moves: list[str]) -> list[str]:
        stack = []
        for move in moves:
            stack.append([move[0], int(move[1])])

            i = len(stack) - 2
            while i >= 0:
                if stack[i][0] == stack[-1][0]:
                    stack[i][1] += stack.pop()[1]
                    stack[i][1] %= 4
                    if stack[i][1] == 0:
                        del stack[i]
                    i = len(stack) - 2 # restart
                elif stack[i][0] == OPPOSITES[stack[-1][0]]:
                    i -= 1
                else: break

        return [f'{face}{turns}' for face, turns in stack]

    @staticmethod
    def replace_u_moves(moves: list[str]) -> list[str]:
        replaced = []
        for move in moves:
            if move[0] != 'U':
                replaced.append(move)
            else:
                seq = SEQUENCE + ['D' + move[1]] + SEQUENCE
                replaced.extend(seq)
        return replaced
