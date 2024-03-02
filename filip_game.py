import numpy as np
import copy
import matplotlib.pyplot as plt

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

def generate_tree(start, score_dist):

    children = start.create_children()

    if not children:
        score_dist.append(start.depth)
        return start
    
    for i in children:
        generate_tree(i, score_dist)


if __name__ == '__main__':

    N = 5

    M = 5

    a = np.zeros((N, M)) # grid of positions

    n = 3 # horizontal / vertical movements

    m = 2 # diagonal movements

    a[N - 1, 0] = 1

    root = Tree()

    root.data = a
    root.pos = np.array([3, 0])
    root.depth = 1

    root.straight = n
    root.diagonal = m

    score_dist = []

    generate_tree(root, score_dist)

    fig, ax = plt.subplots()
    lbl = '%dx%d grid with %d horizontal and %d diagonal moves' % (N, M, n, m)
    bns = [i + 0.5 for i in range(1, N * M + 1)]
    ax.hist(score_dist, bins = bns, label = lbl)
    ax.set_xlabel('score')
    ax.set_ylabel('counts')
    ax.legend()
    plt.show()