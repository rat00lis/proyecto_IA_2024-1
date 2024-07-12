import math


def get_histograms(board):
    xhisto = [0, 0, 0, 0]
    yhisto = [0, 0, 0, 0]

    for x in range(0, 4):
        for y in range(0, 4):
            if board[x][y]:
                xhisto[y] += math.log(board[x][y], 2)
                yhisto[x] += math.log(board[x][y], 2)

    return (xhisto, yhisto)

def get_features_limits():
    features_limits = []
    for i in range(0, 8):
        features_limits.append([0, 40])
#    for i in range(0, 5):
#        features_limits.append([0, 0])
    return features_limits

def extract_features(board):
    # Dim(set) = 13
    features = []

    # Vertical/horizontal density extraction
    # Dim = 8
    (xdensity, ydensity) = get_histograms(board)
    for density in xdensity:
        features.append(density)
    for density in ydensity:
        features.append(density)

    return features
