from os import path
import cv2


def screenshot():
    pth = path.dirname(path.abspath(__file__))
    import mss
    mss.mss().shot(output=path.join(pth, 'resources', "screenshot.PNG"))


def open_image(IMG_NAME):
    pth = path.dirname(path.abspath(__file__))
    img = cv2.imread(path.join(pth, 'resources', IMG_NAME))
    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return rgb_image


def writeinfile(X, Y, center, IMG_NAME):
    pth = path.dirname(path.abspath(__file__))
    with open(path.join(pth, 'resources', "header.txt")) as f:
        s = f.read()
    res = path.join(pth, 'resources', "{}.FDF".format(IMG_NAME[:-4]))
    with open(res, 'w') as f:
        f.write(s)
        f.write('\r\n')
        f.write("""   30000    5050""" + '\r\n')
        for i in range(len(X)):
            ss = ' ' * (8 - len(str(X[i]))) + str(X[i]) + \
                ' ' * (8 - len(str(Y[i]))) + str(Y[i])
            f.write(ss + '\r\n')
        f.write("""   30000    5050""")


def generate_txt(WEDGE_X, WEDGE_Y, X, Y, CENTER):
    pth = path.dirname(path.abspath(__file__))
    with open(path.join(pth, 'resources', "header2.txt")) as f:
        s = f.read()
    res = path.join(pth, 'resources', "RESULT.txt")
    with open(res, 'w') as f:
        f.write(s)
        f.write('\r\n')
        f.write(r"# {0} {1} {2} {3}".format(
            WEDGE_Y[0], WEDGE_Y[1], WEDGE_X[0], WEDGE_X[1]))
        f.write("\r\n")
        f.write(r"*")
        f.write("\r\n")
        f.write("""30000    150\r\n""")
        for i in range(len(X)):
            ss = str(X[i]) + '   ' + str(Y[i])
            f.write('{}\r\n'.format(ss))
        f.write("""30000    150""")


if __name__ == "__main__":
    IMG_NAME = "1.PNG"
    if open_image(IMG_NAME).any():
        print("works")
    screenshot()
