from copy import copy
from typing import List
import argparse


class CSP:


    ########################################
    #                                      #
    #           Initialization             #
    #                                      #
    ########################################

    def __init__(self, piece, puzzle_sizes) -> None:
        self.new_piece = []
        self.puzzle_sizes = puzzle_sizes
        for i, item in enumerate(piece):
            self.new_piece += self.get_rotated_pieces(item, i)   

        self.result = []

    def get_rotated_pieces(self, piece, i):
        result = set()

        for j in range(0, 4):
            result.add((
                piece[(0+j) % 4],
                piece[(1+j) % 4],
                piece[(2+j) % 4],
                piece[(3+j) % 4],
            ))
        return map(lambda x : (x, i), result)


    ########################################
    #                                      #
    #     Constraint Modeling              #
    #                                      #
    ########################################

    def init_domain(self):
        return [[[i for i in range(len(self.new_piece))] 
                      for _ in range(self.puzzle_sizes[1])] 
                        for _ in range(self.puzzle_sizes[0])]

    def init_by_base(self, base):
        result = []

        for i in range(self.puzzle_sizes[0]):
            result.append([])
            for j in range(self.puzzle_sizes[1]):
                try:
                    result[i].append([
                        index for index, item in enumerate(self.new_piece) if item[1] == base[i][j] - 1
                    ])
                except IndexError:
                    result[i].append([
                        i for i in range(len(self.new_piece))
                    ])

        return result

    def list_adj_by_domains(self, i, j, pos, matrix):
        return set(map(lambda x: self.new_piece[x][0][pos], matrix[i][j]))

    def limits_by(self, i, j, matrix):
        limits = [[0] for _ in range(4)] 
        
        if j - 1 >= 0:
            limits[0] = self.list_adj_by_domains(i, j-1, 2, matrix)
        if i - 1 >= 0:
            limits[1] = self.list_adj_by_domains(i-1, j, 3, matrix)
        if j + 1 < self.puzzle_sizes[1]:
            limits[2] = self.list_adj_by_domains(i, j+1, 0, matrix)
        if i + 1 < self.puzzle_sizes[0]:
            limits[3] = self.list_adj_by_domains(i+1, j, 1, matrix)
        
        return limits
    
    def filter_piece(self, limits, exclude):
        def f(index):
            if not exclude is None and self.new_piece[index][1] == exclude:
                return False

            result = True
            for i in range(4):
                result &= self.new_piece[index][0][i] in limits[i]
            return result
        return f

    ########################################
    #                                      #
    #     Constraint Propagation           #
    #                                      #
    ########################################

    def constraint_propagation(self, matrix_domain, indexes = (-1, -1), exclude = None):
        i, j = 0, 0
        while len(matrix_domain) > i:
            row = matrix_domain[i]
            while len(row) > j:
                if (i, j) == indexes: 
                    j += 1
                    continue
                matrix_domain[i][j] = list(filter(
                    self.filter_piece(
                        self.limits_by(i,j, matrix_domain),
                        exclude
                    ),
                    row[j]
                ))

                assert len(matrix_domain[i][j]) != 0

                j += 1
        
            i, j = i+ 1, 0
        
        return matrix_domain

    ########################################
    #                                      #
    #     Backtracking                     #
    #                                      #
    ########################################
    def deep_clone(self, matrix):
        return [[copy(matrix[i][j]) 
                    for j in range(self.puzzle_sizes[1])] 
                    for i in range(self.puzzle_sizes[0])]

    def select_next_val(self, matrix_domain):
        pivot = float('inf')
        indexes = self.puzzle_sizes

        for i, row in enumerate(matrix_domain):
            for j, item in enumerate(row):
                if len(item) > 1 and len(item) < pivot:
                    pivot = len(item)
                    indexes = (i, j)
        
        return indexes

    def find(self, base = None):
        if base is None:
            matrix = self.init_domain()
        else:
            matrix = self.init_by_base(base)

        matrix = self.constraint_propagation(matrix)
        matrix[0][0] = [min(matrix[0][0])]
        selected_piece = self.new_piece[matrix[0][0][0]][1]
        matrix = self.constraint_propagation(matrix, (0, 0), exclude=selected_piece)

        self._find(matrix)
        result = self.result
        self.result = []
        return result

    def _find(self, matrix_domains, indexes = (0, 0)):
        if indexes == self.puzzle_sizes:
            self.result.append(matrix_domains)
            return

        # next_index = self.next_indexes(indexes)
        for piece in matrix_domains[indexes[0]][indexes[1]]:
            new_matrix = self.deep_clone(matrix_domains)
            new_matrix[indexes[0]][indexes[1]] = [piece]
            selected_piece = self.new_piece[piece][1]

            try:
                new_matrix = self.constraint_propagation(new_matrix, indexes, exclude=selected_piece)
                next_index = self.select_next_val(new_matrix)
                self._find(new_matrix, next_index)
            except AssertionError:
                continue

    ########################################
    #                                      #
    #     Printers                         #
    #                                      #
    ########################################

    def print_result(self, result):
        for row in result:
            for index in row:
                print(self.new_piece[index[0]][1] + 1, end=' ')
            print()
        print()
    
    def print_puzzle(self, result):
        matrix = [[ " "
                    for j in range(self.puzzle_sizes[1] * 3)] 
                    for i in range(self.puzzle_sizes[0] * 3)]

        for i, row in enumerate(result):
            for j, item in enumerate(row):
                i_center = i * 3 + 1
                j_center = j * 3 + 1

                matrix[i_center][j_center-1] = f'\x1b[{31}m{self.new_piece[item[0]][0][0]}\x1b[0m'
                matrix[i_center-1][j_center] = f'\x1b[{31}m{self.new_piece[item[0]][0][1]}\x1b[0m'
                matrix[i_center][j_center + 1] = f'\x1b[{31}m{self.new_piece[item[0]][0][2]}\x1b[0m'
                matrix[i_center+1][j_center] = f'\x1b[{31}m{self.new_piece[item[0]][0][3]}\x1b[0m'
               

        for row in matrix:
            for item in row:
                print(item, end=' ')
            print()
        print()


parser = argparse.ArgumentParser()
parser.add_argument('file', type=str)
parser.add_argument('--base', type=str, required=False)
parser.add_argument('--pretty', type=bool, required=False)
args = parser.parse_args()

assert args.file

with open(args.file, 'r') as f:
    w, h = list(map(int, f.readline().split()))

    piece : List[List[int]] = [None] * (w * h)
    for i in range(w * h):
        piece[i] = list(map(int,f.readline().split()))

    f.close()

base = None

if args.base:
    with open(args.base, 'r') as f:
        lines = list(map(int, f.readline().split()))[0]
        base = [None] * lines
        for i in range(lines):
            base[i] = list(map(int,f.readline().split()))
    
        f.close()    

csp = CSP(piece, (h, w))
for r in csp.find(base):
    csp.print_result(r) 
    if args.pretty:
        csp.print_puzzle(r)