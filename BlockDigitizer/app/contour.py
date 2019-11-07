import cv2
import tkinter
import numpy as np
from sys import setrecursionlimit
import common_functions as cf


def get_contour(contour_mask):
    "Будем возвращать только один контур. Потому что косяков быть не должно"
    img = (contour_mask * 200).astype("uint8")
    gray_image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    contours, _ = cv2.findContours(
        gray_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print("Найдено контуров: {0}".format(len(contours)))
    cnt = contours[0]
    epsilon = 0.001 * cv2.arcLength(cnt, True)
    approx = (cv2.approxPolyDP(cnt, epsilon, True))

    img = cv2.drawContours(img, [approx], 0, (0, 255, 0), 1)
    cf.show_image(img)

    return approx[:, 0, :]


def draw_lines(img, wx, wy, scale):
    img = img * 200
    "Сначала получим значение цвета маски в виде кортежа"
    color = tuple(np.amax(img, axis=(0, 1)).tolist())
    "Координаты ненулевых точек"
    nzx, nzy = img[:, :, 0].nonzero()[0], img[:, :, 0].nonzero()[1]
    cutcenter = [nzx[nzx.argmin()], nzy[nzx.argmin()]]
    "Отступим влево и вправо на расстояние масштаба"
    for i in range(scale):
        if (cutcenter[1] - scale - i) in nzy:
            xarr = nzx[np.where(nzy == (cutcenter[1] - scale - i))]
            """Квадрат нужен, чтобы игнорировать знак -, если он есть"""
            leftxy = (xarr[np.argmin((cutcenter[0] - xarr)**2)],
                      cutcenter[1] - scale - i)
            break
        if i == (scale - 1):
            print("Не могу выпилить")

    for i in range(scale):
        if (cutcenter[1] + scale + i) in nzy:
            xarr = nzx[np.where(nzy == (cutcenter[1] + scale + i))]
            """Квадрат нужен, чтобы игнорировать знак -, если он есть"""
            rightxy = (xarr[np.argmin((cutcenter[0] - xarr)**2)],
                       cutcenter[1] + scale + i)
            break
        if i == (scale - 1):
            print("Не могу выпилить")
    print((leftxy[1], leftxy[0]), (leftxy[1], (np.min(wx) - scale)))
    cv2.line(img, (leftxy[1], leftxy[0]),
             (leftxy[1], np.min(wx) - scale), color, 2)
    cv2.line(img, (rightxy[1], rightxy[0]),
             (rightxy[1], np.min(wx) - scale), color, 2)
    "Рисуем квадрат с отступом от створок в размере масштаба"
    cv2.rectangle(img, (np.min(wy) - scale, np.min(wx) - scale),
                  (np.max(wy) + scale, np.max(wx) + scale), color, 2)
    """wx тут отвечает за горизонтальные створки.
    Будем выпиливать часть, которая выше всего."""
    "Теперь нужно обнулить часть контура, которая в выпиле"
    img[np.min(wx) - scale - 5:min(leftxy[0], rightxy[0]) + 25,
        leftxy[1] + 1:rightxy[1] - 1] = np.array([0, 0, 0], dtype="int32")
    return img


def simple_fill(array):
    setrecursionlimit(999999999)
    copy, newColor, oldColor = array.copy(), np.amax(
        array, axis=(0, 1)), np.amin(array, axis=(0, 1))
    Xmax, Ymax, _ = array.shape

    def fill(x, y, counter):
        if (copy[x, y] == oldColor).all() and (0 <= y < Ymax):
            leftborder, i = x, 0
            while (0 <= (x + i) < Xmax) and (copy[x + i, y] == oldColor).all():
                leftborder = x + i
                i -= 1
            rightborder, i = x, 0
            while (0 <= (x + i) < Xmax) and (copy[x + i, y] == oldColor).all():
                rightborder = x + i
                i += 1
            copy[leftborder:rightborder + 1, y] = newColor
            for i in range(leftborder, rightborder):
                if 0 < y < (Ymax - 1):
                    fill(i, y + 1, counter)
                    fill(i, y - 1, counter)

    fill(1, 1, 0)
    return copy


def fix_contour(axemask, contour, wx, wy):
    """Убирает дырки в контуре, получающиеся из-за пикселей с координатными осями"""
    holes = []
    newColor, oldColor = np.amax(contour, axis=(
        0, 1)), np.amin(contour, axis=(0, 1))

    def distance(ar0, ar1):
        return int(((ar1[0] - ar0[0])**2 + (ar1[1] - ar0[1])**2)**0.5)
    anz, cnz = axemask[:, :, 0].nonzero(), contour[:, :, 0].nonzero()
    anz, cnz = np.array([anz[0], anz[1]], dtype="int32").transpose(
    ), np.array([cnz[0], cnz[1]], dtype="int32").transpose()
    "Не будем учитывать заведомо отдалённые участки маски осей"
    anz1 = anz[:, 0].clip(wx[0] - 3, wx[1] - 3)
    anz2 = anz[:, 1].clip(wy[0] - 3, wy[1] - 3)
    anz = np.array([anz1, anz2], dtype="int32").transpose()
    print(anz.shape)
    return contour


def fix_contour1(contour):
    contour = contour.copy()  # Ну на всякий пожарный

    def minimask(pnt):
        minimask = contour[point[0] - 1:point[0] +
                           2, point[1] - 1:point[1] + 2]
        minimask = minimask[:, :, 0]
        return minimask
    newColor, oldColor = np.amax(contour, axis=(
        0, 1)), np.amin(contour, axis=(0, 1))
    cnz = contour[:, :, 0].nonzero()
    cnz = list(np.array([cnz[0], cnz[1]], dtype="int32").transpose())
    stranges = []
    for point in cnz:
        mm = minimask(point)
        "В условие нельзя ставить какой-то порог, поскольку не всегда унадаешь с толщиной"
        stranges.append([mm.sum(), point])
    stranges = sorted(stranges, key=lambda x: x[0])
    """Теперь нужно как-то отобрать те случаи, в которых действительно есть разрыв.
    Полагаю, можно начать с того, что будем называть разрывом ситуацию, когда невозможно
    попасть из одной части матрицы в другую."""
    for point in stranges:
        pnt = point[1]
        mm = contour[point[1][0] - 3:point[1][0] +
                     4, point[1][1] - 3:point[1][1] + 4]
        nz = mm[:, :, 0].nonzero()
        oldColor = mm[3, 3]  # Это, собственно, и есть point
        newColor = np.array([255, 0, 0], dtype="int32")
        mm = fill8(mm, [3, 3], oldColor, newColor)
        if oldColor[0] in mm:
            """Заделывать дырки, пожалуй, нужно сразу в цикле. Это исключит добавление в набор поломанных точек
            тех точек, которые находятся в окрестности разрыва."""
            whites = np.asarray(cf.color_mask(mm, oldColor)[
                                :, :, 0].nonzero()).transpose()
            # Чтоб было сгруппировано по набору точек
            reds = np.asarray(cf.color_mask(mm, newColor)[
                              :, :, 0].nonzero()).transpose()
            dst = 9000
            for point in reds:
                for point1 in whites:
                    if cf.distance(point, point1) < dst:
                        dst = cf.distance(point, point1)
                        wc, rc = point1, point
            if (rc[0] - wc[0]) != 0:
                dx = (rc[0] - wc[0]) / abs(rc[0] - wc[0])
            else:
                dx = 0
            if (rc[1] - wc[1]) != 0:
                dy = (rc[1] - wc[1]) / abs(rc[1] - wc[1])
            else:
                dy = 0
            # Тут идёшь лесенкой и заполняешь всю хуйню
            while True:
                if (wc == rc).all():
                    break
                if wc[0] != rc[0]:
                    mm[wc[0], wc[1]] = newColor
                    wc[0] = wc[0] + dx
                if wc[1] != rc[1]:
                    mm[wc[0], wc[1]] = newColor
                    wc[1] = wc[1] + dy
            # Чтобы закрасить красное назад в белое
            mm = fill8(mm, [3, 3], newColor, oldColor)

            # Теперь поправленный mm засунем туда, где взяли
            contour[pnt[0] - 3:pnt[0] + 4, pnt[1] - 3:pnt[1] + 4] = mm
    return contour


def fill8(array, point, oldColor, newColor):
    setrecursionlimit(999999999)
    copy = array.copy()
    Xmax, Ymax, _ = array.shape

    def fill(x, y):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (0 <= (x + i) < Xmax) and (0 <= (y + j) < Ymax) and (copy[x + i, y + j] == oldColor).all():
                    copy[x + i, y + j] = newColor
                    fill(x + i, y + j)
    fill(point[0], point[1])
    return copy


def inverse_fill(matrix):
    copy = matrix.copy()
    t = np.where(copy != 0, 0, 1).astype("int32")
    return t


def rearrange(points, center):
    center = [center[0], center[1]]

    def distance(point1, point2):
        return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    distances = []
    for point in points:
        distances.append(distance(point, center))

    distances = np.array(distances, dtype="float32")
    kindafirst = np.argmin(distances)
    ordered = [center]
    for i in range(kindafirst, len(distances), 1):
        ordered.append(points[i].tolist())
    for i in range(kindafirst + 1):
        ordered.append(points[i].tolist())
    ordered.append(center)
    return ordered


if __name__ == "__main__":
    import work_with_files as wwf
    img = wwf.open_image("TEST.png")
    img = fix_contour1(img)
    d = simple_fill(img)
    t = inverse_fill(d)
    get_contour(t)
