# -*- coding: utf-8 -*-
"""
Authors:
========
Möllers, Konstantin (6313136)

"""

from __future__ import division

import numpy as np
import math
from numpy import linalg as la
from scipy import misc
from scipy.signal import convolve2d

def hue_to_rgb(hue, saturation=1, alpha=1):
    """
    Converts a HSV value to an RGB array.
    """
    alpha *= 255
    while hue < 0:
        hue += 2 * math.pi
    while hue > 2 * math.pi:
        hue -= 2 * math.pi

    k = 3 * hue / math.pi
    i = math.floor(k)
    f = (k - i)
    p = 255 * (1 - saturation)
    q = 255 * (1 - saturation * f)
    t = 255 * (1 - saturation * (1 - f))

    if i == 0 or i == 6:
        return [255, t, p, alpha]

    if i == 1:
        return [q, 255, p, alpha]

    if i == 2:
        return [p, 255, t, alpha]

    if i == 3:
        return [p, q, 255, alpha]

    if i == 4:
        return [t, p, 255, alpha]

    return [255, p, q, alpha]


class EdgeDetectionResult:
    def __init__(self, name, gradients):
        self.prefix = name
        self.gradients = gradients

    def save_gray_values(self, name, grayvalues):
        """
        Creates an image of some gray values.
        """
        misc.imsave("img/" + self.prefix + "_" + name + ".png", grayvalues)

    def save_magnitudes(self, mag=None):
        """
        Creates an image of the magnitudes.
        :param mag: explicit magnitudes to save
        """
        if mag is None:
            mag = -np.absolute(self.gradients)
        self.save_gray_values("magnitudes", mag)

    def save_real(self):
        """
        Creates an image of the real.
        """
        self.save_gray_values("real", np.real(self.gradients))

    def save_imag(self):
        """
        Creates an image of the imag.
        """
        self.save_gray_values("imag", np.imag(self.gradients))

    def save_directions(self, directions=None):
        """
        Creates an image of the directions.
        :param directions: Explicit directions to save.
        """
        if directions is None:
            directions = np.angle(self.gradients)

        height, width = directions.shape
        img = np.zeros((height, width, 4))
        for y in range(height):
            for x in range(width):
                img[y, x, :] = hue_to_rgb(hue=directions[y, x])

        misc.imsave("img/" + self.prefix + "_directions.png", img)

    def save_combined(self, mag=None, directions=None):
        """
        Creates an image of the directions.
        :param mag: Explicit magnitudes to save.
        :param directions: Explicit directions to save.
        """
        if mag is None:
            mag_abs = np.absolute(self.gradients)
            mag = mag_abs / np.max(mag_abs)
        if directions is None:
            directions = np.angle(self.gradients)

        height, width = directions.shape
        img = np.zeros((height, width, 4))
        for y in range(height):
            for x in range(width):
                img[y, x, :] = hue_to_rgb(directions[y, x], 1, mag[y, x])

        misc.imsave("img/" + self.prefix + "_combined.png", img)

    def save_images(self):
        for name in self.images.iterkeys():
            self.images[name].save(self.prefix + name + ".png")


