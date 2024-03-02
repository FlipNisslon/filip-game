from filip_game import *

def starting_points(mat, n, m, ax):
    (N, M) = mat.shape

    center_row = N // 2 + 1
    center_column = M // 2 + 1

    win_grid = np.zeros((center_row, center_column))

    for i in range(center_row):
        for j in range(center_column):

            mat[i, j] = 1 # set starting position

            root = Tree()

            root.data = a
            root.pos = np.array([i, j])
            root.depth = 1

            root.straight = n
            root.diagonal = m

            score_dist = []

            generate_tree(root, score_dist)

            lbl = '[%d, %d]' % (i, j)
            bns = [i + 0.5 for i in range(1, N * M + 1)]
            ax.hist(score_dist, bins = bns, label = lbl, alpha = 0.5)

            win_grid[i, j] = sum(np.array(score_dist) == N * M)

            mat = np.zeros_like(mat)

    fig, ax2 = plt.subplots()
    scores = ax2.imshow(win_grid)
    ax2.set_xticks(np.arange(center_column))
    ax2.set_yticks(np.arange(center_row))
    fig.colorbar(scores, ax = ax2)

if __name__ == '__main__':

    fig, ax = plt.subplots()

    a = np.zeros((5, 5)) # grid of positions

    starting_points(a, 3, 2, ax)

    ax.legend()
    ax.set_xlabel('score')
    ax.set_ylabel('counts')

    plt.show()