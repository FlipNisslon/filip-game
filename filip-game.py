import numpy as np
import copy
import matplotlib.pyplot as plt

N = 4

M = 4

a = np.zeros((N, M)) # grid of positions

n = 3 # horizontal / vertical movements

m = 2 # diagonal movements

class Tree(object):
    def __init__(self):
        self.children_directions = []
        self.children = []

        self.data = None
        self.pos = None
        self.depth = None

        self.straight = None
        self.diagonal = None

    def __str__(self):
        return str(self.data)

    def create_children(self):
        allowed = self.allowed_movements()
        for i in allowed:
            
            tmp = copy.copy(self.data)
            self.children_directions.append(i)
            child = Tree()
            child.pos = self.pos + i
            child.depth = self.depth + 1
            tmp[tuple(self.pos + i)] = self.depth + 1
            child.data = tmp

            child.straight = self.straight
            child.diagonal = self.diagonal


            self.children.append(child)

        return self.children


    def allowed_movements(self):
        mat = self.data
        pos = self.pos
        straight = self.straight
        diagonal = self.diagonal

        # eight combinations to check
        down = np.array([straight, 0])
        right = np.array([0, straight])
        up = np.array([-straight, 0])
        left = np.array([0, -straight])

        down_right = np.array([diagonal, diagonal])
        up_right = np.array([-diagonal, diagonal])
        up_left = np.array([-diagonal, -diagonal])
        down_left = np.array([diagonal, -diagonal])

        dirs = [up, up_right, right, down_right, down, down_left, left, up_left]

        # movements are not allowed if matrix is out of bounds or there is a number in that position

        # check if movement puts us out of bounds

        allowed = []

        (N, M) = mat.shape

        for i in dirs:
            if pos[0] + i[0] < 0 or pos[0] + i[0] >= N:
                pass 
            elif pos[1] + i[1] < 0 or pos[1] + i[1] >= M:
                pass
            elif mat[tuple(pos + i)] == 0:
                allowed.append(i)
        
        return allowed

def generate_tree(start):

    children = start.create_children()

    if not children:
        fig, ax = plt.subplots()
        ax.imshow(start.data, vmin = 0, vmax = 16)
        ax.set_title('score: ' + str(start.depth))
        return start
    
    for i in children:
        generate_tree(i)


a[N - 1, 0] = 1

root = Tree()

root.data = a
root.pos = np.array([3, 0])
root.depth = 1

root.straight = 3
root.diagonal = 2

generate_tree(root)

plt.show()