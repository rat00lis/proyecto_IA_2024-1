import copy
import random

class matrix_2048:
    def __init__ (self):
        self.matrix = [[0] * 4 for _ in range(4)]
        self.add_number()
        self.add_number()
    
    def add_number(self):
        empty = []
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == 0:
                    empty.append((i, j))
        random_cell = random.choice(empty)
        random_number = random.randint(0,1)
        self.matrix[random_cell[0]][random_cell[1]] = 2 if random_number == 0 else 4

    def up(self):
        old_matrix = copy.deepcopy(self.matrix)
        for j in range(4):
            column = [self.matrix[i][j] for i in range(4)]
            column = [x for x in column if x != 0]
            column += [0] * (4 - len(column))
            for i in range(3):
                if column[i] == column[i+1]:
                    column[i] *= 2
                    column[i+1] = 0
            column = [x for x in column if x != 0]
            column += [0] * (4 - len(column))
            for i in range(4):
                self.matrix[i][j] = column[i]

        return old_matrix != self.matrix
    
    def down(self):
        old_matrix = copy.deepcopy(self.matrix)
        for j in range(4):
            column = [self.matrix[i][j] for i in range(4)]
            column = [x for x in column if x != 0]
            column = [0] * (4 - len(column)) + column
            for i in range(3, 0, -1):
                if column[i] == column[i-1]:
                    column[i] *= 2
                    column[i-1] = 0
            column = [x for x in column if x != 0]
            column = [0] * (4 - len(column)) + column
            for i in range(4):
                self.matrix[i][j] = column[i]
    
        return old_matrix != self.matrix
    
    def left(self):
        old_matrix = copy.deepcopy(self.matrix)
        for i in range(4):
            row = self.matrix[i]
            row = [x for x in row if x != 0]
            row += [0] * (4 - len(row))
            for j in range(3):
                if row[j] == row[j+1]:
                    row[j] *= 2
                    row[j+1] = 0
            row = [x for x in row if x != 0]
            row += [0] * (4 - len(row))
            self.matrix[i] = row
    
        return old_matrix != self.matrix
    
    def right(self):
        old_matrix = copy.deepcopy(self.matrix)
        for i in range(4):
            row = self.matrix[i]
            row = [x for x in row if x != 0]
            row = [0] * (4 - len(row)) + row
            for j in range(3, 0, -1):
                if row[j] == row[j-1]:
                    row[j] *= 2
                    row[j-1] = 0
            row = [x for x in row if x != 0]
            row = [0] * (4 - len(row)) + row
            self.matrix[i] = row
    
        return old_matrix != self.matrix
    
    def print_matrix(self):
        for row in self.matrix:
            print(row)