class Image:
    def __init__(self, array):
        self.image = array

    @staticmethod
    def from_file(filename):
        """
        Creates an image from a file.

        :param filename: Filename to obtain the image file.
        :return: image instance.
        """
        return Image(misc.imread(filename, flatten=True))

    @staticmethod
    def from_lena():
        """
        :return: instance of the image showing Lena Söderberg from the 1972 US-american Playboy.
        """
        return Image(misc.lena())

    def save(self, filename):
        """
        Saves the image to file.

        :param filename: Filename for the saved image.
        """
        misc.imsave(filename, self.image)

    def _apply_operator(self, op_name, op_matrix):
        """
        Applies an edge detection operator on this image and returns the complex
        gradients and an edge detection result.
        :param op_name: Name of the operator.
        :param op_matrix: The Matrix needed for the operator.
        :return: an edge detection result object
        """
        grad = convolve2d(self.image, op_matrix, boundary='symm', mode='same')
        return EdgeDetectionResult(op_name, grad)

    def _apply_sobel_like(self, op_name, op_matrix):
        """
        Applies an Sobel-like edge detection operator.
        :param op_name: Name of the operator.
        :param op_matrix: The Matrix needed for the operator.
        :return: an edge detection result object
        """
        result = self._apply_operator(op_name, op_matrix)
        result.save_magnitudes()
        result.save_directions()
        result.save_real()
        result.save_imag()
        result.save_combined()

        return result

    def roberts_cross(self):
        """
        Calculates the Robert's Cross operator on this image.
        :return: an edge detection result object
        """
        roberts_cross_operator = np.array([[+0 - 1j, 1 + 0j],
                                           [-1 + 0j, 0 + 1j]])  # G1 + j*G2
        return self._apply_sobel_like("roberts_cross", roberts_cross_operator)

    def sobel(self):
        """
        Calculates the Sobel operator on this image.
        :return: an edge detection result object
        """
        sobel_operator = np.array([[-1-1j, +0-2j, +1-1j],
                                   [-2+0j, +0+0j, +2+0j],
                                   [-1+1j, +0+2j, +1+1j]])  # Gx + j*Gy
        return self._apply_sobel_like("sobel", sobel_operator)

    def scharr(self):
        """
        Calculates the Scharr operator on this image.
        :return: an edge detection result object
        """
        scharr_operator = np.array([[ -3-3j, 0-10j,  +3 -3j],
                                    [-10+0j, 0+ 0j, +10 +0j],
                                    [ -3+3j, 0+10j,  +3 +3j]])  # Gx + j*Gy
        return self._apply_sobel_like("scharr", scharr_operator)

    def prewitt(self):
        """
        Calculates the Prewitt operator on this image.
        :return: an edge detection result object
        """
        prewitt_operator = np.array([[-1-1j, 0-1j, +1-1j],
                                     [-1+0j, 0+0j, +1+0j],
                                     [-1+1j, 0+1j, +1+1j]])  # Gx + j*Gy
        return self._apply_sobel_like("prewitt", prewitt_operator)

    def kirsch(self):
        """
        Calculates the Kirsch operator on this image.
        :return: an edge detection result object
        """

        # Normalize image to 0..1
        g = self.image.copy() / 255

        # Get image dimensions and create resulting images
        shape = g.shape
        magnitudes = np.zeros(shape)
        directions = np.zeros(shape)
        height, width = shape

        # Some helper vars for optimization
        ks = range(8)  # 0..7
        mod = lambda k: k % 8
        limit = lambda k, mn, mx: mn if (k < mn) else mx if (k > mx) else k

        ys = [0, 1, 1, 1, 0, -1, -1, -1]  # Shift in Y direction
        xs = [1, 1, 0, -1, -1, -1, 0, 1]  # Shift in X direction

        for y in range(height):
            for x in range(width):
                gk = [g[limit(y + ys[k], 0, height - 1), limit(x + xs[k], 0, width - 1)] for k in ks]
                magns = [3 * (gk[k] + gk[mod(k + 1)] + gk[mod(k + 2)] + gk[mod(k + 3)] + gk[mod(k + 4)]) - 5 * (gk[mod(k + 5)] + gk[mod(k + 6)] + gk[mod(k + 7)]) for k in ks]
                k_max = np.argsort(magns)[7]

                # Calculate direction
                directions[y, x] = math.pi * ((4 + 2 + k_max) % 8) / 4

                # Get highest magnitude
                magnitudes[y, x] = magns[k_max]

        result = EdgeDetectionResult("kirsch", [])
        result.save_magnitudes(-magnitudes)
        result.save_directions(directions)
        result.save_combined(magnitudes / np.max(magnitudes), directions)

        return result

    def laplacian(self):
        """
        Calculates the Laplacian operator on this image.
        :return: an edge detection result object
        """
        laplacian_operator = np.array([[0,  1, 0],
                                       [1, -4, 1],
                                       [0,  1, 0]])
        result = self._apply_operator("laplacian", laplacian_operator)
        result.save_real()

        return result

if __name__ == '__main__':

    lena = Image.from_lena()
    lena.save("lena.png")
    #lena = Image.from_file("laura.jpg")

    print('Applying Robert\'s Cross operator ...'),
    lena.roberts_cross()
    print('done.')

    print('Applying Sobel operator ...'),
    lena.sobel()
    print('done.')

    print('Applying Scharr operator ...'),
    lena.scharr()
    print('done.')

    print('Applying Prewitt operator ...'),
    lena.prewitt()
    print('done.')

    print('Applying Kirsch operator ...'),
    lena.kirsch()
    print('done.')

    print('Applying Laplacian operator ...'),
    lena.laplacian()
    print('done.')

