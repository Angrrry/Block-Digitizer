"""Модуль для распространённых функций,
преимущественно матматических, нужных в других модулях"""
import numpy as np
import cv2


def distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def color_mask(image, rgb):
    axes = np.zeros_like(image)
    axes[(image[:, :, 0] == rgb[0]) & (image[:, :, 1] == rgb[1]) &
         (image[:, :, 2] == rgb[2])] = np.array([1, 1, 1], dtype="int32")
    return axes


def rotate_image(img, angle, center=None):
    if not center:
        (h, w, d) = img.shape
        center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotatedmask = cv2.warpAffine(img, M, (w, h))
    return rotatedmask


def show_image(img):
    cv2.imshow("contour points", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def crop_image(img):
    img = img.copy()
    mask = color_mask(img, [0, 200, 0]).astype("uint8")
    gray_image = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)
    contours, _ = cv2.findContours(
        gray_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 1:
        cnt = contours[0]
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box).transpose()
        img = img[np.min(box[1, :]):np.max(box[1, :]),
                  np.min(box[0, :]):np.max(box[0, :]), :]

    else:
        print('Уберите с экрана всё зелёное')
        raise ValueError
    return img


if __name__ == "__main__":
    import work_with_files as wwf
    import matplotlib.pyplot as plt
    img = wwf.open_image("test1.png")
    img = crop_image(img)
    plt.imshow(img)
    plt.show()
