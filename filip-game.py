import numpy as np

N = 4

M = 4

a = np.zeros((N, M)) # grid of positions

n = 3 # horizontal / vertical movements

m = 2 # diagonal movements

def allowed_movements(mat, pos, straight, diagonal):
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

def game(mat, pos, cnt, allowed):

    mat[tuple(pos)] = cnt

    if not allowed:
        print(mat)

    for i in allowed:
        oldmat = mat
        game(mat, pos + i, cnt + 1, allowed_movements(mat, pos + i, 3, 2))
        mat = oldmat

game(a, np.array([3, 0]), 1, allowed_movements(a, np.array([3, 0]), 3, 2))