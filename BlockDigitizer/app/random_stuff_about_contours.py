import work_with_files as wwf
from colourpicker import main_colour
import cv2
import tkinter
import numpy as np
import os


def Mask(image, R, G, B):
    axes = np.zeros_like(image)
    axes[(image[:, :, 0] == R) & (image[:, :, 1] == G) &
         (image[:, :, 2] == B)] = [1, 1, 1]
    return(axes)


img = wwf.open_image("1.PNG")
main_colour(img)
msk = Mask(img, 180, 164, 0)
img = msk * img
print(img.shape)
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(gray_image.shape)
contours, _ = cv2.findContours(
    gray_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print("no of shapes {0}".format(len(contours)))

for cnt in contours:
    epsilon = 0.005 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    img = cv2.drawContours(img, [approx], 0, (0, 255, 0), 1)
