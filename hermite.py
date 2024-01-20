import numpy as np
import cv2

def hermite_interpolate(p0, p1, p2, p3, t):
    """计算Hermite插值"""
    m0 = (p2 - p0) / 2
    m1 = (p3 - p1) / 2
    a = 2 * (p1 - p2) + m0 + m1
    b = -3 * (p1 - p2) - 2 * m0 - m1
    c = m0
    d = p1
    return a * t**3 + b * t**2 + c * t + d

def hermite_resize(image, new_width, new_height):
    """使用Hermite插值法调整图像大小"""
    old_height, old_width, channels = image.shape
    resized_image = np.zeros((new_height, new_width, channels), np.uint8)

    for y in range(new_height):
        for x in range(new_width):
            # 计算对应于旧图像中的坐标
            gx = x / (new_width / old_width)
            gy = y / (new_height / old_height)
            gxi = int(gx)
            gyi = int(gy)

            # 计算插值像素
            c = np.zeros(3)
            for channel in range(channels):
                p0 = image[max(gyi - 1, 0), max(gxi - 1, 0), channel]
                p1 = image[gyi, gxi, channel]
                p2 = image[min(gyi + 1, old_height - 1), min(gxi + 1, old_width - 1), channel]
                p3 = image[min(gyi + 2, old_height - 1), min(gxi + 2, old_width - 1), channel]

                c[channel] = hermite_interpolate(p0, p1, p2, p3, gy - gyi)

            resized_image[y, x] = np.clip(c, 0, 255)

    return resized_image

