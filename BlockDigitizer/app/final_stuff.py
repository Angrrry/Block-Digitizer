def transform_coords(points, center, scale):
    X, Y = [], []
    for i in range(len(points)):
        X.append(int(100 * (points[i][0] - center[0]) // scale))
        Y.append(int(100 * (center[1] - points[i][1]) // scale))
    return X, Y


if __name__ == "__main__":
    writeinfile([1], [5], 3)
