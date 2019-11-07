# -*- coding: utf-8 -*-
import numpy as np


def get_wedges(wedge_mask):
    """Допускаем, что значения створок - значения x0, y0,
    в которых сумма точек маски максимальна"""
    wedge_mask = np.where(wedge_mask != 0, 1,
                          0)  # При повороте значения пикселей изменились
    wedge_mask *= 200  # так виднее
    x, y = wedge_mask.sum(axis=1)[:, 0], wedge_mask.sum(axis=0)[:, 0]
    max2x, max2y = np.sort(
        x.argsort()[-2:][::-1]), np.sort(y.argsort()[-2:][::-1])
    return max2x.astype("int32"), max2y.astype("int32")


if __name__ != "__main__":
    print("Находим положение створок")
