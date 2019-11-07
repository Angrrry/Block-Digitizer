# -*- coding: utf-8 -*-
# if __name__=="__main__":
import final_stuff as fin
import contour as cnt
import wedges as wdg
import common_functions as cf
import axes
import work_with_files as wwf
from collections import namedtuple

palette = namedtuple("W", "CONTOUR AXE WEDGE")
WHITE, BLACK = palette([180, 164, 0], [255, 0, 0], [0, 0, 0]),\
    palette([200, 200, 0], [255, 0, 0], [200, 200, 0])
COL_VALUES = namedtuple("CV", "WHITE BLACK")
COL_VALUES = COL_VALUES(WHITE, BLACK)
"""Создаёт вложенный именонванный кортеж, хранящий значения цвета всяких штук.
К элементам можно обращаться конструкцией вида COL_VALUES.WHITE.AXE """

# Тут нужно вставить код, который делает скриншот и загружает изображение в IMG_NAME

IMG_NAME = "Untitled5.png"
IMG = wwf.open_image(IMG_NAME)
IMG = cf.crop_image(IMG)
AX_MASK = cf.color_mask(IMG, COL_VALUES.WHITE.AXE)
ANGLE, CENTER, SCALE = axes.get_rotation_angle(AX_MASK)
CENTER = [CENTER[1], CENTER[0]]
ROTATED_IMG = cf.rotate_image(IMG, ANGLE)
"""При повороте изображения значения пикселей немного меняются,
и створки уже не попадают в маску. Поэтому поворачиваем маску
оригинального изображения"""

WDG_MASK = cf.rotate_image(cf.color_mask(IMG, COL_VALUES.WHITE.WEDGE), ANGLE)

WEDGE_X, WEDGE_Y = wdg.get_wedges(WDG_MASK)

CONTOUR_MASK = cf.rotate_image(cf.color_mask(
    IMG, COL_VALUES.WHITE.CONTOUR), ANGLE)
ROTATED_AXE_MASK = cf.rotate_image(AX_MASK, ANGLE)
CONTOUR_MASK = cnt.draw_lines(
    CONTOUR_MASK, WEDGE_X, WEDGE_Y, int(round(SCALE)))
# возвращает уже не маску, а [200,200,200]
CONTOUR_MASK = cnt.fix_contour1(CONTOUR_MASK)
CONTOUR_MASK = cnt.inverse_fill(cnt.simple_fill(
    CONTOUR_MASK)).astype("int32")  # возвращает уже маску
CONTOUR_POINTS = cnt.get_contour(CONTOUR_MASK)
CONTOUR_POINTS = cnt.rearrange(CONTOUR_POINTS, CENTER)

# Копипаст из прошлой версии. Не гарантирую работоспособность
X, Y = fin.transform_coords(CONTOUR_POINTS, CENTER, SCALE)
wwf.writeinfile(X, Y, CENTER, IMG_NAME)
# wwf.generate_txt(WEDGE_X,WEDGE_Y,X,Y,CENTER)
