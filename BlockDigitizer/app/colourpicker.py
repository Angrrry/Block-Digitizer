# -*- coding: utf-8 -*-
def main_colour(img):
    """Находит самый часто встрачающийся цвет и возвращает в формате RGB"""
    import cv2
    import numpy as np
    average = img.mean(axis=0).mean(axis=0)
    pixels = np.float32(img.reshape(-1, 3))
    n_colors = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(
        pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)
    dominant = palette[np.argmax(counts)]
    return dominant


def black_or_white(img):
    dominant_colour = main_colour(img)
    white = [255 for i in range(3)]
    # Не уверен в отказоустойчивости нижеприведённого кода
    if ((white - dominant_colour) < dominant_colour).all():
        return "WHITE"
    else:
        return "BLACK"


if __name__ == '__main__':
    import work_with_files as wwf
    for i in range(1, 8):
        img = wwf.open_image("{0}.PNG".format(i))
