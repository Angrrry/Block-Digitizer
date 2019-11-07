# -*- coding: utf-8 -*-
"""В этом модуле обнаруживаются оси и  выясняется масштаб.
При наличии поворота осей осуществляется обратный поворот изображения."""


"""Для нахождения угла поворота оси без подключения scipy можно сделать следующее:
Поворачивая в цикле маску осей на 1 градус вокруг предполагаемого центра, найти угол поворота,
при сумма количества точек вдоль осей X и Y будет максимальной. Для верности можно также потребовать, чтобы отличие максимального значения от
следующего за ним для этого угла также было бы максимальным."""




import cv2
import numpy as np
def get_rotation_angle(axe_mask):
    from common_functions import rotate_image
    angle_vals = np.zeros(90, dtype=int)
    coords = []
    for angle in range(90):
        """Cумма сумм "Массив суммы значений вдоль оси X"""
        rotatedmask = rotate_image(axe_mask, angle)
        angle_vals[angle] = np.max(rotatedmask.sum(
            axis=0)) + np.max(rotatedmask.sum(axis=1))
        """Тот ужас, который снизу, получился из-за того, что в матрице получается 3 значения, argmax без указания оси превращает массив в одномерный,
        поэтому выдаёт неверные индексы"""
        coords.append((rotatedmask.sum(axis=1).argmax(axis=0).max(),
                       rotatedmask.sum(axis=0).argmax(axis=0).max()))
    angle = np.argmax(angle_vals)
    "Это центр после поворота изображения, пусть и определяется заранее"
    center = coords[angle]
    scale = axeScale1(rotate_image(axe_mask, angle))
    return angle, center, scale


def get_scale(rotatedmask, center):
    "Надо переписать. Масштаб получается с большой погрешностью. Я бы не ограничивал область"
    max, mean, i = 100, 1, 0
    while max / mean > 20:
        rm = rotatedmask.sum(axis=1)[:center[0] - 5 * i]
        # снова проблемы из-за функции mask. Теперь rm- одномерный массив
        rm = rm[:, 1]
        max, mean = rm.max(), rm.mean()
        i += 1
    max21indexes = np.sort(rm.argsort()[-21:][::-1])
    mx0, mx1 = max21indexes[:-1], max21indexes[1:]
    scale = int(round((mx1 - mx0).mean()))
    return scale


def axeScale1(rotated_axe_mask):
    rotated_axe_mask = rotated_axe_mask[:, :, 0]
    sums = rotated_axe_mask.sum(axis=0)
    # Примитивный фильтр для малых значений
    sums = np.where(sums <= 2, 0, sums)
    nz = sums.nonzero()[0]
    _ = np.roll(nz, -1)  # смещает массив на 1 элемент
    difs = _[:-1] - nz[:-1]
    # Ну типа если у них масштаб меньше 5 пикселей, то это жопа
    difs = np.where(difs <= 5, 0, difs)
    difs = difs[difs.nonzero()[0]].tolist()  # Выбрасываем обнулённые значения
    from collections import Counter
    difs.sort(key=Counter(difs).get, reverse=True)
    _ = difs[0]
    difs = np.asarray(difs)
    # Чтобы учитывать 2 соседних пикселя
    difs = np.where((difs - _)**2 <= 4, difs, 0)
    difs = difs[difs.nonzero()[0]]  # выбрасываем нули из массива
    return difs.mean()
